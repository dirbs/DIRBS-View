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


from marshmallow import Schema, fields, post_dump, pre_dump


class LastSchema03(Schema):
    value = fields.Integer()


class SchemaCore03(Schema):

    mno = fields.String(attribute='key')
    total_imeis = fields.String(attribute='doc_count')
    unique_imeis = fields.List(fields.Nested(LastSchema03))
    unique_imsis = fields.List(fields.Nested(LastSchema03))
    unique_msisdns = fields.List(fields.Nested(LastSchema03))
    imei_imsi_pairs = fields.List(fields.Nested(LastSchema03))
    imsi_msisdn_pairs = fields.List(fields.Nested(LastSchema03))
    imei_msisdn_pairs = fields.List(fields.Nested(LastSchema03))
    imei_imsi_msisdn_triplets = fields.List(fields.Nested(LastSchema03))

    @post_dump(pass_many=False)
    def extract_values(self, data):
        data['unique_imeis'] = data['unique_imeis'][0]['value']
        data['unique_imsis'] = data['unique_imsis'][0]['value']
        data['unique_msisdns'] = data['unique_msisdns'][0]['value']
        data['imei_imsi_pairs'] = data['imei_imsi_pairs'][0]['value']
        data['imei_msisdn_pairs'] = data['imei_msisdn_pairs'][0]['value']
        data['imsi_msisdn_pairs'] = data['imsi_msisdn_pairs'][0]['value']
        data['imei_imsi_msisdn_triplets'] = data['imei_imsi_msisdn_triplets'][0]['value']


class CoreSchema03(Schema):
    nationwide_imeis = fields.Integer(required=False)
    segregated_result = fields.List(fields.Nested(SchemaCore03), attribute='buckets')


class CoreSchema04(Schema):
    total_imeis = fields.Integer(required=False)
    unique_imeis = fields.List(fields.Nested(LastSchema03))
    unique_imsis = fields.List(fields.Nested(LastSchema03))
    unique_msisdns = fields.List(fields.Nested(LastSchema03))
    imei_imsi_pairs = fields.List(fields.Nested(LastSchema03))
    imei_msisdn_pairs = fields.List(fields.Nested(LastSchema03))
    imsi_msisdn_pairs = fields.List(fields.Nested(LastSchema03))
    imei_imsi_msisdn_triplets = fields.List(fields.Nested(LastSchema03))

    @post_dump(pass_many=False)
    def extract_values(self, data):
        data['unique_imeis'] = data['unique_imeis'][0]['value']
        data['unique_imsis'] = data['unique_imsis'][0]['value']
        data['unique_msisdns'] = data['unique_msisdns'][0]['value']
        data['imei_imsi_pairs'] = data['imei_imsi_pairs'][0]['value']
        data['imei_msisdn_pairs'] = data['imei_msisdn_pairs'][0]['value']
        data['imsi_msisdn_pairs'] = data['imsi_msisdn_pairs'][0]['value']
        data['imei_imsi_msisdn_triplets'] = data['imei_imsi_msisdn_triplets'][0]['value']


class SchemaCore16(Schema):
    classification_condition = fields.List(fields.String())
    unique_imeis = fields.Integer()
    imei_imsi_pairs = fields.Integer()
    triplets = fields.Integer()

    @pre_dump(pass_many=False)
    def extract_values(self, data):
        data['classification_condition'] = data['classification_condition']
        data['unique_imeis'] = data['unique_imeis']['value']
        data['imei_imsi_pairs'] = data['imei_imsi_pairs']['value']
        data['triplets'] = data['triplets']['value']


class CoreSchema16(Schema):
    conditions = fields.List(fields.String())
    results = fields.List(fields.Nested(SchemaCore16), attribute='conditions_values')
