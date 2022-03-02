import json
import math
import pathlib
import uuid as uuidlib

import celery_util
from database import Property, db
from dto.requests import AnalysisRequestParameters
from dto.responses import AnalysisRequest
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from pydantic import ValidationError
from services.afdb_service import (
    count_analysis_configs,
    count_property_by_code,
    select_analysis_configs,
    select_property_by_code,
)
from sqlalchemy import text

af_apis = Blueprint("af", __name__, url_prefix="/v1")

# TODO: this will be replaced by the AFDB connector instead of being held in memory
global analysis_type
analysis_type = [
    {"name": "Phenotypic Analysis", "id": str(uuidlib.uuid4())},
    {"name": "Genetic Analysis", "id": str(uuidlib.uuid4())},
    {"name": "Genomic analysis", "id": str(uuidlib.uuid4())},
]


@af_apis.route("/analysis-type", methods=["GET"])
def get_analysis_type():
    # todo read from AFDB

    return jsonify({"status": "ok", "response": analysis_type}), 200


@af_apis.route("/analysis-type", methods=["POST"])
def post_analysis_type():
    content = request.json
    if "name" not in content:
        return jsonify({"status": "error", "message": "missing 'name'"}), 400
    if not content["name"]:
        return jsonify({"status": "error", "message": "'name' is empty"}), 400

    id = str(uuidlib.uuid4())
    # TODO add to AFDB instead
    analysis_type.append({"name": content["name"], "id": id})

    print(json.dumps(analysis_type))

    return jsonify({"status": "ok", "id": id}), 201


@af_apis.route("/datasources", methods=["GET"])
def get_data_source():
    path = pathlib.Path(__file__).parent.absolute()
    with open(str(path) + "/datasourceconfig.json") as f:
        data = json.load(f)

    return data


@af_apis.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@af_apis.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")


@af_apis.route("/properties")
def get_properties():
    page = request.args.get("page", 0)
    if not page:
        page = 0
    pageSize = request.args.get("pageSize", 1000)
    if not pageSize:
        pageSize = 1000

    propertyRoot = request.args.get("propertyRoot")

    # do a quick check for the property root
    validPropertyRoots = ["objective", "trait_pattern", "exptloc_analysis_pattern"]

    if propertyRoot not in validPropertyRoots:
        return jsonify({"errorMsg": "invalid propertyRoot"}), 400

    result = select_property_by_code(propertyRoot, pageSize, int(pageSize) * int(page))
    count = count_property_by_code(propertyRoot)

    props = []
    for row in result:

        props.append(
            {
                "propertyCode": row.code,
                "propertyName": row.name,
                "label": row.label,
                # "desription": row.description,
                "type": row.type,
                "createdOn": (
                    "" if not row.creation_timestamp else row.creation_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
                ),
                "modifiedOn": (
                    "" if not row.modification_timestamp else row.modification_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
                ),
                "createdBy": ("" if not row.creator_id else row.creator_id),
                "modifiedBy": ("" if not row.modifier_id else row.modifier_id),
                "propertyId": row.id,
                "statement": ("" if not row.statement else row.statement),
                "isActive": str(not row.is_void),
            }
        )

    return (
        jsonify(
            {
                "metadata": {
                    "pagination": {
                        "pageSize": pageSize,
                        "currentPage": page,
                        "totalCount": count,
                        "totalPages": math.ceil(count / int(pageSize)),
                    }
                },
                "result": {"data": props},
            }
        ),
        200,
    )


@af_apis.route("/analysis-configs/<analysisConfigId>/formula")
def get_analysis_config_formulas():
    try:
        page = int(request.args.get("page", 0))
    except ValueError:
        page = 0
    if not page or not isinstance(page, int) or page < 0:
        page = 0

    try:
        pageSize = int(request.args.get("pageSize", 1000))
    except ValueError:
        pageSize = 1000

    page = request.args.get("page")
    if not page or not isinstance(page, int) or page < 0:
        page = 0
    pageSize = request.args.get("pageSize")
    if not pageSize or not isinstance(pageSize, int) or pageSize <= 0:
        pageSize = 1000

    result, count = service.get_formulas(analysisConfigId)

    ret = []
    for row in result:
        ret.append(row)

    return (
        jsonify(
            {
                "metadata": {
                    "pagination": {
                        "pageSize": pageSize,
                        "currentPage": page,
                        "totalCount": count,
                        "totalPages": math.ceil(count / pageSize),
                    }
                },
                "result": {"data": ret},
            }
        ),
        200,
    )


@af_apis.route("/analysis-configs/<analysisConfigId>/residuals")
def get_analysis_config_residuals(analysisConfigId):
    try:
        page = int(request.args.get("page", 0))
    except ValueError:
        page = 0
    if not page or not isinstance(page, int) or page < 0:
        page = 0

    try:
        pageSize = int(request.args.get("pageSize", 1000))
    except ValueError:
        pageSize = 1000

    if not pageSize or not isinstance(pageSize, int) or pageSize <= 0:
        pageSize = 1000

    result = select_analysis_configs(analysisConfigId, pageSize, pageSize * page, "residual")
    count = count_analysis_configs(analysisConfigId, "residual")

    ret = []
    for row in result:
        temp = row.values()
        ret.append(
            {
                "propertyId": str(temp[12]),
                "propertyName": temp[13],
                "propertyCode": temp[0],
                "label": temp[1],
                "type": temp[3],
                "createdOn": temp[5],  # "2021-06-09T15:06:31.825Z",
                "modifiedOn": temp[6],
                "createdBy": temp[7],
                "modifiedBy": temp[8],
                "isActive": not temp[9],
                "statement": temp[11],
                "description": temp[2],
            }
        )

    return (
        jsonify(
            {
                "metadata": {
                    "pagination": {
                        "pageSize": pageSize,
                        "currentPage": page,
                        "totalCount": count,
                        "totalPages": math.ceil(count / pageSize),
                    }
                },
                "result": {"data": ret},
            }
        ),
        200,
    )


@af_apis.route("/test/asreml", methods=["POST"])
def testasreml():
    content = request.json
    # req = Request(uuid=str(uuidlib.uuid4()))
    # db.session.add(req)
    # db.session.commit()
    # content["requestId"] = req.uuid
    celery_util.send_task(process_name="run_asreml", args=(content,), queue="ASREML", routing_key="ASREML")
    return "", 200
