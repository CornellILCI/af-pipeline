import json
import uuid as uuidlib

import celery_util
from af_requests import api_models
from af_requests import models as db_models
from database import db


def submit_analysis_request(request_data: api_models.AnalysisRequestParameters):
    """Submits analysis request to pipeline."""

    req = db_models.Request(
        uuid=str(uuidlib.uuid4()),
        institute=request_data.institute,
        crop=request_data.crop,
        type=request_data.analysisType,
        status="PENDING",
    )

    db.session.add(req)
    db.session.commit()

    celery_util.send_task(
        process_name="analyze",
        args=(
            req.uuid,
            json.loads(request_data.json()),
        ),
    )

    return _map_analsysis_request(req)


def get_analysis_requests(query_params: api_models.AnalysisRequestListQueryParameters):

    query = db_models.Request.query

    if query_params.requestorId:
        query = query.filter(db_models.Request.requestorId == query_params.requestorId)

    if query_params.crop:
        query = query.filter(db_models.Request.crop == query_params.crop)

    if query_params.institute:
        query = query.filter(db_models.Request.institute == query_params.institute)

    if query_params.status:
        query = query.filter(db_models.Request.status == query_params.status)

    # Get latest requests first
    query = query.order_by(db_models.Request.creation_timestamp.desc())

    # AnalysisRequestListQueryParameters have default page and pageSize
    query = query.limit(query_params.pageSize).offset(query_params.page * query_params.pageSize)

    analysis_requests = query.all()

    # DTOs for api response
    _analysis_requests = []

    for analysis_request in analysis_requests:
        _analysis_requests.append(_map_analsysis_request(analysis_request))

    return api_models.AnalysisRequestListResponse(
        metadata=api_models.create_metadata(query_params.page, query_params.pageSize),
        result=api_models.AnalysisRequestListResponseResult(data=_analysis_requests),
    )


def get_analysis_request_by_id(request_id: str):

    analysis_request = db_models.Request.query.filter(db_models.Request.uuid == request_id).one()

    return api_models.AnalysisRequestResponse(result=_map_analsysis_request(analysis_request))


def _map_analsysis_request(req):
    return api_models.AnalysisRequest(
        requestId=req.uuid,
        crop=req.crop,
        institute=req.institute,
        analysisType=req.type,
        status=req.status,
        createdOn=req.creation_timestamp,
        modifiedOn=req.modification_timestamp,
    )
