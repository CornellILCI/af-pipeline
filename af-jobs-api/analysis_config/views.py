from http import HTTPStatus

from analysis_config import api_models, service
from common.responses import json_response
from common.validators import validate_api_request
from flask import request
from flask.blueprints import Blueprint
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

analysis_configs_bp = Blueprint("analysis_configs", __name__, url_prefix="/v1/analysis-configs")


@analysis_configs_bp.route("", methods=["GET"])
@validate_api_request(query_model=api_models.AnalysisConfigsListQueryParameters)
def list():
    """Create request object based on body params"""

    request_query_params = api_models.AnalysisConfigsListQueryParameters(**request.args)

    filter_params = request_query_params.as_db_filter_params()

    analysis_configs: list[Property] = service.get_analysis_configs(
        page=request_query_params.page, page_size=request_query_params.pageSize, **filter_params
    )

    # DTOs for api response
    analysis_config_dtos = []

    for analysis_config in analysis_configs:
        analysis_config_dtos.append(api_models.map_property(analysis_config))

    response = api_models.AnalysisConfigListResponse(
        metadata=api_models.create_metadata(request_query_params.page, request_query_params.pageSize),
        result=api_models.AnalysisConfigListResponseResult(data=analysis_config_dtos),
    )

    return json_response(response, HTTPStatus.OK)


@analysis_configs_bp.route("/analysis-configs/<analysisConfigId>/formulas", methods=["GET"])
@validate_api_request(query_model=api_models.AnalysisConfigsListQueryParameters)
def get_formulas(analysisConfigId):
    """Create request object based on body params"""

    request_query_params = api_models.AnalysisConfigsListQueryParameters(**request.args)

    filter_params = request_query_params.as_db_filter_params()

    formulas, count = service.get_formulas(
        analysis_config_id=analysisConfigId,
        page=request_query_params.page,
        page_size=request_query_params.pageSize, **filter_params
    )

    # DTOs for api response
    formula_dtos = []

    for formula in formulas:
        formula_dtos.append(api_models.map_property(formula))

    response = api_models.AnalysisConfigListResponse(
        metadata=api_models.create_metadata(request_query_params.page, request_query_params.pageSize),
        result=api_models.AnalysisConfigListResponseResult(data=formula_dtos),
    )

    return json_response(response, HTTPStatus.OK)
