from orchestrator.app import app
from orchestrator.processing.data_gathering.tasks import gather_data, run dpo
from orchestrator.processing.debug.tasks import debug, debug_result


@app.task(name="run_dpo_demo")
def run_dpo_demo(params: dict):
    """Call run_dpo"""
    (debug.s(params) | gather_data.s() |run_dpo.s() | debug.s() | debug_result.s()).apply_async()
