from af.orchestrator.app import app
from af.orchestrator.processing.data_gathering.tasks import gather_data
from af.orchestrator.processing.debug.tasks import debug, debug_result


@app.task(name="data_gathering_demo")
def data_gathering_demo(params: dict):
    """Call gather_data"""
    (debug.s(params) | gather_data.s() | debug.s() | debug_result.s()).apply_async()
