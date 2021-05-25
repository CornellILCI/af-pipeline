import uuid as uuidlib

import celery_util
from database import Request, db
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint
from sqlalchemy import text

af_requests_bp = Blueprint("af_requests", __name__)


@af_requests_bp.route("/requests", methods=["POST"])
def create_request():
    """Create request object based on body params

    NOTE:  the parameter currently described here are used in gather_data task

    Required JSON Body parameters:  
    dataSource - either EBS or BRAPI
    dataSourceId - specific data source identifier, ex. EBS1, EBS2, BRAPI1 etc
    dataType - either PHENOTYPE or GENOTYPE
    apiBearerToken - user token for use in API calls
    processName - the name of the analysis workflow job to be executed

    Optional/Context Specific Body Parameters:
    experimentId - Id of the experiment
    occurrenceId - Id of occurence
    traitId - Id of Trait
    """
    content = request.json

    error_messages = []
    if not content:
        error_messages.append("Empty request.")
    else:
        if "dataSource" not in content:
            error_messages.append("dataSource does not exist in the request.")
        elif content["dataSource"] not in ("EBS", "BRAPI"):
            error_messages.append("dataSource is not 'EBS' or 'BRAPI'.")
        if "dataSourceId" not in content:
            error_messages.append("dataSourceId does not exist in the request.")

        if "dataType" not in content:
            error_messages.append("dataType does not exist in the request.")
        elif content["dataType"] not in ("GENOTYPE", "PHENOTYPE"):
            error_messages.append("dataType is not 'GENOTYPE' or 'PHENOTYPE'.")
        if "apiBearerToken" not in content:
            error_messages.append("token does not exist in the request.")
        if "processName" not in content:
            error_messages.append("processName does not exist in the request.")

    # TODO we will need further validations on the request

    if not error_messages:
        print("No errors")
        req = Request(uuid=str(uuidlib.uuid4()))
        db.session.add(req)
        db.session.commit()

        content["processId"] = req.uuid

        celery_util.send_task(process_name=content.get("processName"), args=(content,))

        return jsonify({"status": "ok", "Process ID": req.uuid}), 201

    return jsonify({"status": "error", "message": error_messages}), 400


@af_requests_bp.route("/requests/<request_uuid>")
def get_request(request_uuid):
    """Get the request object identified by the request_uuid url param."""
    req = Request.query.filter_by(uuid=request_uuid).first()
    if req is None:
        return jsonify({"status": "error", "message": "Request not found"}), 404

    return jsonify(req), 200

@af_requests_bp.route("/model", methods=["GET"])
def getModel():
    
    page = request.args.get('page')
    pageSize = request.args.get('pageSize') 

    params = {
        "engine" : request.args.get('engine'),
        "design" : request.args.get('design'),
        "trait_level" : request.args.get('trait_level'),
        "analysis_objective" : request.args.get('analysis_objective'),
        "exp_analysis_pattern" : request.args.get('exp_analysis_pattern'),
        "loc_analysis_pattern" : request.args.get('loc_analysis_pattern'),
        "trait_pattern" : request.args.get('trait_pattern')
    }


    sql = text("Select id, name, label, description  from af.Property WHERE property.id IN "+
        "(SELECT Property_Config.config_property_id FROM af.Property "+
        "JOIN af.Property_Config on Property_Config.property_id = Property.id "+
        "WHERE Property.code = 'analysis_config' AND Property_Config.property_id != Property_Config.config_property_id)")
    result = db.engine.execute(sql)

    models = []
    for row in result:
        temp = row.values()
        tempMap = {"id":temp[0], "name": temp[1], "label": temp[2], "description":temp[3]}

        #query
        property_meta = db.engine.execute(text("select code, value from af.property_meta where property_id = "+str(temp[0])))
        doAppend = True
        for property_row in property_meta:
            if property_row[0] in params and params[property_row[0]] is not None and params[property_row[0]] != property_row[1]:
                doAppend = False
        if(doAppend):
            models.append(tempMap)

    result = {"status": "ok"}
    if(page is not None and pageSize is not None):
        page = int(page)
        pageSize = int(pageSize)
        pagination = {
            "totalCount" : len(models),
            "pageSize" : pageSize,
            "totalPages" : len(models) / pageSize,
            "currentPage" : page
        }
        result['pagination'] = pagination
        models2 = []
        for i in range(0, pageSize):
            models2.append(models[i+(pageSize*page)])
        models = models2
    
    result["model"] = models
    
    return jsonify(result), 200


@af_requests_bp.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@af_requests_bp.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")
