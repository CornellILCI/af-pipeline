import os
import uuid
import json

from celery import Celery
from flask import Flask, jsonify, render_template, request

BROKER = os.getenv("BROKER")

celery_app = Celery("af-tasks", broker=BROKER)
celery_app.conf.update({"task_serializer": "pickle"})

app = Flask(__name__)

#TODO: this will be replaced by the AFDB connector instead of being held in memory
global analysis_type
analysis_type = [
    {"name": "Phenotypic Analysis", "id": str(uuid.uuid4())},
    {"name": "Genetic Analysis", "id": str(uuid.uuid4())},
    {"name": "Genomic analysis", "id": str(uuid.uuid4())}
]


# Example API endpoint
# @app.route('/jobs', methods=['POST'])
# def create_job():
#     content = request.json

#     #
#     conn = get_connection()
#     channel = conn.channel()
#     channel.basic_publish(
#         exchange='',
#         body=json.dumps(content)
#     )
#     conn.close()
#     return jsonify({"status": "ok"}), 201


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
        processid = str(uuid.uuid4())
        content["processId"] = processid

        celery_app.send_task(content.get("processName"), args=(content,))

        return jsonify({"status": "ok", "Process ID": processid}), 201

    return jsonify({"status": "error", "message": error_messages}), 400

@app.route("/analysis-type", methods=["GET"])
def get_analysis_type():
    #todo read from AFDB
    response = json.dumps(analysis_type)
    return jsonify({"status": "ok", "response":response}), 201


@app.route("/analysis-type", methods=["POST"])
def post_analysis_type():
    content = request.json
    if "name" not in content:
        return jsonify({"status": "error", "message": "missing 'name'"}), 400
    if content["name"] is None:
        return jsonify({"status": "error", "message": "'name' is empty"}), 400

    id = str(uuid.uuid4())
    #TODO add to AFDB instead
    analysis_type.append({"name":content["name"], "id": id})
    
    print(json.dumps(analysis_type))

    return jsonify({"status": "ok", "id": id}), 201

@app.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@app.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")


# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")
