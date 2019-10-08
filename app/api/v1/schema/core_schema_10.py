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


from marshmallow import fields, Schema, pre_dump


class SchemaCore10a(Schema):
    mno = fields.String(attribute='key')
    total_imei = fields.Integer(attribute='doc_count')
    duplicated_imeis = fields.Integer()
    lost_stolen_imeis = fields.Integer()
    malformed_imeis = fields.Integer()
    unregistered_imeis = fields.Integer()
    gsma_invalid_imeis = fields.Integer()

    @pre_dump()
    def extract_values(self, data):
        for val in data['blacklist_reasons']['buckets']:
            if val['key'] == "{\"Duplicate IMEI\"}":
                data['duplicated_imeis'] = val['doc_count']
            elif val['key'] == "{\"IMEI in local stolen list\"}":
                data['lost_stolen_imeis'] = val['doc_count']
            elif val['key'] == "{\"Malformed IMEI\"}":
                data['malformed_imeis'] = val['doc_count']
            elif val['key'] == "{\"Not in registration list\"}":
                data['unregistered_imeis'] = val['doc_count']
            elif val['key'] == "{\"TAC not in gsma\"}":
                data['gsma_invalid_imeis'] = val['doc_count']


class CoreSchema10(Schema):
    results = fields.List(fields.Nested(SchemaCore10a), attribute='buckets')
