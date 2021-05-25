import uuid as uuidlib

import celery_util
from database import Request, db
from flask import jsonify, render_template, request
from flask.blueprints import Blueprint

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


@af_requests_bp.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@af_requests_bp.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")
