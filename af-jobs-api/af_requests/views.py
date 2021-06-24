from http import HTTPStatus

from af_requests import service, api_models
from flask import request, jsonify

from flask.blueprints import Blueprint
from pydantic import ValidationError

af_requests_bp = Blueprint("af_requests", __name__, url_prefix="/v1/requests")

@af_requests_bp.route("", methods=["POST"])
def post():
    """Create request object based on body params"""
    content = request.json
    request_data: api_models.AnalysisRequestParameters = None
    try:
        request_data = api_models.AnalysisRequestParameters(**content)
    except ValidationError as e:
        return jsonify({"errorMsg": str(e)}), HTTPStatus.BAD_REQUEST

    submitted_request: api_models.AnalysisRequest = service.submit_analysis_request(request_data)

    return jsonify(submitted_request.dict()), HTTPStatus.CREATED

@af_requests_bp.route("", methods=["GET"])
def list():
    """Create request object based on body params"""
    
    query_params = api_models.AnalysisRequestListQueryParameters(**request.args)

    analysis_requests = service.get_analysis_requests(query_params)

    return jsonify(analysis_requests.dict(exclude_none=True)), HTTPStatus.OK
