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


from flask import Blueprint, Response, jsonify
from app.api.v1.resources.lsds.lsds_01_reported_devices_chart import lsds_01_total_reported_devices
from app.api.v1.resources.lsds.lsds_02_incident_types_chart import lsds_02_incident_type
from app.api.v1.resources.lsds.lsds_03_case_status_chart import lsds_03_case_status
from app.api.v1.resources.lsds.lsds_04_top_stolen_brands import lsds_04_top_stolen_brand
from app.api.v1.resources.lsds.lsds_05_top_stolen_models import lsds_05_top_stolen_model
from app.api.v1.resources.lsds.lsds_06_main_counters_of_lsds import LsdsMainCounters
from app.api.v1.resources.drs.registration.drs_01_manufacturing_location import drs_devices_manufacturing_location
from app.api.v1.resources.drs.registration.drs_02_regstrd_num_of_sims import drs_devices_num_of_sims
from app.api.v1.resources.drs.registration.drs_03_regstrd_imeis_approved import drs_registered_imeis_approved
from app.api.v1.resources.drs.registration.drs_04_imei_count_of_statuses import drs_imei_count_of_statues
from app.api.v1.resources.drs.registration.drs_05_top_device_importer import drs_top_device_importers
from app.api.v1.resources.drs.registration.drs_06_single_importer_status import drs_single_importer_status
from app.api.v1.resources.drs.registration.drs_07_registration_input_type import drs_input_type
from app.api.v1.resources.drs.registration.drs_08_os_type import drs_os_type
from app.api.v1.resources.drs.registration.drs_09_device_type import drs_device_type
from app.api.v1.resources.drs.registration.drs_10_rat_type import drs_rat_type
from app.api.v1.resources.drs.registration.drs_11_top_brands import drs_top_brands
from app.api.v1.resources.drs.registration.drs_12_top_models import drs_top_models
from app.api.v1.resources.drs.registration.drs_13_main_counters_of_drs import DrsMainCounters
from app.api.v1.resources.dps.dps_01_top_brands import dps_top_brands
from app.api.v1.resources.dps.dps_02_top_models import dps_top_models
from app.api.v1.resources.dps.dps_03_rat_types import dps_rat_types
from app.api.v1.resources.dps.dps_04a_active_primary_secondary_pairs import dps_active_primary_secondary_pairs
from app.api.v1.resources.dps.dps_04b_deleted_primary_secondary_pairs import dps_deleted_primary_secondary_pairs
from app.api.v1.resources.dps.dps_05_num_of_connections import dps_num_of_connections_msisdns_imsis
from app.api.v1.resources.dps.dps_06_num_of_devices import dps_num_of_devices
from app.api.v1.resources.dps.dps_07_total_created_pairs import dps_total_created_pairs
from app.api.v1.resources.dps.dps_08_total_deleted_pairs import dps_total_deleted_pairs
from app.api.v1.resources.dps.dps_09_total_permanent_pairs import dps_total_permanent_pairs
from app.api.v1.resources.dps.dps_10_unique_pairs_triplets import dps_unique_pairs_triplets
from app.api.v1.resources.dps.dps_11_main_counters_of_dps import dps_nationwide_pairs_triplets
from app.api.v1.resources.core.core_01_num_of_blacklisted_imeis import core_num_of_blacklisted_imeis
from app.api.v1.resources.core.core_02_num_of_exceptionlist_imeis import core_num_of_exceptionlist_imeis
from app.api.v1.resources.core.core_03_num_of_notificationlist_imeis import core_num_of_notificationlist_imeis
from app.api.v1.resources.core.core_04_identifier_counts import core_identifier_counts
from app.api.v1.resources.core.core_05_identifiers_trends import core_identifier_trends
from app.api.v1.resources.core.core_06_reg_list_top_models import core_reglist_top_models
from app.api.v1.resources.core.core_07_reg_list_top_models_detail import core_reglist_top_models_detail
from app.api.v1.resources.core.core_08_registration_status_details import core_registration_status_details
from app.api.v1.resources.core.core_09_stolen_imeis_on_network import stolen_imeis_on_network
from app.api.v1.resources.core.core_10_all_blacklist_reasons_imeis_on_network import all_blacklist_imeis_on_network
from app.api.v1.resources.core.core_11_countrywide_blacklist_violations_in_day_ranges import \
    countrywide_blacklist_violations_day_ranges
