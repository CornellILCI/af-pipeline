import os
import json

from flask import Flask, request, jsonify, render_template
from pika import BlockingConnection, ConnectionParameters
from pika.credentials import PlainCredentials

app = Flask(__name__)


def get_connection():
    return (
        BlockingConnection(ConnectionParameters(
            host=os.getenv('MQ_HOST'),
            port=os.getenv('MQ_PORT'),
            credentials=PlainCredentials(
                username=os.getenv('MQ_USER'),
                password=os.getenv('MQ_PASS')
            )
        ))
    )


CONSUMER_QUEUE = os.getenv("CONSUMER_QUEUE")

@app.route('/jobs', methods=['POST'])
def create_job():
    content = request.json

    #
    conn = get_connection()
    channel = conn.channel()
    channel.basic_publish(
        exchange='',
        routing_key=CONSUMER_QUEUE,
        body=json.dumps(content)
    )
    conn.close()
    return jsonify({"status": "ok"}), 201


@app.route('/test', methods=['GET'])
def test():
    return render_template('loginExample.html')

@app.route('/test/redirect', methods=['GET'])
def testredirect():
    return render_template('loginExample.html')    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
