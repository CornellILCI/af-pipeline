from orchestrator.app import app
from orchestrator.processing.data_gathering.tasks import gather_data
from orchestrator.processing.debug.tasks import debug


@app.task(name="data_gathering_demo")
def data_gathering_demo(params: dict):
    """Call gather_data"""
    (debug.s(params) | gather_data.s() | debug.s()).apply_async()
