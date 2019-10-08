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


from app import es, conf
from calendar import monthrange


class ComplianceBreakdown:

    def __init__(self, para):
        self.para = para

    def imei_breakdown(self):

        global total_mno_triplets

        b = self.para
        result = {"Compliance_Breakdown": {}}

        a, no_of_days = monthrange(b['trend_year'], b['trend_month'])

        if b['trend_month'] < 10:
            start_date_range = str(b['trend_year']) + '-0' + str(b['trend_month']) + '-01'
            end_date_range = str(b['trend_year']) + '-0' + str(b['trend_month']) + '-' + str(no_of_days)
        else:
            start_date_range = str(b['trend_year']) + '-' + str(b['trend_month']) + '-01'
            end_date_range = str(b['trend_year']) + '-' + str(b['trend_month']) + '-' + str(no_of_days)

        qry_classification_count = {
            "aggs": {
                "run_id": {
                    "terms": {
                        "field": "run_id",
                        "size": 31,         # in-case classification runs on daily basis
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
                            "exists": {
                                "field": "block_date"
                            }
                        },
                        {
                            "range": {
                                "start_date": {
                                    "gte": start_date_range,
                                    "lte": end_date_range
                                }
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "exists": {
                                "field": "end_date"
                            }
                        }
                    ]
                }
            }
        }

        qry1 = es.search(index=conf['core_indices']['core_classification_data'], body=qry_classification_count,
                         request_timeout=conf['request_timeout'])

        result['Compliance_Breakdown']['non-compliant_imeis'] = qry1['hits']['total']

        qry_mno_count = {
            "aggs": {
                "unique_imeis": {
                    "cardinality": {
                        "field": "imei_norm.keyword",
                        "precision_threshold": b['precision_threshold']
                    }
                },
                "unique_triplets": {
                    "cardinality": {
                        "field": "triplet_hash.keyword",
                        "precision_threshold": b['precision_threshold']
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
                            "match": {
                                "triplet_year": b['trend_year']
                            }
                        },
                        {
                            "match": {
                                "triplet_month": b['trend_month']
                            }
                        }
                    ]
                }
            }
        }

        qry2 = es.search(index=conf['core_indices']['core_mno_data'], body=qry_mno_count,
                         request_timeout=conf['request_timeout'])

        total_hits = qry2['hits']['total']

        if qry2['aggregations']['unique_imeis']['value'] > total_hits:
            total_mno_imeis = total_hits
        else:
            total_mno_imeis = qry2['aggregations']['unique_imeis']['value']

        if qry2['aggregations']['unique_triplets']['value'] > total_hits:
            total_mno_triplets = total_hits
        else:
            total_mno_triplets = qry2['aggregations']['unique_triplets']['value']

        if total_mno_imeis != 0:
            nc_imeis_percnt = round(((result['Compliance_Breakdown']['non-compliant_imeis'] /
                                      total_mno_imeis) * 100), 2)
        else:
            nc_imeis_percnt = 0

        result['Compliance_Breakdown']['non-compliant_imeis %'] = nc_imeis_percnt

        result['Compliance_Breakdown']['compliant_imeis'] = total_mno_imeis - \
                                                            result['Compliance_Breakdown']['non-compliant_imeis']

        result['Compliance_Breakdown']['compliant_imeis %'] = round((100 - nc_imeis_percnt), 2)

        return result, 200

    def triplet_breakdown(self):

        c = self.para
        result = {}

        qry_triplet_count_join = {
            "aggs": {
                "triplet_hash": {
                    "cardinality": {
                        "field": "triplet_hash.keyword",
                        "precision_threshold": c['precision_threshold']
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
                                "field": "classification_block_date"
                            }
                        },
                        {
                            "match_phrase": {
                                "triplet_month": {
                                    "query": c['trend_month']
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                "triplet_year": {
                                    "query": c['trend_year']
                                }
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

        qry3 = es.search(index=conf['core_indices']['join_core_mno-classification'], body=qry_triplet_count_join,
                         request_timeout=conf['request_timeout'])

        total_triplet_hits = qry3['hits']['total']

        if qry3['aggregations']['triplet_hash']['value'] > total_triplet_hits:
            total_join_triplets = total_triplet_hits
        else:
            total_join_triplets = qry3['aggregations']['triplet_hash']['value']

        result['non-compliant_triplets'] = total_join_triplets

        if total_mno_triplets != 0:
            nc_triplets_prcnt = round(((result['non-compliant_triplets']/total_mno_triplets) * 100), 2)
        else:
            nc_triplets_prcnt = 0

        result['non-compliant_triplets %'] = nc_triplets_prcnt

        result['compliant_triplets'] = total_mno_triplets - result['non-compliant_triplets']

        result['compliant_triplets %'] = 100 - nc_triplets_prcnt

        return result
