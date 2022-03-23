from af.pipeline.job_data import JobData
from af.pipeline.asreml.dpo import AsremlProcessData


class AsremlRProcessData(AsremlProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def mesl(self):

        return [JobData()]
