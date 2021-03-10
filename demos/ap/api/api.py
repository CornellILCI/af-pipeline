import os

from flask import Flask, request, jsonify
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
    print(jsonify(content))
    #
    conn = get_connection()
    channel = conn.channel()
    channel.basic_publish(
        exchange='',
        routing_key=CONSUMER_QUEUE,
        body=jsonify(content)
    )
    conn.close()
    return jsonify({"status": "ok"}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
