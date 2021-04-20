from orchestrator.app import app
from orchestrator.processing.calculation.tasks import sample_calculation_task
from orchestrator.processing.data_gathering.tasks import sample_data_gathering_task
from orchestrator.processing.data_upload.tasks import sample_data_upload_task
from orchestrator.processing.workflow.tasks import sample_aggregator_task


@app.task(name="sample_route")
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
