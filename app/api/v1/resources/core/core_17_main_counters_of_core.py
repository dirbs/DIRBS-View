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


class CoreMainCounters:

    def __init__(self, kwargs, field1, field2, field3, qry_index):
        self.kwargs = kwargs
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.qry_index = qry_index

    @staticmethod
    def core_total_imeis(kwargs, field3, qry_index):

        qry_dsl = {
            "aggs": {
                "unique_imeis": {
                    "cardinality": {
                        "field": "imei_norm.keyword",
                        "precision_threshold": kwargs['precision_threshold']
                    }
                }
            },
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": field3
                            }
                        }
                    ]
                }
            }
        }

        qry = es.search(index=qry_index, body=qry_dsl, request_timeout=conf['request_timeout'])

        return qry['aggregations']['unique_imeis']['value']

    @staticmethod
    def core_invalid_imeis(field1, field2, qry_index):

        qry_dsl = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": field1
                            }
                        },
                        {
                            "exists": {
                                "field": field2
                            }
                        }
                    ]
                }
            }
        }

        qry = es.count(index=qry_index, body=qry_dsl, request_timeout=conf['request_timeout'])

        return qry['count']

    @staticmethod
    def total_blacklist_imeis():
        qry_dsl = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "imei_norm"
                            }
                        }
                    ]
                }
            }
        }

        qry = es.count(index='alias_blacklist', body=qry_dsl, request_timeout=conf['request_timeout'])

        return qry['count']
