from af.pipeline.job_data import JobData, JobParams
from af.pipeline.asreml.dpo import AsremlProcessData

from collections import defaultdict

import pandas as pd


class AsremlRProcessData(AsremlProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def mesl(self):

        jobs = []

        # read plot for each occurrence and plot measurements for occurrence and trait
        data_by_trait_location = self.__get_data_by_trait_and_location()

        for location_id in self.location_ids:

            for trait_id in self.trait_ids:

                job_data = JobData(job_name=f"{self.analysis_request.requestId}_mesl_{location_id}_{trait_id}")

                trait = self.get_trait_by_id(trait_id)

                analysis_data = data_by_trait_location[(location_id, trait_id)]

                analysis_data = self._format_result_data(analysis_data, trait)

                self._write_job_data(job_data, analysis_data, trait)

                jobs.append(job_data)

        return jobs

    def __get_data_by_trait_and_location(self):

        data_by_trait_location = defaultdict(pd.DataFrame)

        for occurr_id in self.occurrence_ids:

            plots = self.data_reader.get_plots(occurrence_id=occurr_id)

            occurrence = self.data_reader.get_occurrence(occurr_id)

            for trait_id in self.trait_ids:

                plot_measurements = self.data_reader.get_plot_measurements(occurrence_id=occurr_id, trait_id=trait_id)

                _data = plots.merge(plot_measurements, on="plot_id", how="left")

                data_by_trait_location[(str(occurrence.location_id), trait_id)] = data_by_trait_location[
                    (str(occurrence.location_id), trait_id)
                ].append(_data)

        return data_by_trait_location

    def _set_job_params(self, job_data, trait):

        job_params = JobParams(formula=self._get_formuala(trait), residual=self._get_residual())

        job_data.job_params = job_params
