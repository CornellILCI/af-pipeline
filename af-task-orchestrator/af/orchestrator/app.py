import os

import jsonpickle.ext.pandas as jsonpickle_pandas
from celery import Celery
from celery.utils.log import get_task_logger

# from event_consumer import message_handler
# from event_consumer.handlers import AMQPRetryConsumerStep


jsonpickle_pandas.register_handlers()

# register('json', jsonpickle.dumps, jsonpickle.loads, content_type='application/json')

BROKER = os.getenv("BROKER")
BACKEND = os.getenv("BACKEND")
CONSUMER_QUEUE = os.getenv("CONSUMER_QUEUE")
LOGGER = get_task_logger(__name__)

INSTALLED_TASKS = ["af.orchestrator.processing.analyze"]


app = Celery("af-worker", broker=BROKER, backend=BACKEND)
app.autodiscover_tasks(INSTALLED_TASKS)
app.conf.update({"accept_content": ["pickle"], "task_serializer": "pickle", "result_serializer": "pickle"})