from app.api.v1.resources.core.core_12_operator_wise_blacklist_violations_in_day_ranges import \
    operator_wise_blacklist_violations_day_ranges
from app.api.v1.resources.core.core_13_compliance_breakdown import ComplianceBreakdown
from app.api.v1.resources.core.core_14_compliance_breakdown_trend import ComplianceBreakdownTrend
from app.api.v1.resources.core.core_15_conditions_breakdown import ConditionsBreakdown
from app.api.v1.resources.core.core_16_condition_combinations_breakdown import ConditionCombinationsBreakdown
from app.api.v1.resources.core.core_17_main_counters_of_core import CoreMainCounters
from app.api.v1.resources.dashboard.db_01_view_dashboard import dashboard
from app.api.v1.resources.dashboard.user_dashboards import SetDashboard, GetDashboard
from app.api.v1.schema.simple_output_schema import SimpleMainSchema, SimpleDpsSchema
from app.api.v1.schema.single_aggs_output_schema import SnglAggsCommonSchema, CoreSchema15, DrsSchema13
from app.api.v1.schema.double_aggs_output_schema import DblAggsSchema
from app.api.v1.schema.core_schema_02 import CoreSchema02
from app.api.v1.schema.core_schema_03 import CoreSchema03, CoreSchema04, CoreSchema16
from app.api.v1.schema.core_schema_05 import CoreSchema05
from app.api.v1.schema.core_schema_07 import CoreSchema07
from app.api.v1.schema.core_schema_08 import CoreSchema08
from app.api.v1.schema.core_schema_09 import CoreSchema09
from app.api.v1.schema.core_schema_10 import CoreSchema10
from app.api.v1.schema.lsds_schemas import LsdsMainSchema01, LsdsMainSchema02, LsdsMainSchema03, LsdsMainSchema06
from app.api.v1.schema.common_input_schema import CommonSchema, CommonDpsSchema, CommonCoreExceptionListSchema03,\
    CommonCoreSchema, SetDashboardSchema, GetDashboardSchema
from app.api.v1.schema.schema_dps_cardinality import DpsCardinalitySchema
from app.api.v1.common.date_range_defintions import TrendMonthRange
from flask_apispec import use_kwargs
import json
from itertools import combinations
from app import conf


api = Blueprint('v1', __name__.split('.')[0])


@api.app_errorhandler(422)
def validate_error(error):
    """Transform marshmallow validation errors to custom responses to maintain backward-compatibility."""
    return Response(json.dumps(error.exc.messages),
                    status=422, mimetype='application/json')


@api.route('/base', methods=['GET'])
def base_api():
    data = {"message": "DIRBS-VIEW Version 1"}
    return Response(json.dumps(data), status=200, mimetype='application/json')


@api.route('/mno-names', methods=['GET'])
def mno_names():
    mno_details = []
    mnos = {}
    for k, v in conf['MNO_Names'].items():
        mno_details.append(v)
    mnos['MNO_Details'] = mno_details

    return Response(json.dumps(mnos), status=200, mimetype='application/json')


