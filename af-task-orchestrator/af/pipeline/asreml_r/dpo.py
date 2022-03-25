from af.pipeline.job_data import JobData
from af.pipeline.asreml.dpo import AsremlProcessData


class AsremlRProcessData(AsremlProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def mesl(self):

        jobs = []

        for trait in self.trait_ids:
            for location in self.location_ids:
                jobs.append(JobData())

        return jobs
