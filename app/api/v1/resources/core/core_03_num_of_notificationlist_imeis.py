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


def core_num_of_notificationlist_imeis(kwargs):

    if kwargs['start_date'] > kwargs['end_date']:
        return "wrong end_date"

    qry_dsl = {
        "aggs": {
            "MNOs": {
                "terms": {
                    "field": "operator_id.keyword",
                    "size": conf['num_of_mnos'],
                    "order": {
                        "_count": "desc"
                    }
                },
                "aggs": {
                    "unique_imeis": {
                        "cardinality": {
                            "field": "imei_norm.keyword",
                            "precision_threshold": kwargs['precision_threshold']
                        }
                    },
                    "unique_imsis": {
                        "cardinality": {
                            "field": "imsi.keyword",
                            "precision_threshold": kwargs['precision_threshold']
                        }
                    },
                    "unique_msisdns": {
                        "cardinality": {
                            "field": "msisdn.keyword",
                            "precision_threshold": kwargs['precision_threshold']
                        }
                    },
                    "imei_imsi_pairs": {
                        "cardinality": {
                            "script": "doc['imei_norm.keyword'].value + '_' "
                                      "+ doc['imsi.keyword'].value",
                            "precision_threshold": kwargs['precision_threshold']
                        }
                    },
                    "imei_msisdn_pairs": {
                        "cardinality": {
                            "script": "doc['imei_norm.keyword'].value + '_' "
                                      "+ doc['msisdn.keyword'].value",
                            "precision_threshold": kwargs['precision_threshold']
                        }
                    },
                    "imsi_msisdn_pairs": {
                        "cardinality": {
                            "script": "doc['imsi.keyword'].value + '_' "
                                      "+ doc['msisdn.keyword'].value",
                            "precision_threshold": kwargs['precision_threshold']
                        }
                    },
                    "imei_imsi_msisdn_triplets": {
                        "cardinality": {
                            "script": "doc['imei_norm.keyword'].value + '_' "
                                      "+ doc['imsi.keyword'].value + '.' "
                                      "+ doc['msisdn.keyword'].value",
                            "precision_threshold": kwargs['precision_threshold']
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
                        "exists": {
                            "field": "imei_norm.keyword"
                        }
                    },
                    {
                        "exists": {
                            "field": "imsi.keyword"
                        }
                    },
                    {
                        "exists": {
                            "field": "msisdn.keyword"
                        }
                    },
                    {
                        "range": {
                            "block_date": {
                                "gte": kwargs['start_date'],
                                "lte": kwargs['end_date']
                            }
                        }
                    }
                ],
                "filter": [
                    {
                        "match_all": {}
                    }
                ]
            }
        }
    }

    qry = es.search(index=conf['core_indices']['core_notificationlist_index'], body=qry_dsl,
                    request_timeout=conf['request_timeout'])

    return qry
