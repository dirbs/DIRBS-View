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


from marshmallow import fields, Schema, pre_dump, post_dump


class SchemaMain(Schema):
    x_axis = fields.String(attribute='key_as_string')
    unique_devices = fields.Integer()

    @pre_dump(pass_many=False)
    def extract_devices2(self, data):
        data['unique_devices'] = data['unique_devices']['value']


class LsdsMainSchema01(Schema):
    results = fields.List(fields.Nested(SchemaMain), attribute='buckets')


class DblAggsSchema02(Schema):
    x_axis = fields.String(attribute='key_as_string')
    y_axis_Stolen_devices = fields.Integer()
    y_axis_Lost_devices = fields.Integer()

    @pre_dump(pass_many=False)
    def extract_2nd_aggs(self, data):
        for k in data:
            if k == 'aggs_2':
                t_data = data[k]['buckets']
                del data[k]['buckets']
        for c in t_data:
            a = 'y_axis_' + c['key'] + '_devices'
            data[a] = c['unique_devices']['value']


class LsdsMainSchema02(Schema):
    results = fields.List(fields.Nested(DblAggsSchema02), attribute='buckets')


class LastSchema(Schema):
    devices = fields.Integer(attribute='value')


class LastSchema03(Schema):
    t_key = fields.String(attribute='key')
    u_devices = fields.List(fields.Nested(LastSchema), attribute='unique_devices')


class SchemaMain03(Schema):
    x_axis = fields.String(attribute='key_as_string')
    aggs_2 = fields.List(fields.Nested(LastSchema03))

    @pre_dump(pass_many=False)
    def extract_aggs(self, data):

        for k in data:
            if k == 'aggs_2':
                data[k] = data[k]['buckets']

    @post_dump(pass_many=False)
    def extract_devices(self, data):
        rslt = data['aggs_2']
        del data['aggs_2']
        for v in rslt:
            a = 'y_axis_' + v['t_key']
            data[a] = v['u_devices'][0]['devices']


class LsdsMainSchema03(Schema):
    results = fields.List(fields.Nested(SchemaMain03), attribute='buckets')


class SchemaMain06(Schema):
    Stolen = fields.Integer()
    Lost = fields.Integer()
    Pending = fields.Integer()
    Blocked = fields.Integer()
    Recovered = fields.Integer()
    total_reported_devices = fields.Integer()

    @pre_dump(pass_many=False)
    def extract_devices(self, data):
        data[data['key']] = data['unique_devices']['value']


class LsdsMainSchema06(Schema):
    lsds_boxes = fields.List(fields.Nested(SchemaMain06), attribute='lsds_boxes')