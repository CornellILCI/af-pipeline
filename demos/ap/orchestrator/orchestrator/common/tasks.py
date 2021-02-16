"""Module for common tasks"""

from orchestrator.app import app
from gevent import time


@app.task
def common_task(params):
    time.sleep(1)    # simulate a task
    return params
