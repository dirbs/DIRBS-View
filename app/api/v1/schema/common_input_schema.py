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


from marshmallow import Schema, fields, validate
from app import conf
from app.api.v1.common.validations import validate_granularity, validate_mno, validate_subsytem, validate_empty_id, \
    validate_config


class CommonSchema(Schema):

    role = fields.String(required=True)
    type = fields.String(required=True)
    granularity = fields.String(required=True, missing='monthly', validate=validate_granularity)
    trend_qty = fields.Integer(required=False, missing=3, validate=validate.Range(min=1, max=conf['max_trend_val'],
                                                                                  error='trend range must be from 1 to '
                                                                                        '{}'.format(conf['max_trend_val'])))
    start_date = fields.Date(required=True, format='%Y-%m-%d')
    end_date = fields.Date(required=True, format='%Y-%m-%d')
    importer_name = fields.String(required=False, missing='user')

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields

    # @validates_schema
    # def validate_end_date(self, data):
    #     print(data['end_date'])
    #     if data['end_date'] < data['start_date']:
    #         raise ValidationError('End_Date does not satisfy date range')


class CommonDpsSchema(Schema):

    role = fields.String(required=True)
    type = fields.String(required=True)
    granularity = fields.String(required=True, missing='monthly', validate=validate_granularity)
    trend_qty = fields.Integer(required=False, missing=3,
                               validate=validate.Range(min=1, max=conf['max_trend_val'],
                                                       error='trend range must be from 1 to {}'
                                                       .format(conf['max_trend_val'])))
    start_date = fields.Date(required=True, format='%Y-%m-%d')
    end_date = fields.Date(required=True, format='%Y-%m-%d')
    importer_name = fields.String(required=False, missing='user')
    mno = fields.String(required=True, validate=validate_mno, missing='all')
    precision_threshold = fields.Integer(required=True, missing=40000)

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class CommonCoreExceptionListSchema03(Schema):
    role = fields.String(required=True)
    type = fields.String(required=True)
    start_date = fields.Date(required=True, format='%Y-%m-%d', missing="2019-01-01")
    end_date = fields.Date(required=True, format='%Y-%m-%d', missing="2019-01-30")
    precision_threshold = fields.Integer(required=True, missing=40000)
    mno = fields.String(required=True, validate=validate_mno, missing='all')

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class CommonCoreSchema(Schema):
    role = fields.String(required=True)
    type = fields.String(required=True)
    chart_id = fields.String(required=True)
    mno = fields.String(required=True, validate=validate_mno, missing='all')
    trend_month = fields.Integer(required=False, validate=validate.Range(1, 12, error='Month must be in range 1 to 12'))
    trend_year = fields.Integer(required=False)
    granularity = fields.String(required=True, missing='monthly', validate=validate_granularity)
    trend_qty = fields.Integer(required=False, missing=3, validate=validate.Range(min=1, max=conf['max_trend_val'],
                                                                                  error='trend range must be from 1 to '
                                                                                  '{}'.format(conf['max_trend_val'])))
    start_date = fields.Date(required=False, format='%Y-%m-%d')
    end_date = fields.Date(required=False, format='%Y-%m-%d')
    importer_name = fields.String(required=False, missing='user')
    precision_threshold = fields.Integer(required=True, missing=40000)

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class SetDashboardSchema(Schema):
    user_id = fields.String(required=True, validate=validate_empty_id)
    subsystem = fields.String(required=True, validate=validate_subsytem)
    config = fields.List(fields.Dict(), required=True, validate=validate_config)

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class GetDashboardSchema(Schema):
    user_id = fields.String(required=True, validate=validate_empty_id)
    subsystem = fields.String(required=True, validate=validate_subsytem)

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields
