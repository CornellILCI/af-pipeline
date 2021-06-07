from orchestrator.app import app
from orchestrator.base import StatusReportingTask


@app.task(name="run_asreml", base=StatusReportingTask)
def run_asreml(params):
    """
    TODO: write down params
    """



    
    
