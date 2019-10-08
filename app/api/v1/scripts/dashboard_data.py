"""
Copyright (c) 2018-2019 Qualcomm Technologies, Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
limitations in the disclaimer below) provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.
* The origin of this software must not be misrepresented; you must not claim that you wrote the original software.
If you use this software in a product, an acknowledgment is required by displaying the trademark/log as per the details
provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
* Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
* This notice may not be removed or altered from any source distribution.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
"""


from elasticsearch import Elasticsearch
from time import strftime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import calendar


es = Elasticsearch('http://192.168.100.223:9200')
es_doc_fields = {}


class DashBoardData:

    def __init__(self, url):
        self.url = url

    @staticmethod
    def script_start():

        print("-----------------------Calculations for DashBoard's Data is started ----------------------------")

        return

    @staticmethod
    def script_update_time():

        if not es.indices.exists(index="dashboard_data"):
            es.indices.create(index="dashboard_data", ignore=400)

        started_at = strftime("%Y-%m-%d %H:%M:%S")

        es_doc_fields['dashboard_updation_started'] = started_at

        print("Script starts at : ", started_at)
        print("------------------------------------------------------------------------------------------------")

    @staticmethod
    def core_main_counters():

        core_total_imeis = {}
        core_compliant_imeis = {}
        core_non_compliant_imeis = {}
        monthly_imeis_list = []
        monthly_imeis_sum = 0
        monthly_noncompliant_imeis_list = []
        monthly_noncompliant_imeis_sum = 0
        monthly_compliant_imeis_list = []
        monthly_compliant_imeis_sum = 0

        qry_total_core_imeis = {
            "aggs": {
                "unique_imeis": {
                    "cardinality": {
                        "field": "imei_norm.keyword",
                        "precision_threshold": 40000
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "last_seen"
                            }
                        },
                        {
                            "exists": {
                                "field": "first_seen"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.search(index='alias_mno_data_dump', body=qry_total_core_imeis, request_timeout=60)

        total_core_imeis = qry['aggregations']['unique_imeis']['value']

        qry_total_non_compliant_imeis = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "classification_block_date"
                            }
                        },
                        {
                            "exists": {
                                "field": "classification_imei"
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "exists": {
                                "field": "classification_end_date"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.count(index='alias_join_mno_dump-classification', body=qry_total_non_compliant_imeis,
                       request_timeout=60)

        total_non_compliant_imeis = qry['count']

        total_compliant_imeis = total_core_imeis - total_non_compliant_imeis

        current_time = datetime.now()

        trend_months, end_date = month_range(current_time.month, current_time.year, -6)

        for v in trend_months:
            year, month = v.split('-', 1)
            qry_monthly_imeis = {
                "aggs": {
                    "unique_imeis": {
                        "cardinality": {
                            "field": "imei_norm.keyword",
                            "precision_threshold": 40000
                        }
                    }
                },
                "size": 0,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "exists": {
                                    "field": "last_seen"
                                }
                            },
                            {
                                "exists": {
                                    "field": "first_seen"
                                }
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "match": {
                                    "triplet_year": year
                                }
                            },
                            {
                                "match": {
                                    "triplet_month": month
                                }
                            }
                        ]
                    }
                }
            }

            qry = es.search(index='alias_mno_data_dump', body=qry_monthly_imeis, request_timeout=60)

            t_imeis = qry['aggregations']['unique_imeis']['value']

            monthly_imeis_list.append(t_imeis)
            monthly_imeis_sum = monthly_imeis_sum + t_imeis

            qry_monthly_noncompliant_imeis = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "exists": {
                                    "field": "classification_block_date"
                                }
                            },
                            {
                                "exists": {
                                    "field": "classification_imei"
                                }
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "match": {
                                    "triplet_year": year
                                }
                            },
                            {
                                "match": {
                                    "triplet_month": month
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "exists": {
                                    "field": "classification_end_date"
                                }
                            }
                        ]
                    }
                }
            }

            qry = es.count(index='alias_join_mno_dump-classification', body=qry_monthly_noncompliant_imeis,
                           request_timeout=60)

            n_imeis = qry['count']

            monthly_noncompliant_imeis_list.append(n_imeis)
            monthly_noncompliant_imeis_sum = monthly_noncompliant_imeis_sum + n_imeis

            c_imeis = t_imeis - n_imeis
            monthly_compliant_imeis_list.append(c_imeis)
            monthly_compliant_imeis_sum = monthly_compliant_imeis_sum + c_imeis

        monthly_imeis_avg = int(round((monthly_imeis_sum/6), 0))
        monthly_noncompliant_imeis_avg = int(round((monthly_noncompliant_imeis_sum / 6), 0))
        monthly_compliant_imeis_avg = int(round((monthly_compliant_imeis_sum / 6), 0))

        t_trend_up, t_avg_trend = monthly_trend(monthly_imeis_list)
        c_trend_up, c_avg_trend = monthly_trend(monthly_compliant_imeis_list)
        n_trend_up, n_avg_trend = monthly_trend(monthly_noncompliant_imeis_list)

        core_total_imeis['total_core_imeis'] = total_core_imeis
        core_total_imeis['monthly_total_imeis_avg'] = monthly_imeis_avg
        core_total_imeis['total_avg_trend'] = t_avg_trend
        core_total_imeis['total_trend_up'] = t_trend_up

        es_doc_fields['B1_core_total_imeis'] = core_total_imeis

        core_compliant_imeis['core_compliant_imeis'] = total_compliant_imeis
        core_compliant_imeis['monthly_compliant_imeis_avg'] = monthly_compliant_imeis_avg
        core_compliant_imeis['compliant_avg_trend'] = c_avg_trend
        core_compliant_imeis['compliant_trend_up'] = c_trend_up

        es_doc_fields['B2_core_compliant_imeis'] = core_compliant_imeis

        core_non_compliant_imeis['total_non_compliant_imeis'] = total_non_compliant_imeis
        core_non_compliant_imeis['monthly_non_compliant_imeis_avg'] = monthly_noncompliant_imeis_avg
        core_non_compliant_imeis['non_compliant_avg_trend'] = n_avg_trend
        core_non_compliant_imeis['non_compliant_trend_up'] = n_trend_up

        es_doc_fields['B3_core_non_compliant_imeis'] = core_non_compliant_imeis

        print("BOX-01: Total IMEIs Details")
        print("Total CORE IMEIs : ", total_core_imeis)
        print("Monthly Total-IMEIs Avg : ", monthly_imeis_avg)
        print("Monthly_Avg Total-IMEIs % trend : ", t_avg_trend)
        print("Total Trend_UP : ", t_trend_up)
        print("------------------------------------------------------------------------------------------------")
        print("BOX-02: CORE Compliant IMEIs Details")
        print("Total Compliant IMEIs : ", total_compliant_imeis)
        print("Monthly Compliant-IMEIs Avg : ", monthly_compliant_imeis_avg)
        print("Monthly_Avg Compliant-IMEIs % trend : ", c_avg_trend)
        print("Compliant Trend_UP : ", c_trend_up)
        print("------------------------------------------------------------------------------------------------")
        print("BOX-03: CORE Non-Compliant IMEIs Details")
        print("Total Non-Compliant IMEIs : ", total_non_compliant_imeis)
        print("Monthly Non-Compliant-IMEIs Avg : ", monthly_noncompliant_imeis_avg)
        print("Monthly_Avg Non-Compliant-IMEIs % trend : ", n_avg_trend)
        print("Non-Compliant Trend_UP : ", n_trend_up)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def dps_main_counters():

        dps_total_imeis = {}
        monthly_dps_imeis_list = []
        monthly_dps_imeis_sum = 0

        qry = es.count(index='alias_dps', request_timeout=60)
        total_dps_imeis = qry['count']

        current_time = datetime.now()

        trend_months, end_date = month_range(current_time.month, current_time.year, -6)

        for v in end_date:
            year, month, day = v.split('-', 2)

            qry_monthly_dps_imeis = {
                "query": {
                    "bool": {
                        "filter": {
                            "bool": {
                                "must": [
                                    {
                                        "match_all": {}
                                    },
                                    {
                                        "range": {
                                            "pairing_created_on": {
                                                "gte": str(year) + '-' + str(month) + '-01',
                                                "lte": v
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }

            qry = es.count(index='alias_dps', body=qry_monthly_dps_imeis, request_timeout=60)
            dps_imeis = qry['count']

            monthly_dps_imeis_list.append(dps_imeis)
            monthly_dps_imeis_sum = monthly_dps_imeis_sum + dps_imeis

        monthly_dps_imeis_avg = int(round((monthly_dps_imeis_sum / 6), 0))
        d_trend_up, d_avg_trend = monthly_trend(monthly_dps_imeis_list)

        dps_total_imeis['total_dps_imeis'] = total_dps_imeis
        dps_total_imeis['monthly_dps_imeis_avg'] = monthly_dps_imeis_avg
        dps_total_imeis['dps_avg_trend'] = d_avg_trend
        dps_total_imeis['dps_trend_up'] = d_trend_up

        es_doc_fields['B4_dps_paired_imeis'] = dps_total_imeis

        print("BOX-04: DPS Details")
        print("Total DPS IMEIs : ", total_dps_imeis)
        print("Monthly DPS-IMEIs Avg : ", monthly_dps_imeis_avg)
        print("Monthly_Avg DPS-IMEIs % trend : ", d_avg_trend)
        print("DPS Trend_UP : ", d_trend_up)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def lsds_main_counters():

        lsds_total_devices = {}
        monthly_lsds_devices_list = []
        monthly_lsds_devices_sum = 0

        qry_total_lsds_devices = {
            "aggs": {
                "unique_devices": {
                    "cardinality": {
                        "field": "case_id",
                        "precision_threshold": 40000
                    }
                }
            },
            "size": 0
        }

        qry = es.search(index='alias_lsds', body=qry_total_lsds_devices, request_timeout=60)

        total_lsds_devices = qry['aggregations']['unique_devices']['value']

        current_time = datetime.now()

        trend_months, end_date = month_range(current_time.month, current_time.year, -6)

        for v in end_date:
            year, month, day = v.split('-', 2)

            qry_monthly_lsds_devices = {
                "aggs": {
                    "unique_devices": {
                        "cardinality": {
                            "field": "case_id",
                            "precision_threshold": 40000
                        }
                    }
                },
                "size": 0,
                "query": {
                    "bool": {
                        "filter": {
                            "bool": {
                                "must": [
                                    {
                                        "match_all": {}
                                    },
                                    {
                                        "range": {
                                            "case_reported_date": {
                                                "gte": str(year) + '-' + str(month) + '-01',
                                                "lte": v
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }

            qry = es.search(index='alias_lsds', body=qry_monthly_lsds_devices, request_timeout=60)
            lsds_devices = qry['aggregations']['unique_devices']['value']

            monthly_lsds_devices_list.append(lsds_devices)
            monthly_lsds_devices_sum = monthly_lsds_devices_sum + lsds_devices

        monthly_lsds_devices_avg = int(round((monthly_lsds_devices_sum / 6), 0))
        l_trend_up, l_avg_trend = monthly_trend(monthly_lsds_devices_list)

        lsds_total_devices['total_lsds_devices'] = total_lsds_devices
        lsds_total_devices['monthly_lsds_devices_avg'] = monthly_lsds_devices_avg
        lsds_total_devices['lsds_avg_trend'] = l_avg_trend
        lsds_total_devices['lsds_trend_up'] = l_trend_up

        es_doc_fields['B5_lsds_reported_devices'] = lsds_total_devices

        print("BOX-05: LSDS Details")
        print("Total LSDS Devices : ", total_lsds_devices)
        print("Monthly LSDS-Devices Avg : ", monthly_lsds_devices_avg)
        print("Monthly_Avg Devices % trend : ", l_avg_trend)
        print("LSDS Trend_Up : ", l_trend_up)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def drs_main_counters():

        drs_total_imeis = {}
        monthly_drs_imeis_list = []
        monthly_drs_imeis_sum = 0

        qry_total_drs_imeis = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "registration_status": "Approved"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.count(index='alias_drs_reg', body=qry_total_drs_imeis, request_timeout=60)
        total_drs_imeis = qry['count']

        current_time = datetime.now()

        trend_months, end_date = month_range(current_time.month, current_time.year, -6)

        for v in end_date:
            year, month, day = v.split('-', 2)

            qry_monthly_drs_imeis = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "registration_status": "Approved"
                                }
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "registration_date": {
                                        "gte": str(year) + '-' + str(month) + '-01',
                                        "lte": v
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            qry = es.count(index='alias_drs_reg', body=qry_monthly_drs_imeis, request_timeout=60)
            drs_imeis = qry['count']

            monthly_drs_imeis_list.append(drs_imeis)
            monthly_drs_imeis_sum = monthly_drs_imeis_sum + drs_imeis

        monthly_drs_imeis_avg = int(round((monthly_drs_imeis_sum / 6), 0))
        drs_trend_up, drs_avg_trend = monthly_trend(monthly_drs_imeis_list)

        drs_total_imeis['total_drs_imeis'] = total_drs_imeis
        drs_total_imeis['monthly_drs_imeis_avg'] = monthly_drs_imeis_avg
        drs_total_imeis['drs_avg_trend'] = drs_avg_trend
        drs_total_imeis['drs_trend_up'] = drs_trend_up

        es_doc_fields['B6_drs_registered_imeis'] = drs_total_imeis

        print("BOX-06: DRS Details")
        print("Total DRS IMEIs : ", total_drs_imeis)
        print("Monthly DRS-IMEIs Avg : ", monthly_drs_imeis_avg)
        print("Monthly_Avg IMEIs % trend : ", drs_avg_trend)
        print("DRS Trend_UP : ", drs_trend_up)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def operator_wise_imeis():

        operators_imeis = {}
        qry_operator_wise_imeis = {
            "aggs": {
                "MNOs": {
                    "terms": {
                        "field": "operator_id.keyword",
                        "size": 10,
                        "order": {
                            "unique_imeis": "desc"
                        }
                    },
                    "aggs": {
                        "unique_imeis": {
                            "cardinality": {
                                "field": "imei_norm.keyword",
                                "precision_threshold": 40000
                            }
                        }
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                        },
                        {
                            "exists": {
                                "field": "last_seen"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.search(index='alias_mno_data_dump', body=qry_operator_wise_imeis, request_timeout=60)

        total_mnos_imeis = qry['hits']['total']

        for val in qry['aggregations']['MNOs']['buckets']:
            operators_imeis[val['key']] = val['unique_imeis']['value']

        operators_imeis['total_MNOs_IMEIs'] = total_mnos_imeis
        es_doc_fields['B7_operator_wise_imeis'] = operators_imeis

        print("BOX-07: Operator-Wise IMEIs in CORE")
        print("Total MNOs IMEIs : ", total_mnos_imeis)
        print("Operator wise IMEIs : ", operators_imeis)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def operators_imeis_six_month_trend():

        result = {"six_months_trend": []}
        operators_imeis = {}

        current_time = datetime.now()

        trend_months, end_date = month_range(current_time.month, current_time.year, -6)

        for v in end_date:
            year, month, day = v.split('-', 2)
            qry_monthly_operators_imeis = {
                "aggs": {
                    "MNOs": {
                        "terms": {
                            "field": "operator_id.keyword",
                            "size": 6,
                            "order": {
                                "unique_imeis": "desc"
                            }
                        },
                        "aggs": {
                            "unique_imeis": {
                                "cardinality": {
                                    "field": "imei_norm.keyword",
                                    "precision_threshold": 40000
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "last_seen": {
                                        "gte": str(year) + '-' + str(month) + '-01',
                                        "lte": v
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            qry = es.search(index='alias_mno_data_dump', body=qry_monthly_operators_imeis, request_timeout=60)

            operators_imeis['trend_date'] = str(year) + '-' + str(month)

            if qry['aggregations']['MNOs']['buckets']:
                for val in qry['aggregations']['MNOs']['buckets']:
                    operators_imeis[val['key']] = val['unique_imeis']['value']
            else:
                continue

            result['six_months_trend'].append(dict(operators_imeis))

        es_doc_fields['B8_operators_imeis_trend'] = result

        print("BOX-08: Operator-IMEIs Six Month Trend in CORE")
        print("Operator-IMEIs Trend: ", result)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def operators_wise_blocking():

        operators_blckd_imeis = {}
        qry_operators_wise_blocking = {
            "aggs": {
                "MNOs": {
                    "terms": {
                        "field": "mno_operator.keyword",
                        "size": 15,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                        }
                    ]
                }
            }
        }

        qry = es.search(index='alias_join_mno_dump-blacklist', body=qry_operators_wise_blocking, request_timeout=60)

        total_blckd_imeis = qry['hits']['total']

        for val in qry['aggregations']['MNOs']['buckets']:
            operators_blckd_imeis[val['key']] = val['doc_count']

        operators_blckd_imeis['total_blocked_IMEIs'] = total_blckd_imeis
        es_doc_fields['B9_operator_wise_blocked_imeis'] = operators_blckd_imeis

        print("BOX-09: Operator-Wise Blocked IMEIs in CORE")
        print("Total Blocked IMEIs : ", total_blckd_imeis)
        print("Operator-wise Blocked IMEIs : ", operators_blckd_imeis)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def drs_imeis_devices():

        drs_imeis_trend = {"drs_imei_status": {}, "last_3_months_imeis": {}}
        qry_total_unique_drs_imeis = {
            "aggs": {
                "unique_imeis": {
                    "cardinality": {
                        "field": "imeis.keyword",
                        "precision_threshold": 40000
                    }
                }
            },
            "size": 0
        }

        qry_1 = es.search(index='alias_drs_reg', body=qry_total_unique_drs_imeis, request_timeout=60)

        total_drs_imeis = qry_1['aggregations']['unique_imeis']['value']

        qry_drs_imeis_status = {
            "aggs": {
                "statuses": {
                    "terms": {
                        "field": "registration_status.keyword",
                        "size": 3,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "unique_imeis": {
                            "cardinality": {
                                "field": "imeis.keyword",
                                "precision_threshold": 40000
                            }
                        }
                    }
                }
            },
            "size": 0,
            "query": {
                "terms": {
                    "registration_status.keyword": [
                        "Approved",
                        "Rejected",
                        "Pending Review"
                    ]
                }
            }
        }

        qry_2 = es.search(index='alias_drs_reg', body=qry_drs_imeis_status, request_timeout=60)

        status_sum = 0
        for val in qry_2['aggregations']['statuses']['buckets']:
            drs_imeis_trend['drs_imei_status'][val['key']] = val['unique_imeis']['value']
            status_sum = status_sum + val['unique_imeis']['value']

        if status_sum > total_drs_imeis:
            status_sum_percnt = "100%"
        else:
            status_sum_percnt = str(round((status_sum / total_drs_imeis) * 100)) + "%"

        drs_imeis_trend['drs_imei_status']['statuses_percentage'] = status_sum_percnt

        qry_approved_devices = {
            "aggs": {
                "unique_devices": {
                    "cardinality": {
                        "field": "device_id",
                        "precision_threshold": 40000
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "registration_status": "Approved"
                            }
                        }
                    ]
                }
            }
        }

        qry_3 = es.search(index='alias_drs_reg', body=qry_approved_devices, request_timeout=60)

        approved_devices = qry_3['aggregations']['unique_devices']['value']

        current_time = datetime.now()

        trend_months, end_date = month_range(current_time.month, current_time.year, -3)

        for v in end_date:
            year, month, day = v.split('-', 2)
            qry__last_3_months_total_imeis = {
                "aggs": {
                    "unique_imeis": {
                        "cardinality": {
                            "field": "imeis.keyword",
                            "precision_threshold": 40000
                        }
                    }
                },
                "size": 0,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "registration_date": {
                                        "gte": str(year) + '-' + str(month) + '-01',
                                        "lte": v
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            qry_4 = es.search(index='alias_drs_reg', body=qry__last_3_months_total_imeis, request_timeout=60)

            month_name = calendar.month_abbr[int(month)]
            drs_imeis_trend['last_3_months_imeis'][month_name] = qry_4['aggregations']['unique_imeis']['value']

        drs_imeis_trend['total_drs_imeis'] = total_drs_imeis
        drs_imeis_trend['drs_approved_devices'] = approved_devices
        es_doc_fields['B10_drs_imeis_trend'] = drs_imeis_trend

        print("BOX-10: DRS IMEIs Trend & Devices Count")
        print("DRS Total-IMEIs: ", total_drs_imeis)
        print("DRS Total Approved-Devices: ", approved_devices)
        print("DRS Last 3-Months Total-IMEIs: ", drs_imeis_trend['last_3_months_imeis'])
        print("DRS IMEIs Statuses: ", drs_imeis_trend['drs_imei_status'])
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def drs_technology_approved_devices():

        rat_approved_devices = {"approved_devices": []}
        rat_device = {"x_axis": "", "y_axis": "", "percentage": ""}
        qry_rat_devices = {
            "aggs": {
                "rat": {
                    "terms": {
                        "field": "technologies.keyword",
                        "size": 4,
                        "order": {
                            "unique_devices": "desc"
                        }
                    },
                    "aggs": {
                        "unique_devices": {
                            "cardinality": {
                                "field": "device_id",
                                "precision_threshold": 40000
                            }
                        }
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                        },
                        {
                            "match_phrase": {
                                "registration_status": "Approved"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.search(index='alias_drs_reg', body=qry_rat_devices, request_timeout=60)

        total_devices = 0
        for val in qry['aggregations']['rat']['buckets']:
            rat_device['y_axis'] = val['key']
            rat_device['x_axis'] = val['unique_devices']['value']
            rat_device['percentage'] = ""
            total_devices = total_devices + val['unique_devices']['value']
            rat_approved_devices['approved_devices'].append(dict(rat_device))

        for v in rat_approved_devices['approved_devices']:
            v['percentage'] = str(round((v['x_axis']/total_devices * 100), 2)) + '%'

        rat_approved_devices['total_approved_devices'] = total_devices
        es_doc_fields['B11_drs_technology_wise_devices'] = rat_approved_devices

        print("BOX-11: DRS Technology-Wise Approved Devices")
        print("Total Approved Devices: ", total_devices)
        print("DRS RAT-Wise Approved-Devices: ", rat_approved_devices['approved_devices'])
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def drs_top_approved_brands():

        drs_top_brands = {"drs_top_brands": {}}
        qry_top_brands = {
            "aggs": {
                "brands": {
                    "terms": {
                        "field": "registered_brand.keyword",
                        "size": 5,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                        },
                        {
                            "match_phrase": {
                                "registration_status": "Approved"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.search(index='alias_drs_reg', body=qry_top_brands, request_timeout=60)
        total_top_brands = 0
        for val in qry['aggregations']['brands']['buckets']:
            drs_top_brands['drs_top_brands'][val['key']] = val['doc_count']
            total_top_brands = total_top_brands + val['doc_count']
        drs_top_brands['total_top_brands'] = total_top_brands
        es_doc_fields['B12_drs_top_approved_brands'] = drs_top_brands

        print("BOX-12: DRS Top Approved Brands")
        print("Total Top Devices: ", total_top_brands)
        print("DRS Top Approved-Brands: ", drs_top_brands['drs_top_brands'])
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def dps_pairing_types():

        pairing_types = {}
        qry_primary_secondary_count = {
            "aggs": {
                "primary": {
                    "terms": {
                        "field": "primary_pair",
                        "size": 2
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "match_all": {}
                                },
                                {
                                    "exists": {
                                        "field": "imsi"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        qry = es.search(index='alias_dps', body=qry_primary_secondary_count, request_timeout=60)

        for val in qry['aggregations']['primary']['buckets']:
            if val['key'] == 1:
                pairing_types['primary_pairs'] = val['doc_count']
            else:
                pairing_types['secondary_pairs'] = val['doc_count']

        es_doc_fields['B13_dps_pairing_types_count'] = pairing_types

        print("BOX-13: DPS Primary Vs Secondary  Pairs")
        print("Total Primary-Pairs: ", pairing_types['primary_pairs'])
        print("Total Secondary-Pairs: ", pairing_types['secondary_pairs'])
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def dps_mnos_active_pairs():

        mno_active_pairs = {}
        qry_mno_active_pairs = {
            "aggs": {
                "MNOs": {
                    "terms": {
                        "field": "operator_name.keyword",
                        "size": 10
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "match_all": {}
                                },
                                {
                                    "exists": {
                                        "field": "operator_name"
                                    }
                                },
                                {
                                    "exists": {
                                        "field": "imsi"
                                    }
                                }
                            ],
                            "must_not": [
                                {
                                    "exists": {
                                        "field": "pairing_ended_on"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        qry = es.search(index='alias_dps', body=qry_mno_active_pairs, request_timeout=60)

        for val in qry['aggregations']['MNOs']['buckets']:
            mno_active_pairs[val['key']] = val['doc_count']

        es_doc_fields['B14_dps_operators_active_pairs'] = mno_active_pairs

        print("BOX-14: DPS Operator-Wise Active Pairs")
        print("Operators Active-Pairs: ", mno_active_pairs)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def dps_pairs_classification():

        pair_classification = {}
        pair_cond = ["must", "must_not"]

        for value in pair_cond:
            qry_pair_classification = {
                "query": {
                    "bool": {
                        value: [
                            {
                                "exists": {
                                    "field": "pairing_ended_on"
                                }
                            }
                        ]
                    }
                }
            }

            qry1 = es.count(index='alias_dps', body=qry_pair_classification, request_timeout=60)

            if value == "must":
                pair_classification['deleted_pairs'] = qry1['count']
            elif value == "must_not":
                pair_classification['active_pairs'] = qry1['count']

        qry_active_pairs = {
            "aggs": {
                "pairs": {
                    "terms": {
                        "field": "is_pair_active",
                        "size": 2
                    }
                }
            },
            "size": 0
        }

        qry2 = es.search(index='alias_dps', body=qry_active_pairs, request_timeout=60)

        for val in qry2['aggregations']['pairs']['buckets']:
            if val['key'] == 1:
                pair_classification['permanent_pairs'] = val['doc_count']
            else:
                pair_classification['temporary_pairs'] = val['doc_count']

        es_doc_fields['B15_dps_pairs_classification'] = pair_classification

        print("BOX-15: DPS Pairs Classification")
        print("Total Active Pairs : ", pair_classification['active_pairs'])
        print("Total Deleted Pairs : ", pair_classification['deleted_pairs'])
        print("Total permanent Pairs : ", pair_classification['permanent_pairs'])
        print("Total Temporary Pairs : ", pair_classification['temporary_pairs'])
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def lsds_devices_status():

        device_status_details = {"statuses": []}
        device_status = {"x_axis": "", "y_axis": "", "percentage": ""}
        qry_lsds_devices_status = {
            "aggs": {
                "status": {
                    "terms": {
                        "field": "case_status.keyword",
                        "size": 3,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "unique_devices": {
                            "cardinality": {
                                "field": "case_id",
                                "precision_threshold": 40000
                            }
                        }
                    }
                }
            },
            "size": 0
        }

        qry = es.search(index='alias_lsds', body=qry_lsds_devices_status, request_timeout=60)

        devices_sum = 0
        for val in qry['aggregations']['status']['buckets']:
            device_status['y_axis'] = val['key']
            device_status['x_axis'] = val['unique_devices']['value']
            device_status['percentage'] = ""
            devices_sum = devices_sum + val['unique_devices']['value']
            device_status_details['statuses'].append(dict(device_status))

        for v in device_status_details['statuses']:
            v['percentage'] = str(round((v['x_axis'] / devices_sum * 100), 2)) + '%'

        device_status_details['total_devices'] = devices_sum
        es_doc_fields['B16_lsds_devices_status'] = device_status_details

        print("BOX-16: LSDS Devices Status")
        print("Total LSDS Devices: ", devices_sum)
        print("Devices Statuses: ", device_status_details['statuses'])
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def lsds_devices_trend():

        result = {"lsds_six_months_trend": []}
        lsds_devices = {}

        current_time = datetime.now()
        trend_months, end_date = month_range(current_time.month, current_time.year, -6)

        for v in end_date:
            year, month, day = v.split('-', 2)
            qry_lsds_devices_trend = {
                "aggs": {
                    "status": {
                        "terms": {
                            "field": "case_status.keyword",
                            "size": 3,
                            "order": {
                                "_count": "desc"
                            }
                        },
                        "aggs": {
                            "unique_devices": {
                                "cardinality": {
                                    "field": "case_id",
                                    "precision_threshold": 40000
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "case_reported_date": {
                                        "gte": str(year) + '-' + str(month) + '-01',
                                        "lte": v
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            qry = es.search(index='alias_lsds', body=qry_lsds_devices_trend, request_timeout=60)
            lsds_devices['trend_date'] = str(year) + '-' + str(month)

            if qry['aggregations']['status']['buckets']:
                for val in qry['aggregations']['status']['buckets']:
                    lsds_devices[val['key']] = val['unique_devices']['value']
            else:
                continue

            result['lsds_six_months_trend'].append(dict(lsds_devices))

        es_doc_fields['B17_lsds_devices_trend'] = result

        print("BOX-17: LSDS Devices Six-Months Status Trend")
        print("LSDS Devices Trend: ", result)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def lsds_top_stolen_lost_brands():

        lsds_top_brands = {}
        qry_most_stolen_lost_brands = {
            "aggs": {
                "top_brands": {
                    "terms": {
                        "field": "reported_brand.keyword",
                        "size": 5,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "unique_devices": {
                            "cardinality": {
                                "field": "case_id",
                                "precision_threshold": 400
                            }
                        }
                    }
                }
            },
            "size": 0
        }

        qry = es.search(index='alias_lsds', body=qry_most_stolen_lost_brands, request_timeout=60)
        for val in qry['aggregations']['top_brands']['buckets']:
            lsds_top_brands[val['key']] = val['unique_devices']['value']

        es_doc_fields['B18_lsds_top_brands'] = lsds_top_brands

        print("BOX-18: LSDS Top Stolen/Lost Brands")
        print("LSDS Top Stolen/Lost Brands: ", lsds_top_brands)
        print("------------------------------------------------------------------------------------------------")

        return

    @staticmethod
    def script_completed_time():

        completed_at = strftime("%Y-%m-%d %H:%M:%S")

        es_doc_fields['dashboard_updation_completed'] = completed_at

        es.index(index='dashboard_data', doc_type='doc', id=1, body=es_doc_fields)

        print("Script Completed at : ", completed_at)
        print("------------------------------------------------------------------------------------------------")


def monthly_trend(monthly_imeis_list):

    if monthly_imeis_list[4] == 0 and monthly_imeis_list[5] != 0:
        avg_trend = '100%'
        trend_up = True
    elif monthly_imeis_list[5] == 0 or (monthly_imeis_list[5] == 0 and monthly_imeis_list[4] == 0):
        avg_trend = '0%'
        trend_up = False
    else:
        tmp_trend = (monthly_imeis_list[5] / monthly_imeis_list[4]) * 100
        tmp_trend = round((tmp_trend - 100), 2)

        if tmp_trend < 0:
            trend_up = False
            avg_trend = str(-tmp_trend) + '%'
        else:
            trend_up = True
            avg_trend = str(tmp_trend) + '%'

    return trend_up, avg_trend


def month_range(month, year, total_months):
    trend_duration = []
    month_end = []

    initial_date = str(year) + '-' + str(month)

    i_date = datetime.strptime(initial_date, '%Y-%m')

    prev_date = i_date.date() + relativedelta(months=total_months)

    date_list = pd.date_range(prev_date, i_date, freq='M')

    for val in date_list:
        val1 = val.strftime('%Y-%m')
        val2 = val.strftime('%Y-%m-%d')
        trend_duration.append(val1)
        month_end.append(val2)

    # trend_duration.append(initial_date)
    return trend_duration, month_end


if __name__ == "__main__":
    DashBoardData.script_start()
    DashBoardData.script_update_time()
    DashBoardData.core_main_counters()
    DashBoardData.dps_main_counters()
    DashBoardData.lsds_main_counters()
    DashBoardData.drs_main_counters()
    DashBoardData.operator_wise_imeis()
    DashBoardData.operators_imeis_six_month_trend()
    DashBoardData.operators_wise_blocking()
    DashBoardData.drs_imeis_devices()
    DashBoardData.drs_technology_approved_devices()
    DashBoardData.drs_top_approved_brands()
    DashBoardData.dps_pairing_types()
    DashBoardData.dps_mnos_active_pairs()
    DashBoardData.dps_pairs_classification()
    DashBoardData.lsds_devices_status()
    DashBoardData.lsds_devices_trend()
    DashBoardData.lsds_top_stolen_lost_brands()
    DashBoardData.script_completed_time()
