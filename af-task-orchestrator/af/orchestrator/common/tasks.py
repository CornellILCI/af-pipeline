"""Module for common tasks"""

from af.orchestrator.app import app
from gevent import time


@app.task(name="common_task")
def common_task(params):
    time.sleep(1)  # simulate a task
    return params
