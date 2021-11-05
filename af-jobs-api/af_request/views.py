from http import HTTPStatus

import config
from af_request import api_models, service
from common.api_models import Status
from common.validators import validate_api_request
from common.responses import json_response
from flask import jsonify, request, send_from_directory, make_response
from flask.blueprints import Blueprint
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

af_requests_bp = Blueprint("af_requests", __name__, url_prefix="/v1/requests")


@af_requests_bp.route("", methods=["POST"])
@validate_api_request(body_model=api_models.AnalysisRequestParameters)
def post():
    """Create request object based on body params"""

    request_data = api_models.AnalysisRequestParameters(**request.json)

    submitted_request = service.submit(request_data)

    submitted_request_dto = _map_analsysis_request(submitted_request)

    return json_response(submitted_request_dto, HTTPStatus.CREATED)


@af_requests_bp.route("", methods=["GET"])
@validate_api_request(query_model=api_models.AnalysisRequestListQueryParameters)
def list():
    """Create request object based on body params"""

    query_params = api_models.AnalysisRequestListQueryParameters(**request.args)

    analysis_requests = service.query(query_params)

    # DTOs for api response
    _analysis_requests = []

    for analysis_request in analysis_requests:
        _analysis_requests.append(_map_analsysis_request(analysis_request))

    response = api_models.AnalysisRequestListResponse(
        metadata=api_models.create_metadata(query_params.page, query_params.pageSize),
        result=api_models.AnalysisRequestListResponseResult(data=_analysis_requests),
    )

    return json_response(response, HTTPStatus.OK)


@af_requests_bp.route("/<request_uuid>")
def get(request_uuid: str):
    """Get the request object identified by the request_uuid url param."""

    try:
        req = service.get_by_id(request_uuid)
        req_dto = api_models.AnalysisRequestResponse(result=_map_analsysis_request(req))
        return json_response(req_dto, HTTPStatus.OK)
    except NoResultFound:
        error_response = api_models.ErrorResponse(errorMsg="AnalysisRequest not found")
        return json_response(error_response, HTTPStatus.NOT_FOUND)
    except MultipleResultsFound:
        error_response = api_models.ErrorResponse(errorMsg="Multiple results found")
        return json_response(error_response, HTTPStatus.INTERNAL_SERVER_ERROR)


@af_requests_bp.route("/<request_uuid>/files/result.zip")
def download_result(request_uuid: str):
    """Download file result of analysis request as zip file"""

    request_uuid_without_hyphens = request_uuid.replace("-", "")
    download_name = f"{request_uuid_without_hyphens}.zip"

    return send_from_directory(
        config.get_analysis_request_folder(request_uuid), "result.zip", as_attachment=True, download_name=download_name
    )


def _map_analsysis_request(req):
    """Maps the db result to the Result model."""

    req_dto = api_models.AnalysisRequest(
        requestId=req.uuid,
        crop=req.crop,
        institute=req.institute,
        analysisType=req.type,
        status=req.status,
        createdOn=req.creation_timestamp,
        modifiedOn=req.modification_timestamp,
        requestorId=req.requestor_id,
    )

    if req.analyses is not None and len(req.analyses) == 1:
        req_dto.configFormulaProperty = _map_property(req.analyses[0].formula)
        req_dto.configResidualProperty = _map_property(req.analyses[0].residual)

    if req.status == Status.DONE:
        req_dto.resultDownloadRelativeUrl = config.get_result_download_url(req.uuid)

    return req_dto


def _map_property(_property):

    if _property is None:
        return None

    property_dto = api_models.Property(
        propertyId=_property.id,
        propertyCode=_property.code,
        propertyName=_property.name,
        label=_property.label,
        statement=_property.statement,
        type=_property.type,
        createdOn=_property.creation_timestamp,
        modifiedOn=_property.modification_timestamp,
    )

    return property_dto
