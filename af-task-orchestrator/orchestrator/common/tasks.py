"""Module for common tasks"""

from gevent import time
from orchestrator.app import app


@app.task(name="common_task")
def common_task(params):
    time.sleep(1)  # simulate a task
    return params
