from orchestrator.processing.data_gathering.tasks import gather_data
from orchestrator.processing.debug.tasks import debug
from orchestrator.registry import register


def data_gathering_demo(params: dict):
    """Call gather_data"""
    (debug.s(params) | gather_data.s() | debug.s()).apply_async()


register("data_gathering_demo", data_gathering_demo)
