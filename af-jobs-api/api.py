import os
import uuid
import pathlib
import json

from celery import Celery
from flask import Flask, jsonify, render_template, request

BROKER = os.getenv("BROKER")

celery_app = Celery("af-tasks", broker=BROKER)
celery_app.conf.update({"task_serializer": "pickle"})

app = Flask(__name__)


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

#

@app.route("/datasource", methods=["GET"])
def get_data_source():
    path = pathlib.Path(__file__).parent.absolute()
    with open(str(path)+'/datasourceconfig.json') as f:
        data = json.load(f)

    return data

@app.route("/test", methods=["GET"])
def test():
    return render_template("loginExample.html")


@app.route("/test/redirect", methods=["GET"])
def testredirect():
    return render_template("loginExample.html")


# if __name__ == "__main__":
#     app.run(debug=os.getenv("DEBUG", False), host="0.0.0.0")
