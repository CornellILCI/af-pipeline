import json
import os

from celery import Celery
from celery.utils.log import get_task_logger
from event_consumer import message_handler
from event_consumer.handlers import AMQPRetryConsumerStep

from .registry import WORKFLOW_REGISTRY

BROKER = os.getenv("BROKER")
BACKEND = os.getenv("BACKEND")
CONSUMER_QUEUE = os.getenv("CONSUMER_QUEUE")
LOGGER = get_task_logger(__name__)

INSTALLED_WORKFLOWS = [
    "orchestrator.common",
    "orchestrator.workflows.sample_workflow",
    "orchestrator.workflows.sample_workflow_2",
    "orchestrator.processing.calculation",
    "orchestrator.processing.data_gathering",
    "orchestrator.processing.data_upload",
    "orchestrator.processing.workflow",
    "orchestrator.routes.example_route",
    "orchestrator.workflows.data_gathering_demo",
]


@message_handler(CONSUMER_QUEUE)
def process_external_requests(body):
    LOGGER.warning("==================================================================")
    LOGGER.warning(body)
    LOGGER.warning(str(type(body)))
    if isinstance(body, list):
        body = body[1]
    # do some logging here
    else:
        body = json.loads(body)
    func = WORKFLOW_REGISTRY.get(body["jobName"])
    job_id = body.get("jobId")
    if func and job_id:
        LOGGER.info(f"Workflow: {func.__name__} with ID:{job_id} initiated.")  # noqa: FS003
        func(body)
        return

    # else no func registered for workflow requested
    LOGGER.warning("No available workflow func for request %s", json.dumps(body))  # noqa: FS003

    # we can maybe put this in a dead-letter queue
    # TODO for later


app = Celery("ap-worker", broker=BROKER, backend=BACKEND)
app.autodiscover_tasks(INSTALLED_WORKFLOWS)
app.steps["consumer"].add(AMQPRetryConsumerStep)
