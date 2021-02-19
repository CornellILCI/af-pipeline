from flask import Flask
import redis
import pika
import os

# setup redis for storage
REDIS_URL = os.getenv('REDIS_URL')

redis_conn = redis.Redis(url=REDIS_URL)
pika 

app = Flask(__name__)


