import json
import pathlib
import uuid as uuidlib

import celery_util
from database import Request, db, Property
from dto.requests import AnalysisRequestParameters
from dto.responses import AnalysisRequest
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from pydantic import ValidationError
from sqlalchemy import text
from services.afdb_service import select_property_by_code, select_analysis_configs

af_requests_bp = Blueprint("af_requests", __name__)

#TODO: this will be replaced by the AFDB connector instead of being held in memory
global analysis_type
analysis_type = [
    {"name": "Phenotypic Analysis", "id": str(uuidlib.uuid4())},
    {"name": "Genetic Analysis", "id": str(uuidlib.uuid4())},
    {"name": "Genomic analysis", "id": str(uuidlib.uuid4())}
]

@af_requests_bp.route("/analysis-type", methods=["GET"])
def get_analysis_type():
    #todo read from AFDB
    
    return jsonify({"status": "ok", "response":analysis_type}), 200


@af_requests_bp.route("/analysis-type", methods=["POST"])
def post_analysis_type():
    content = request.json
    if "name" not in content:
        return jsonify({"status": "error", "message": "missing 'name'"}), 400
    if not content["name"]:
        return jsonify({"status": "error", "message": "'name' is empty"}), 400

    id = str(uuidlib.uuid4())
    #TODO add to AFDB instead
    analysis_type.append({"name":content["name"], "id": id})
    
    print(json.dumps(analysis_type))

    return jsonify({"status": "ok", "id": id}), 201

@af_requests_bp.route("/datasources", methods=["GET"])
def get_data_source():
    path = pathlib.Path(__file__).parent.absolute()
    with open(str(path) + "/datasourceconfig.json") as f:
        data = json.load(f)

    return data


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


