import uuid as uuidlib

import celery_util
from database import Request, db
from dto.requests import AnalysisRequestParameters
from dto.responses import AnalysisRequest
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from pydantic import ValidationError
from sqlalchemy import text

af_requests_bp = Blueprint("af_requests", __name__)


@af_requests_bp.route("/requests", methods=["POST"])
def create_request():
    """Create request object based on body params"""
    content = request.json
    request_data: AnalysisRequestParameters = None
    try:
        request_data = AnalysisRequestParameters(**content)
    except ValidationError as e:
        return jsonify({"errorMsg": str(e)}), 400

    req = Request(
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
            content,
        ),
    )

    return (
        jsonify(
            AnalysisRequest(
                requestId=req.uuid,
                crop=req.crop,
                institute=req.institute,
                analysisType=req.type,
                status=req.status,
                createdOn=req.creation_timestamp,
                modifiedOn=req.modification_timestamp,
            ).dict()
        ),
        201,
    )


@af_requests_bp.route("/requests/<request_uuid>")
def get_request(request_uuid):
    """Get the request object identified by the request_uuid url param."""
    req = Request.query.filter_by(uuid=request_uuid).first()
    if req is None:
        return jsonify({"status": "error", "message": "Request not found"}), 404

    return jsonify(req), 200


@af_requests_bp.route("/models", methods=["GET"])
def get_model():

    page = request.args.get("page")
    pageSize = request.args.get("pageSize")

    params = {
        "engine": request.args.get("engine"),
        "design": request.args.get("design"),
        "trait_level": request.args.get("trait_level"),
        "analysis_objective": request.args.get("analysis_objective"),
        "exp_analysis_pattern": request.args.get("exp_analysis_pattern"),
        "loc_analysis_pattern": request.args.get("loc_analysis_pattern"),
        "trait_pattern": request.args.get("trait_pattern"),
    }

    sql = text(
        "Select id, name, label, description  from af.Property WHERE property.id IN "
        + "(SELECT Property_Config.config_property_id FROM af.Property "
        + "JOIN af.Property_Config on Property_Config.property_id = Property.id "
        + "WHERE Property.code = 'analysis_config' AND Property_Config.property_id != Property_Config.config_property_id)"
    )
    result = db.engine.execute(sql)

    models = []
    for row in result:
        temp = row.values()
        tempMap = {"id": temp[0], "name": temp[1], "label": temp[2], "description": temp[3]}

        # query
        property_meta = db.engine.execute(
            text("select code, value from af.property_meta where property_id = {}".format(str(temp[0])))
        )
        doAppend = True
        for property_row in property_meta:
            if (
                property_row[0] in params
                and params[property_row[0]] is not None
                and params[property_row[0]] != property_row[1]
            ):
                doAppend = False
                break
        if doAppend:
            models.append(tempMap)

    result = {}
    if page is not None and pageSize is not None:
        page = int(page)
        pageSize = int(pageSize)
        pagination = {
            "totalCount": len(models),
            "pageSize": pageSize,
            "totalPages": len(models) / pageSize,
            "currentPage": page,
        }
        result["pagination"] = pagination
        models2 = []
        for i in range(0, pageSize):
            models2.append(models[i + (pageSize * page)])
        models = models2

    result["model"] = models

    return jsonify(result), 200


@af_requests_bp.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@af_requests_bp.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")


@af_requests_bp.route("/test/asreml", methods=["POST"])
def testasreml():
    content = request.json
    # req = Request(uuid=str(uuidlib.uuid4()))
    #db.session.add(req)
    #db.session.commit()
    #content["requestId"] = req.uuid
    celery_util.send_task(process_name="run_asreml", args=(content,))
    return "", 200

