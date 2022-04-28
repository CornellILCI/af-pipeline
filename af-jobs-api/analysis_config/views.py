from http import HTTPStatus

from analysis_config import api_models, service
from common.responses import json_response
from common.validators import validate_api_request
from flask import request
from flask.blueprints import Blueprint
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

analysis_configs_bp = Blueprint("analysis_configs", __name__, url_prefix="/v1/analysis-configs")
analysis_models_bp = Blueprint("analysis_models", __name__, url_prefix="/v1/analysis-models")


@analysis_configs_bp.route("", methods=["GET"])
@validate_api_request(query_model=api_models.AnalysisConfigsListQueryParameters)
def list():
    """Create request object based on body params"""

    request_query_params = api_models.AnalysisConfigsListQueryParameters(**request.args)

    filter_params = request_query_params.as_db_filter_params()

    analysis_configs, total_count = service.get_analysis_configs(
        page=request_query_params.page, page_size=request_query_params.pageSize, **filter_params
    )

    # DTOs for api response
    analysis_config_dtos = []

    for analysis_config in analysis_configs:
        analysis_config_dtos.append(api_models.map_property(analysis_config))

    response = api_models.AnalysisConfigListResponse(
        metadata=api_models.create_metadata(request_query_params.page, request_query_params.pageSize, total_count),
        result=api_models.AnalysisConfigListResponseResult(data=analysis_config_dtos),
    )

    return json_response(response, HTTPStatus.OK)


# @analysis_models_bp.route("", methods=["POST"])
# @validate_api_request(body_model=api_models.AnalysisRequestParameters)
# def post_analysis_config():
#     """Create request object based on body params"""
#     request_query_params = api_models.AnalysisConfigsListQueryParameters(**request.args)

#     filter_params = request_query_params.as_db_filter_params()

#     analysis_configs, total_count = service.get_analysis_configs(
#         page=request_query_params.page, page_size=request_query_params.pageSize, **filter_params
#     )

#     # DTOs for api response
#     analysis_config_dtos = []

#     for analysis_config in analysis_configs:
#         analysis_config_dtos.append(api_models.map_property(analysis_config))

#     response = api_models.AnalysisConfigListResponse(
#         metadata=api_models.create_metadata(request_query_params.page, request_query_params.pageSize, total_count),
#         result=api_models.AnalysisConfigListResponseResult(data=analysis_config_dtos),
#     )

#     return json_response(response, HTTPStatus.OK)

@analysis_models_bp.route("", methods=["POST"])
def post_analysis_config():

    analysis_config_params = api_models.AnalysisConfigCreateObject(**request.args)

    service.create_analysis_config(
        property_code = analysis_config_params.code,
        property_configName = analysis_config_params.configName,
        property_label = analysis_config_params.label,
        property_description = analysis_config_params.description,
        property_design = analysis_config_params.design,
        property_data_type = analysis_config_params.dataType,
        property_creator_id = analysis_config_params.creatorId,
        property_modifier_id = analysis_config_params.modifierId,
        property_tenant_id = analysis_config_params.tenantId,
        property_id = analysis_config_params.id,
        property_statement = analysis_config_params.statement,
        property_meta_version = analysis_config_params.property_meta_version,
        property_meta_date = analysis_config_params.property_meta_date,
        property_meta_author = analysis_config_params.property_meta_author,
        property_meta_email = analysis_config_params.property_meta_email,
        property_meta_organization_code = analysis_config_params.property_meta_organization_code,
        property_meta_engine = analysis_config_params.property_meta_engine,
        property_meta_breeding_program_id = analysis_config_params.property_meta_breeding_program_id,
        property_meta_pipeline_id = analysis_config_params.property_meta_pipeline_id,
        property_meta_stage_id = analysis_config_params.property_meta_stage_id,
        property_meta_design = analysis_config_params.property_meta_design,
        property_meta_trait_level = analysis_config_params.property_meta_trait_level,
        property_meta_analysis_objective = analysis_config_params.property_meta_analysis_objective,
        property_meta_exp_analysis_pattern = analysis_config_params.property_meta_exp_analysis_pattern,
        property_meta_loc_analysis_pattern = analysis_config_params.property_meta_loc_analysis_pattern,
        property_meta_year_analysis_pattern = analysis_config_params.property_meta_year_analysis_pattern,
        property_meta_trait_pattern = analysis_config_params.property_meta_trait_pattern
    )

    response = {}
    return json_response(response, HTTPStatus.OK)