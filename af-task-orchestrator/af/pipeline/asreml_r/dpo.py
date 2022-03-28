from af.pipeline.job_data import JobData
from af.pipeline.asreml.dpo import AsremlProcessData


class AsremlRProcessData(AsremlProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def mesl(self):

        jobs = []

        plot_measurements = None

        for occurr_id in self.occurrence_ids:
            plots = self.data_reader.get_plots(occurrence_id=occurr_id)
            for trait_id in self.trait_ids:
                plot_measurements = self.data_reader.get_plot_measurements(occurrence_id=occurr_id, trait_id=trait_id)


        for trait in self.trait_ids:
            for location in self.location_ids:
                job_data = JobData(job_name=f"{self.analysis_request.requestId}_mesl_{location}_{trait}")
                self._write_job_data(job_data, plot_measurements, trait)
                jobs.append(job_data)

        return jobs

    def _set_job_params(self, job_data, trait):
        pass
