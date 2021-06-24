from http import HTTPStatus

from af_requests import service, api_models
from flask import request, jsonify

from flask.blueprints import Blueprint
from common.validators import validate_api_request

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

af_requests_bp = Blueprint("af_requests", __name__, url_prefix="/v1/requests")


@af_requests_bp.route("", methods=["POST"])
@validate_api_request(body_model=api_models.AnalysisRequestParameters)
def post():
    """Create request object based on body params"""

    request_data: api_models.AnalysisRequestParameters = api_models.AnalysisRequestParameters(**request.json)

    submitted_request: api_models.AnalysisRequest = service.submit_analysis_request(request_data)

    return jsonify(submitted_request.dict()), HTTPStatus.CREATED


@af_requests_bp.route("", methods=["GET"])
@validate_api_request(query_model=api_models.AnalysisRequestListQueryParameters)
def list():
    """Create request object based on body params"""

    query_params = api_models.AnalysisRequestListQueryParameters(**request.args)

    analysis_requests = service.get_analysis_requests(query_params)

    return jsonify(analysis_requests.dict(exclude_none=True)), HTTPStatus.OK


@af_requests_bp.route("/<request_uuid>")
def get(request_uuid: str):
    """Get the request object identified by the request_uuid url param."""

    try:
        req = service.get_analysis_request_by_id(request_uuid)
        return jsonify(req.dict(exclude_none=True)), HTTPStatus.OK
    except NoResultFound:
        error_response = api_models.ErrorResponse(errorMsg="AnalysisRequest not found")
        return jsonify(error_response.dict()), HTTPStatus.NOT_FOUND
    except MultipleResultsFound:
        error_response = api_models.ErrorResponse(errorMsg="Multiple results found")
        return jsonify(error_response.dict()), HTTPStatus.INTERNAL_SERVER_ERROR
