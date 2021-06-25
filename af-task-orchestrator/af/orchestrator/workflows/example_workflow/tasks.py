# from af.orchestrator.app import app
# from af.orchestrator.processing.calculation.tasks import sample_calculation_task
# from af.orchestrator.processing.data_gathering.tasks import sample_data_gathering_task
# from af.orchestrator.processing.data_upload.tasks import sample_data_upload_task
# from af.orchestrator.processing.workflow.tasks import sample_aggregator_task


# @app.task(name="sample_workflow")
# def sample_workflow(params):
#     """
#     Sample workflow functions that call the tasks
#     """
#     (
#         sample_data_gathering_task.s(params)
#         | sample_aggregator_task.s()
#         | sample_calculation_task.s()
#         | sample_data_upload_task.s()
#     ).apply_async()
