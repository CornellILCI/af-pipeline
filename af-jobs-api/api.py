import datetime
import os
import uuid as uuidlib
from dataclasses import dataclass

from celery import Celery
from flask import Flask, jsonify, render_template, request
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

BROKER = os.getenv("BROKER")

celery_app = Celery("af-tasks", broker=BROKER)
celery_app.conf.update({"task_serializer": "pickle"})


# encoder
class CustomJSONEncoder(JSONEncoder):
    "Add support for serializing timedeltas"

    def default(self, o):
        if type(o) == datetime.timedelta:
            return str(o)
        elif type(o) == datetime.datetime:
            return o.isoformat()
        else:
            return super().default(o)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("AFDB_URL")
app.json_encoder = CustomJSONEncoder
db = SQLAlchemy(app)

# bind db to the engine
db.Model.metadata.schema = "af"
db.Model.metadata.reflect(db.engine)


# models
@dataclass
class Request(db.Model):
    id: int
    uuid: str
    status: str
    tasks: list

    __table__ = db.Model.metadata.tables["af.request"]

    # TODO add the other columns here
    tasks = db.relationship("Task", backref="request", foreign_keys="Task.request_id")


@dataclass
class Task(db.Model):
    id: int
    name: str
    time_start: datetime.datetime
    time_end: datetime.datetime
    status: str
    err_msg: str
    processor: str
    request_id: int

    __table__ = db.Model.metadata.tables["af.task"]


# TODO:  this does the same as /process but uses db
@app.route("/requests", methods=["POST"])
def create_request():
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
            error_messages.apeend("dataSource is not 'GENOTYPE' or 'PHENOTYPE'.")
        if "apiBearerToken" not in content:
            error_messages.append("token does not exist in the request.")
        if "processName" not in content:
            error_messages.append("processName does not exist in the request.")

    # TODO we will need further validations on the request

    if not error_messages:
        req = Request(uuid=str(uuidlib.uuid4()))
        db.session.add(req)
        db.session.commit()

        content["processId"] = req.uuid

        celery_app.send_task(content.get("processName"), args=(content,))

        return jsonify({"status": "ok", "Process ID": req.uuid}), 201

    return jsonify({"status": "error", "message": error_messages}), 400


@app.route("/requests/<request_uuid>")
def get_request(request_uuid):
    req = Request.query.filter_by(uuid=request_uuid).first()
    if req is None:
        return jsonify({"status": "error", "message": "Request not found"}), 404

    return jsonify(req), 200


# Inputs
# experimentId - optional
# dataSource - required EBS or BRAPI
# dataSourceId - example EBS1 EBS2 BRAPI1
# dataType - PHENOTYPE or GENOTYPE
# occurrenceId - optional
# traitId - optional
# token -
# processName - required

# Returns
# jobId
@app.route("/process", methods=["POST"])
def start_process():
    content = request.json

    processid = ""
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
            error_messages.apeend("dataSource is not 'GENOTYPE' or 'PHENOTYPE'.")
        if "apiBearerToken" not in content:
            error_messages.append("token does not exist in the request.")
        if "processName" not in content:
            error_messages.append("processName does not exist in the request.")

    # TODO we will need further validations on the request
    if not error_messages:
        processid = str(uuidlib.uuid4())
        content["processId"] = processid

        celery_app.send_task(content.get("processName"), args=(content,))

        return jsonify({"status": "ok", "Process ID": processid}), 201

    return jsonify({"status": "error", "message": error_messages}), 400

@app.route("/model", methods=["GET"])
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

@app.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@app.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")


# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")
