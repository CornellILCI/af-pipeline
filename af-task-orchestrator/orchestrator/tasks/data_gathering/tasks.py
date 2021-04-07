# from gevent import time
# from orchestrator.app import LOGGER, app


# @app.task(base=FailureReportingTask)
# def sample_data_gathering_task(params):
#     LOGGER.info("DATA GATHERING TASK")
#     time.sleep(4)
#     return params  # return for next task
