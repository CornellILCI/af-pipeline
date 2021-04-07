from gevent import time
from orchestrator.app import LOGGER, app
from orchestrator.base import FailureReportingTask, ResultReportingTask
from orchestrator.registry import register
from orchestrator.tasks.calculation.tasks import sample_calculation_task
from orchestrator.tasks.data_gathering.tasks import sample_data_gathering_task
from orchestrator.tasks.data_upload.tasks import sample_data_upload_task
from orchestrator.tasks.workflow.tasks import sample_aggregator_task


def sample_route(params):
    """
    Sample workflow functions that call the tasks
    """
    (
        sample_data_gathering_task.s(params)
        | sample_aggregator_task.s()
        | sample_calculation_task.s()
        | sample_data_upload_task.s()
    ).apply_async()


# this should be called on import
register("sample_route", sample_route)
