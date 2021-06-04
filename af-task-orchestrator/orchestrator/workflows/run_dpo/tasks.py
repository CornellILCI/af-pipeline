from orchestrator.app import app
from orchestrator.processing.data_gathering.tasks import gather_data

from orchestrator.processing.transformation.tasks import run_dpo

from orchestrator.processing.debug.tasks import debug


@app.task(name="run_dpo_demo")
def run_dpo_demo(params: dict):
    """Call run_dpo"""
    (debug.s(params) | gather_data.s() | run_dpo.s() | debug.s()).apply_async()