@af_requests_bp.route("/analysis-configs", methods=["GET"])
def get_analysis_configs():

    page = int(request.args.get("page"))
    if not page or page < 0:
        page = 0
    pageSize = int(request.args.get("pageSize"))
    if not pageSize or pageSize < 1:
        pageSize = 1000

    params = {
        "engine": request.args.get("engine"),
        "design": request.args.get("design"),
        "trait_level": request.args.get("traitLevel"),
        "analysis_objective": request.args.get("analysisObjective"),
        "exp_analysis_pattern": request.args.get("expAnalysisPattern"),
        "loc_analysis_pattern": request.args.get("locAnalysisPattern"),
        "trait_pattern": request.args.get("traitPattern"),
    }

    # sql = text("Select id, name, label, description  from af.Property WHERE property.id IN "+
    #     "(SELECT Property_Config.config_property_id FROM af.Property "+
    #     "JOIN af.Property_Config on Property_Config.property_id = Property.id "+
    #     "WHERE Property.code = 'analysis_config' AND Property_Config.property_id != Property_Config.config_property_id)")
    result = select_property_by_code("analysis_config", 0, 0)
    # result = db.engine.execute(sql)

    models = []
    for row in result:
        tempMap = {
            "propertyCode": row.code,
            "propertyName": row.name,
            "label": row.label,
            #"desription": row.description,
            "type": row.type,
            "createdOn": ("" if not row.creation_timestamp else row.creation_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")),
            "modifiedOn": ("" if not row.modification_timestamp  else row.modification_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")),
            "createdBy": ("" if not row.creator_id else row.creator_id),
            "modifiedBy": ("" if not row.modifier_id else row.modifier_id),
            "propertyId": row.id,
            "statement": ("" if not row.statement else row.statement),
            "isActive": str(not row.is_void),
        }

        # query
        property_meta = db.engine.execute(
            text("select code, value from af.property_meta where property_id = {}".format(str(row.id)))
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

    result["data"] = models

    return jsonify(result), 200


@af_requests_bp.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@af_requests_bp.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")


@af_requests_bp.route("/properties")
def get_properties():
    page = request.args.get("page")
    if not page:
        page = 0
    pageSize = request.args.get("pageSize")
    if not pageSize:
        pageSize = 1000

    propertyRoot = request.args.get("propertyRoot")

    # do a quick check for the property root
    validPropertyRoots = ["objective", "trait_pattern", "exptloc_analysis_pattern"]

    if propertyRoot not in validPropertyRoots:
        return jsonify({"errorMsg": "invalid propertyRoot"}), 400

    result = select_property_by_code(propertyRoot, pageSize, int(pageSize) * int(page))
    props = []
    for row in result:
        
        props.append(
            {
                "propertyCode": row.code,
                "propertyName": row.name,
                "label": row.label,
                #"desription": row.description,
                "type": row.type,
                "createdOn": ("" if not row.creation_timestamp else row.creation_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")),
                "modifiedOn": ("" if not row.modification_timestamp  else row.modification_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")),
                "createdBy": ("" if not row.creator_id else row.creator_id),
                "modifiedBy": ("" if not row.modifier_id else row.modifier_id),
                "propertyId": row.id,
                "statement": ("" if not row.statement else row.statement),
                "isActive": str(not row.is_void),
            }
        )
        
    return jsonify({"metadata": {
        "pagination": {
            "pageSize": pageSize,
            "currentPage": page
            }
        },
        "result":{"data":props}}), 200


@af_requests_bp.route("/analysis-configs/<analysisConfigId>/formulas")
def get_analysis_config_formulas(analysisConfigId):
    page = request.args.get('page')
    if not page or not isinstance(page, (int, long)) or page < 0 : page = 0
    pageSize = request.args.get('pageSize') 
    if not pageSize or not isinstance(pageSize, (int, long)) or pageSize <= 0 : pageSize = 1000

    result = select_analysis_configs(analysisConfigId, pageSize, pageSize*page, "formula");
    ret = []
    for row in result:
        temp = row.values()
        ret.append({
        "propertyId": str(temp[12]),
        "propertyName": temp[13],
        "propertyCode": temp[0],
        "label": temp[1],
        "type": temp[3],
        "createdOn": temp[5],#"2021-06-09T15:06:31.825Z",
        "modifiedOn": temp[6],
        "createdBy": temp[7],
        "modifiedBy": temp[8],
        "isActive": not temp[9],
        "statement": temp[11],
        "description": temp[2]
        })
        
    return jsonify({"metadata": {
        "pagination": {
            "pageSize": pageSize,
            "currentPage": page
            }
        },
        "result":{"data":ret}}), 200


@af_requests_bp.route("/analysis-configs/<analysisConfigId>/residuals")
def get_analysis_config_residuals(analysisConfigId):
    page = request.args.get('page')
    if not page or not isinstance(page, (int, long)) or page < 0 : page = 0
    pageSize = request.args.get('pageSize') 
    if not pageSize or not isinstance(pageSize, (int, long)) or pageSize <= 0 : pageSize = 1000

    result = select_analysis_configs(analysisConfigId, pageSize, pageSize*page, "residual");
    ret = []
    for row in result:
        temp = row.values()
        ret.append({
        "propertyId": str(temp[12]),
        "propertyName": temp[13],
        "propertyCode": temp[0],
        "label": temp[1],
        "type": temp[3],
        "createdOn": temp[5],#"2021-06-09T15:06:31.825Z",
        "modifiedOn": temp[6],
        "createdBy": temp[7],
        "modifiedBy": temp[8],
        "isActive": not temp[9],
        "statement": temp[11],
        "description": temp[2]
        })
        
        

    return jsonify({"metadata": {
        "pagination": {
            "pageSize": pageSize,
            "currentPage": page
            }
        },
        "result":{"data":ret}}), 200

@af_requests_bp.route("/test/asreml", methods=["POST"])
def testasreml():
    content = request.json
    # req = Request(uuid=str(uuidlib.uuid4()))
    #db.session.add(req)
    #db.session.commit()
    #content["requestId"] = req.uuid
    celery_util.send_task(process_name="run_asreml", args=(content,))
    return "", 200

