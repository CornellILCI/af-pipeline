# from gevent import time
# from orchestrator.app import LOGGER, app
# from orchestrator.base import StatusReportingTask


# @app.task(name="sample_calculation_task", base=StatusReportingTask)
# def sample_calculation_task(params):
#     LOGGER.info("CALCULATION TASK")
#     time.sleep(4)
#     return params  # return for next task
