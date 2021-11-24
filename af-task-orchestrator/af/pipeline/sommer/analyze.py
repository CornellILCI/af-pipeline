from af.pipeline.analysis_request import AnalysisRequest
from af.pipeline.analyze import Analyze
from af.pipeline.job_data import JobData

from .dpo import SommeRProcessData


class SommeRAnalyze(Analyze):

    dpo_cls = SommeRProcessData
    engine_script = "sommer"

    def __init__(self, analysis_request: AnalysisRequest, *args, **kwargs):
        super().__init__(analysis_request=analysis_request, *args, **kwargs)

    
    def get_cmd(self, job_data, analysis_engine=None):
        return ["sommer", job_data.settings_file]

    def process_job_result(self, job_result: JobData, gathered_objects: dict = None):
        pass

    def finalize(self, gathered_objects):
        pass