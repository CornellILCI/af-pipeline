from af.pipeline.job_data import JobData
from af.pipeline.asreml.dpo import AsremlProcessData


class AsremlRProcessData(AsremlProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def mesl(self):

        jobs = []

        for occurr_id in self.occurrence_ids:
            plots = self.data_reader.get_plots(occurrence_id=occurr_id)
            for trait_id in self.trait_ids:
                plot_measurements = self.data_reader.get_plot_measurements()


        for trait in self.trait_ids:
            for location in self.location_ids:
                jobs.append(JobData(job_name=f"{self.analysis_request.requestId}_mesl_{location}_{trait}"))

        return jobs
