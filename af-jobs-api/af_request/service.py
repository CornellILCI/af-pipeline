import json
import uuid as uuidlib

import celery_util
from af_request import api_models
from af_request import models as db_models
from database import db


def submit(request_data: api_models.AnalysisRequestParameters):
    """Submits analysis request to pipeline."""

    req = db_models.Request(
        uuid=str(uuidlib.uuid4()),
        institute=request_data.institute,
        crop=request_data.crop,
        type=request_data.analysisType,
        requestor_id=request_data.requestorId,
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

    return req


def query(query_params: api_models.AnalysisRequestListQueryParameters):

    query = db_models.Request.query

    # filter only analysis requests.
    # Requests submitted by other frameworks have non standardized status fields other than what
    # used by af.
    query = query.filter(db_models.Request.type == "ANALYZE")

    if query_params.requestorId:
        query = query.filter(db_models.Request.requestor_id == query_params.requestorId)

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

    return analysis_requests


def get_by_id(request_id: str):

    analysis_request = db_models.Request.query.filter(db_models.Request.uuid == request_id).one()

    return analysis_request
