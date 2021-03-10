import os
import ssl

from flask import Flask, request, jsonify
from rabbitmq_pika_flask import RabbitMQ
from pika import BlockingConnection, ConnectionParameters
from pika.connection import SSLOptions
from pika.credentials import PlainCredentials

app = Flask(__name__)

rabbit = RabbitMQ(app, use_ssl=False)

#monkey patch
rabbit.getConnection = lambda: BlockingConnection(ConnectionParameters(
            host=os.getenv('MQ_HOST'),
            port=os.getenv('MQ_PORT'),
            credentials=PlainCredentials(
                username=os.getenv('MQ_USER'),
                password=os.getenv('MQ_PASS')
            )
        ))

CONSUMER_QUEUE = os.getenv("CONSUMER_QUEUE")


@app.route('/jobs', methods=['POST'])
def create_job():
    content = request.json
    rabbit.send(body=jsonify(content), routing_key=CONSUMER_QUEUE)
    return jsonify({"status": "ok"}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



