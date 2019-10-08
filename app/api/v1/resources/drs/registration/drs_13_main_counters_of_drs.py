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


class DrsMainCounters:

    def __init__(self, kwargs, reg_status, qry_field, aggs_size):
        self.kwargs = kwargs
        self.reg_status = reg_status
        self.qry_field = qry_field
        self.aggs_size = aggs_size

    @staticmethod
    def imeis_status(reg_status, qry_field, aggs_size):

        qry_dsl = {
            "aggs": {
                "aggs_1": {
                    "terms": {
                        "field": qry_field,
                        "size": aggs_size,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            },
            "size": 0,
            "query": {
                "terms": {
                    qry_field: reg_status
                }
            }
        }

        qry = es.search(index=conf['drs_reg_index'], body=qry_dsl, request_timeout=conf['request_timeout'])

        return qry['aggregations']

    @staticmethod
    def device_count(kwargs):

        qry_dsl = {
            "aggs": {
                "unique_devices": {
                    "cardinality": {
                        "field": "device_id",
                        "precision_threshold": kwargs['precision_threshold']
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

        qry = es.search(index=conf['drs_reg_index'], body=qry_dsl, request_timeout=conf['request_timeout'])

        return qry['aggregations']
