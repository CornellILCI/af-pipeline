# from gevent import time
# from orchestrator.app import LOGGER, app
# from orchestrator.base import StatusReportingTask


# @app.task(name="sample_aggregator_task", base=StatusReportingTask)
# def sample_aggregator_task(params):
#     LOGGER.info("AGGREGATOR TASK")
#     time.sleep(4)
#     return params  # return for next task
