import os
import json
import uuid

from flask import Flask, request, jsonify, render_template
from pika import BlockingConnection, ConnectionParameters
from pika.credentials import PlainCredentials

app = Flask(__name__)


def get_connection():
    return (
        BlockingConnection(ConnectionParameters(
            host=os.getenv('MQ_HOST','localhost'),
            port=os.getenv('MQ_PORT','5672'),
            credentials=PlainCredentials(
                username=os.getenv('MQ_USER','admin'),
                password=os.getenv('MQ_PASS','mypass')
            )
        ))
    )


CONSUMER_QUEUE = os.getenv("CONSUMER_QUEUE",'jobs')

#Example API endpoint
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
@app.route('/process', methods=['POST'])
def start_process():
    errorMessage = ''
    content = request.json
    processid = ''

    if content == None: 
        errorMessage = "Empty request. "
    else:
        if "dataSource" not in content:
            errorMessage += "dataSource does not exist in the request. "
        elif (content["dataSource"] != "EBS" and content["dataSource"] != "BRAPI"):
            errorMessage += "dataSource is not 'EBS' or 'BRAPI'. "
        if "dataSourceId" not in content:
            errorMessage += "dataSourceId does not exist in the request. "

        if "dataType" not in content:
            errorMessage += "dataType does not exist in the request. "
        elif (content["dataType"] != "GENOTYPE" and content["dataType"] != "PHENOTYPE"):
            errorMessage += "dataSource is not 'GENOTYPE' or 'PHENOTYPE'. "
        if "token" not in content:
            errorMessage += "token does not exist in the request. "
        if "processName" not in content:
            errorMessage += "processName does not exist in the request. "    




    # TODO we will need further validations on the request

    if(errorMessage == ''):  
        processid = str(uuid.uuid4())  
        message = {
            "dataSource" : content["dataSource"],
            "dataSourceId" : content["dataSourceId"],
            "dataType" : content["dataType"],
            "processName" : content["processName"],
            "token" : content["token"],
            "processId" : processid
        }
        # occurrenceId - optional
        if "occurrenceId" not in content:
            message['occurrenceId'] = content['occurrenceId']
        # traitId - optional
        if "traitId" not in content:
            message['traitId'] = content['traitId']
        # experimentId - optional
        if "experimentId" not in content:
            message['experimentId'] = content['experimentId']

        conn = get_connection()
        channel = conn.channel()
        channel.basic_publish(
            exchange='',
            routing_key=CONSUMER_QUEUE,
            body=json.dumps(message)
        )
        conn.close()

    if(errorMessage != ''):
        return jsonify({"status": "error", "message": errorMessage}), 201
    else:
        return jsonify({"status": "ok", "Process ID" : processid}), 201

@app.route('/test', methods=['GET'])
def test():
    return render_template('loginExample.html')

@app.route('/test/redirect', methods=['GET'])
def testredirect():
    return render_template('loginExample.html')    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
