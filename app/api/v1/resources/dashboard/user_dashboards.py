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
from app.api.v1.common.elasticsearch_dsl_queries import qry_user_dashboard


class SetDashboard:

    @staticmethod
    def create_dashboard(kwargs):

        qry_dsl = qry_user_dashboard(kwargs['user_id'], kwargs['subsystem'])
        dashboard_config = {"user_id": kwargs['user_id'], "subsystem": kwargs['subsystem'], "config": kwargs['config']}

        qry = es.search(index=conf['user_index'], body=qry_dsl, request_timeout=conf['request_timeout'])

        if qry['hits']['total'] == 0:
            es.index(index=conf['user_index'], doc_type="doc", body=dashboard_config)
            return "{}'s Dashboard-configuration added successfully".format(kwargs['user_id'])

        elif qry['hits']['total'] >= 1:
            last_val = len(qry['hits']['hits']) - 1
            doc_id = qry['hits']['hits'][last_val]['_id']
            es.index(index=conf['user_index'], doc_type="doc", id=doc_id, body=dashboard_config)
            return "{}'s Dashboard-configuration updated successfully".format(kwargs['user_id'])


class GetDashboard:

    @staticmethod
    def fetch_dashboard(kwargs):

        qry_dsl = qry_user_dashboard(kwargs['user_id'], kwargs['subsystem'])

        qry = es.search(index=conf['user_index'], body=qry_dsl, request_timeout=conf['request_timeout'])

        if qry['hits']['total'] == 0:
            return 0
        else:
            last_val = len(qry['hits']['hits']) - 1
            return qry['hits']['hits'][last_val]['_source']['config']