@api.route('/lsds-01-total-reported-devices', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def lsds_01_reported_devices(**kwargs):
    data = lsds_01_total_reported_devices(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema01().dump(data['aggregations']['time_range']).data)


@api.route('/lsds-02-incident-types-chart', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def lsds_02_incident_types(**kwargs):
    data = lsds_02_incident_type(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema02().dump(data['aggregations']['time_range']).data)


@api.route('/lsds-03-case-status-chart', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def lsds_03_case_statuses(**kwargs):
    data = lsds_03_case_status(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/lsds-04-top-stolen-brands', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def lsds_04_top_stolen_brands(**kwargs):
    data = lsds_04_top_stolen_brand(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/lsds-05-top-stolen-models', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def lsds_05_top_stolen_models(**kwargs):
    data = lsds_05_top_stolen_model(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/lsds-06-main-counters', methods=['POST'])
@use_kwargs(CommonCoreExceptionListSchema03().fields_dict, locations=['json'])
def lsds_06_main_counters(**kwargs):
    data = {"lsds_boxes": []}
    total_devices = LsdsMainCounters.total_devices(kwargs)
    total_devices['key'] = "total_reported_devices"
    lost_stolen = LsdsMainCounters.incident_type_case_status(kwargs, 'incident_type.keyword', 2, 'case_id')
    block_pending = LsdsMainCounters.incident_type_case_status(kwargs, 'case_status.keyword', 3, 'case_id')
    for v1 in lost_stolen:
        data['lsds_boxes'].append(v1)
    for v2 in block_pending:
        data['lsds_boxes'].append(v2)
    data['lsds_boxes'].append(total_devices)
    # return data
    return jsonify(LsdsMainSchema06().dump(data).data)


@api.route('/drs-reg-01-manufacturing_location', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_01_manufacturing_location(**kwargs):
    data = drs_devices_manufacturing_location(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/drs-reg-02-num-of-sims', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_02_num_of_sims(**kwargs):
    data = drs_devices_num_of_sims(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/drs-reg-03-registered-imeis-approved', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_03_registered_imeis_approved(**kwargs):
    data = drs_registered_imeis_approved(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SimpleMainSchema().dump(dict(data['aggregations']['time_range'],
                                                    total_count=data['hits']['total'])).data)


@api.route('/drs-reg-04-count-of-statuses', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_04_count_of_statues(**kwargs):
    data = drs_imei_count_of_statues(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                            total_count=data['hits']['total'])).data)


@api.route('/drs-reg-05-top-device-importers', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_05_top_device_importers(**kwargs):
    data = drs_top_device_importers(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SnglAggsCommonSchema().dump(dict(data['aggregations']['aggs_1'],
                                                   total_count=data['hits']['total'])).data)


@api.route('/drs-reg-06-single-importer-status', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_06_single_importer_status(**kwargs):
    data = drs_single_importer_status(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SnglAggsCommonSchema().dump(dict(data['aggregations']['aggs_1'],
                                                   total_count=data['hits']['total'])).data)


@api.route('/drs-reg-07-input-type', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_07_input_type(**kwargs):
    data = drs_input_type(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/drs-reg-08-os-type', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_08_os_type(**kwargs):
    data = drs_os_type(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/drs-reg-09-device-type', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_09_device_type(**kwargs):
    data = drs_device_type(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/drs-reg-10-rat-type', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_09_rat_type(**kwargs):
    data = drs_rat_type(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/drs-reg-11-top-brands', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_11_top_brands(**kwargs):
    data = drs_top_brands(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/drs-reg-12-top-models', methods=['POST'])
@use_kwargs(CommonSchema().fields_dict, locations=['json'])
def drs_reg_12_top_models(**kwargs):
    data = drs_top_models(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/drs-reg-13-main-counters', methods=['POST'])
@use_kwargs(CommonCoreExceptionListSchema03().fields_dict, locations=['json'])
def drs_reg_13_drs_main_counters(**kwargs):

    reg_status = ['Approved', 'Rejected', 'Pending Review']
    data = DrsMainCounters.imeis_status(reg_status, 'registration_status.keyword', 3)

    reg_devices = DrsMainCounters.device_count(kwargs)
    reg_devices['doc_count'] = reg_devices['unique_devices']['value']
    del reg_devices['unique_devices']
    reg_devices['key'] = 'Total Registered Devices'
    data['aggs_1']['buckets'].append(reg_devices)

    device_type = ['Smartphone', 'Feature phone']
    device_data = DrsMainCounters.imeis_status(device_type, 'device_type.keyword', 2)
    for i in range(0, len(device_data['aggs_1']['buckets'])):
        data['aggs_1']['buckets'].append(device_data['aggs_1']['buckets'][i])

    return jsonify(DrsSchema13().dump(data['aggs_1']).data)


@api.route('/dps-01-top-brands', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_01_top_brands(**kwargs):
    data = dps_top_brands(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/dps-02-top-models', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_02_top_models(**kwargs):
    data = dps_top_models(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/dps-03-rat-types', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_03_rat_types(**kwargs):
    data = dps_rat_types(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(LsdsMainSchema03().dump(data['aggregations']['time_range']).data)


@api.route('/dps-04a-active-primary-secondary-pairs', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_04a_active_primary_secondary_pairs(**kwargs):
    data = dps_active_primary_secondary_pairs(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/dps-04b-deleted-primary-secondary-pairs', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_04b_deleted_primary_secondary_pairs(**kwargs):
    data = dps_deleted_primary_secondary_pairs(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                 total_count=data['hits']['total'])).data)


@api.route('/dps-05-num-of-connections', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_05_num_of_connections(**kwargs):
    data = dps_num_of_connections_msisdns_imsis(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DpsCardinalitySchema().dump(dict(data['aggregations']['time_range'],
                                                   total_count=data['hits']['total'])).data)


@api.route('/dps-06-num-of-devices', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_06_num_of_devices(**kwargs):
    data = dps_num_of_devices(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(DpsCardinalitySchema().dump(dict(data['aggregations']['time_range'],
                                                   total_count=data['hits']['total'])).data)


@api.route('/dps-07-total-created-pairs', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_07_total_created_pairs(**kwargs):
    data = dps_total_created_pairs(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SimpleMainSchema().dump(dict(data['aggregations']['time_range'],
                                                    total_count=data['hits']['total'])).data)


@api.route('/dps-08-total-deleted-pairs', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_08_total_deleted_pairs(**kwargs):
    data = dps_total_deleted_pairs(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SimpleMainSchema().dump(dict(data['aggregations']['time_range'],
                                                    total_count=data['hits']['total'])).data)


@api.route('/dps-09-total-permanent-pairs', methods=['POST'])
@use_kwargs(CommonDpsSchema().fields_dict, locations=['json'])
def dps_09_total_permanent_pairs(**kwargs):
    data = dps_total_permanent_pairs(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SimpleMainSchema().dump(dict(data['aggregations']['time_range'],
                                                    total_count=data['hits']['total'])).data)


@api.route('dps-10-unique-pairs-triplets', methods=['POST'])
@use_kwargs(CommonCoreExceptionListSchema03().fields_dict, locations=['json'])
def dps_10_unique_pairs_triplets(**kwargs):
    data = dps_unique_pairs_triplets(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        return jsonify(SimpleDpsSchema().dump(dict(data['aggregations']['MNOs'],
                                              total_count=data['hits']['total'])).data)


@api.route('dps-11-main-counters', methods=['POST'])
@use_kwargs(CommonCoreExceptionListSchema03().fields_dict, locations=['json'])
def dps_11_nationwide_pairs_triplets(**kwargs):
    data = {"dps_boxes": []}
    result = dps_nationwide_pairs_triplets(kwargs)
    if data == 'wrong end_date':
        msg = {"end_date": "[incorrect date range]"}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        for k, v in result['aggregations'].items():
            data['dps_boxes'].append({k: v['value']})

        return data


def identifier_trends_year_range(data, month, year, kwargs):

    for val in month:
        t_data = core_identifier_trends(val, year, kwargs)
        t_data['aggregations']['year'] = year
        t_data['aggregations']['month'] = val
        t_data['aggregations']['x_axis'] = str(year) + '-' + str(val) + '-01'

        data['monthly_results']['buckets'].append(t_data['aggregations'])

    return data


# noinspection PyUnboundLocalVariable,PyDictCreation
@api.route('core-graphs', methods=['POST'])
@use_kwargs(CommonCoreSchema().fields_dict, locations=['json'])
def core_graphs(**kwargs):

    if kwargs['chart_id'] == "core_01":
        data = core_num_of_blacklisted_imeis(kwargs)
        if data == 'wrong end_date':
            msg = {"end_date": "[incorrect date range]"}
            return Response(json.dumps(msg), status=422, mimetype='application/json')
        else:
            return jsonify(SimpleMainSchema().dump(dict(data['aggregations']['time_range'],
                                                        total_count=data['hits']['total'])).data)

    if kwargs['chart_id'] == "core_02":
        data = core_num_of_exceptionlist_imeis(kwargs)
        return jsonify(CoreSchema02().dump(dict(data['aggregations']['MNOs'],
                                                nationwide_imeis=data['hits']['total'])).data)

    if kwargs['chart_id'] == "core_03":
        data = core_num_of_notificationlist_imeis(kwargs)
        if data == 'wrong end_date':
            msg = {"end_date": "[incorrect date range]"}
            return Response(json.dumps(msg), status=422, mimetype='application/json')
        else:
            return jsonify(CoreSchema03().dump(dict(data['aggregations']['MNOs'],
                                                    nationwide_imeis=data['hits']['total'])).data)

    if kwargs['chart_id'] == "core_04":
        data = core_identifier_counts(kwargs)
        return jsonify(CoreSchema04().dump(dict(data['aggregations'],
                                                total_imeis=data['hits']['total'])).data)

    if kwargs['chart_id'] == "core_05":

        m1, m2, months, years = [], [], [], []
        y1 = False

        if kwargs['mno'] == "all":
            kwargs['mno'] = 'nationwide'

        data = {"mno": kwargs['mno'], "monthly_results": {"buckets": []}}
        diff = kwargs['trend_month'] - 6

        if diff == 0:
            months = [1, 2, 3, 4, 5, 6]
            data = identifier_trends_year_range(data, months, kwargs['trend_year'], kwargs)
        elif diff > 0:
            for i in range(diff + 1, kwargs['trend_month'] + 1):
                months.append(i)
            data = identifier_trends_year_range(data, months, kwargs['trend_year'], kwargs)
        elif diff < 0:
            diff = -diff
            diff -= 1

            for year in range(kwargs['trend_year'] - 1, kwargs['trend_year'] + 1):
                if not y1:
                    for i in range(12 - diff, 13):
                        m1.append(i)
                    y1 = True
                    data = identifier_trends_year_range(data, m1, year, kwargs)
                else:
                    for j in range(1, kwargs['trend_month'] + 1):
                        m2.append(j)
                    data = identifier_trends_year_range(data, m2, year, kwargs)

        return jsonify(CoreSchema05().dump(dict(data['monthly_results'], mno=data['mno'])).data)

    if kwargs['chart_id'] == "core_06":
        data = core_reglist_top_models(kwargs)
        if data == 'wrong end_date':
            msg = {"end_date": "[incorrect date range]"}
            return Response(json.dumps(msg), status=422, mimetype='application/json')
        else:
            return jsonify(DblAggsSchema().dump(dict(data['aggregations']['time_range'],
                                                     total_count=data['hits']['total'])).data)

    if kwargs['chart_id'] == "core_07":
        data = core_reglist_top_models_detail(kwargs)
        if data == 'wrong end_date':
            msg = {"end_date": "[incorrect date range]"}
            return Response(json.dumps(msg), status=422, mimetype='application/json')
        else:
            return jsonify(CoreSchema07().dump(dict(data['aggregations']['top_models'],
                                                    total_count=data['hits']['total'])).data)

    if kwargs['chart_id'] == "core_08":
        data = core_registration_status_details(kwargs)
        if data == 'wrong end_date':
            msg = {"end_date": "[incorrect date range]"}
            return Response(json.dumps(msg), status=422, mimetype='application/json')
        else:
            return jsonify(CoreSchema08().dump(data['aggregations']['registration_status']).data)

    if kwargs['chart_id'] == "core_09":
        data = stolen_imeis_on_network(kwargs)
        return jsonify(CoreSchema09().dump(dict(data['aggregations']['MNOs'],
                                                total_imeis=data['hits']['total'])).data)
    if kwargs['chart_id'] == "core_10":
        data = all_blacklist_imeis_on_network(kwargs)
        return jsonify(CoreSchema10().dump(data['aggregations']['MNOs']).data)

    if kwargs['chart_id'] == "core_11":
        result = {"day_ranges": []}
        for i in range(0, 5):
            if i is 0:
                starting_day, ending_day = 5, 10
                data = countrywide_blacklist_violations_day_ranges(starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '5-10', 'x_axis': data['count']})
            elif i is 1:
                starting_day, ending_day = 11, 30
                data = countrywide_blacklist_violations_day_ranges(starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '11-30', 'x_axis': data['count']})
            elif i is 2:
                starting_day, ending_day = 31, 60
                data = countrywide_blacklist_violations_day_ranges(starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '31-60', 'x_axis': data['count']})
            elif i is 3:
                starting_day, ending_day = 61, 90
                data = countrywide_blacklist_violations_day_ranges(starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '61-90', 'x_axis': data['count']})
            elif i is 4:
                starting_day = 91
                data = countrywide_blacklist_violations_day_ranges(starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '90+', 'x_axis': data['count']})

        return Response(json.dumps(result), status=200, mimetype='application/json')

    if kwargs['chart_id'] == "core_12":

        result = {"day_ranges": []}
        for i in range(0, 5):
            if i is 0:
                starting_day, ending_day = 5, 10
                data = operator_wise_blacklist_violations_day_ranges(kwargs['mno'], starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '5-10', 'x_axis': data['count']})
            elif i is 1:
                starting_day, ending_day = 11, 30
                data = operator_wise_blacklist_violations_day_ranges(kwargs['mno'], starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '11-30', 'x_axis': data['count']})
            elif i is 2:
                starting_day, ending_day = 31, 60
                data = operator_wise_blacklist_violations_day_ranges(kwargs['mno'], starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '31-60', 'x_axis': data['count']})
            elif i is 3:
                starting_day, ending_day = 61, 90
                data = operator_wise_blacklist_violations_day_ranges(kwargs['mno'], starting_day, ending_day)
                result['day_ranges'].append({'y_axis': '61-90', 'x_axis': data['count']})
            elif i is 4:
                starting_day = 91
                data = operator_wise_blacklist_violations_day_ranges(kwargs['mno'], starting_day)
                result['day_ranges'].append({'y_axis': '90+', 'x_axis': data['count']})

        return Response(json.dumps(result), status=200, mimetype='application/json')

    if kwargs['chart_id'] == "core_13":
        a = ComplianceBreakdown(kwargs)
        data, s_code = a.imei_breakdown()
        data2 = a.triplet_breakdown()
        data['Compliance_Breakdown']['non-compliant_triplets'] = data2['non-compliant_triplets']
        data['Compliance_Breakdown']['non-compliant_triplets %'] = data2['non-compliant_triplets %']
        data['Compliance_Breakdown']['compliant_triplets'] = data2['compliant_triplets']
        data['Compliance_Breakdown']['compliant_triplets %'] = data2['compliant_triplets %']

        return Response(json.dumps(data), status=s_code, mimetype='application/json')

    if kwargs['chart_id'] == "core_14":
        result = {"monthly_results": []}
        if len(str(kwargs['trend_month'])) < 2:
            kwargs['trend_month'] = "0" + str(kwargs['trend_month'])
        trend_months = TrendMonthRange.range_finder(kwargs['trend_month'], kwargs['trend_year'])
        for v in trend_months:
            year, month = v.split('-', 1)
            trend_date = year + '-' + month + '-01'
            data, s_code = ComplianceBreakdownTrend.imei_breakdown_trend(kwargs, year, month)
            data['Compliance_Breakdown']['x_axis'] = trend_date
            del data['Compliance_Breakdown']['non-compliant_imeis']
            del data['Compliance_Breakdown']['compliant_imeis']
            result['monthly_results'].append(data['Compliance_Breakdown'])

        return Response(json.dumps(result), status=200, mimetype='application/json')

    if kwargs['chart_id'] == "core_15":
        data = ConditionsBreakdown.imei_distribution(kwargs)

        return jsonify(CoreSchema15().dump(data['aggregations']['block_cond']).data)

    if kwargs['chart_id'] == "core_16":

        result = {"conditions": [], "conditions_values": []}
        result['conditions'] = conf['Blocking_conditions']
        for t_cmb in range(1, len(conf['Blocking_conditions']) + 1):
            cmb = combinations(conf['Blocking_conditions'], t_cmb)
            for i in cmb:
                classification_cond = i
                data = ConditionCombinationsBreakdown.combination_breakdown(kwargs, classification_cond)
                data['classification_condition'] = list(i)
                result['conditions_values'].append(data)

        return jsonify(CoreSchema16().dump(result).data)

    if kwargs['chart_id'] == "core_17":

        result = {"core_boxes": []}

        qry_index1 = 'dirbs_core_mno_data'
        total_imeis = CoreMainCounters.core_total_imeis(kwargs, 'last_seen', qry_index1)

        qry_index2 = 'join_core_mno-classification'
        invalid_imeis = CoreMainCounters.core_invalid_imeis('classification_block_date', 'classification_imei',
                                                            qry_index2)

        valid_imeis = total_imeis - invalid_imeis
        blacklist_imeis = CoreMainCounters.total_blacklist_imeis()

        qry_index3 = 'alias_exceptionlist'
        exceptionlist_imeis = CoreMainCounters.core_invalid_imeis('imei_norm', 'imsi', qry_index3)

        qry_index4 = 'alias_notificationlist'
        notificationlist_imeis = CoreMainCounters.core_total_imeis(kwargs, 'imei_norm', qry_index4)

        result['core_boxes'].append({"total_imeis": total_imeis})
        result['core_boxes'].append({"invalid_imeis": invalid_imeis})
        result['core_boxes'].append({"valid_imeis": valid_imeis})
        result['core_boxes'].append({"blacklisted_imeis": blacklist_imeis})
        result['core_boxes'].append({"exceptionlist_imeis": exceptionlist_imeis})
        result['core_boxes'].append({"notificationlist_imeis": notificationlist_imeis})

        return result


@api.route('view-dashboard', methods=['GET'])
def view_dashboard():
    data = dashboard()
    return Response(json.dumps(data), status=200, mimetype='application/json')


@api.route('set-user-dashboard', methods=['POST'])
@use_kwargs(SetDashboardSchema().fields_dict, locations=['json'])
def set_user_dashboard(**kwargs):
    result = SetDashboard.create_dashboard(kwargs)
    data = {"Message": result}
    return Response(json.dumps(data), status=200, mimetype='application/json')


@api.route('get-user-dashboard', methods=['GET'])
@use_kwargs(GetDashboardSchema().fields_dict, locations=['querystring'])
def get_user_dashboard(**kwargs):
    result = GetDashboard.fetch_dashboard(kwargs)
    if result == 0:
        msg = {"Error": "{}'s Dashboard is not set for {}".format(kwargs['user_id'], kwargs['subsystem'])}
        return Response(json.dumps(msg), status=422, mimetype='application/json')
    else:
        msg = {"config": result}
        return Response(json.dumps(msg), status=200, mimetype='application/json')
