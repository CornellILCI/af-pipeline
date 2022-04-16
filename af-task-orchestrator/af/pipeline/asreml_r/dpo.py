import collections

import pandas as pd
from af.pipeline.asreml.dpo import AsremlProcessData
from af.pipeline.job_data import JobData, JobParams


class AsremlRProcessData(AsremlProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def mesl(self):

        jobs = []

        data_by_location_trait = collections.defaultdict(pd.DataFrame)
        metadata_by_location_trait = collections.defaultdict(pd.DataFrame)

        for data, metadata, occurrence, trait in self.__get_analysis_data():

            location_trait = (str(occurrence.location_id), str(trait.trait_id))

            data_by_location_trait[location_trait] = data_by_location_trait[location_trait].append(data)
            metadata_by_location_trait[location_trait] = metadata_by_location_trait[location_trait].append(metadata)

        for location_id in self.location_ids:

            for trait_id in self.trait_ids:

                job_name = self.__get_mesl_job_name(location_id, trait_id)
                data = data_by_location_trait[(location_id, trait_id)]
                metadata = metadata_by_location_trait[(location_id, trait_id)]

                jobs.append(self.__generate_job_object(job_name, data, metadata, trait_id))

        return jobs

    def meml(self):

        jobs = []

        data_by_trait = collections.defaultdict(pd.DataFrame)
        metadata_by_trait = collections.defaultdict(pd.DataFrame)

        for data, metadata, occurrence, trait in self.__get_analysis_data():
            data_by_trait[str(trait.trait_id)] = data_by_trait[str(trait.trait_id)].append(data)
            metadata_by_trait[str(trait.trait_id)] = metadata_by_trait[str(trait.trait_id)].append(metadata)

        for trait_id in self.trait_ids:

            job_name = self.__get_meml_job_name(trait_id)
            data = data_by_trait[trait_id]
            metadata = metadata_by_trait[trait_id]

            jobs.append(self.__generate_job_object(job_name, data, metadata, trait_id))

        return jobs

    def __generate_job_object(self, job_name, data, metadata, trait_id):

        job = JobData(job_name=job_name)

        job.metadata_file = self._save_metadata(job_name, metadata)

        trait = self.get_trait_by_id(trait_id)

        data = self._format_result_data(data, trait)

        self._write_job_data(job, data, trait)

        return job

    def __get_analysis_data(self):

        for occurr_id in self.occurrence_ids:

            plots = self.data_reader.get_plots(occurrence_id=occurr_id)

            occurrence = self.data_reader.get_occurrence(occurr_id)

            for trait_id in self.trait_ids:

                job_name = self.__get_mesl_job_name(occurrence.location_id, trait_id)

                trait = self.get_trait_by_id(trait_id)
                metadata = self._generate_metadata(plots, occurrence, trait)

                plot_measurements = self.data_reader.get_plot_measurements(occurrence_id=occurr_id, trait_id=trait_id)

                data = plots.merge(plot_measurements, on="plot_id", how="left")

                yield data, metadata, occurrence, trait

    def __get_mesl_job_name(self, location_id, trait_id):
        return f"{self.analysis_request.requestId}_mesl_{location_id}_{trait_id}"

    def __get_meml_job_name(self, trait_id):
        return f"{self.analysis_request.requestId}_meml_{trait_id}"

    def _set_job_params(self, job_data, trait):

        job_params = JobParams(formula=self._get_formula(trait), residual=self._get_residual(), predictions=[])

        predictions = self._get_predictions()

        job_params.predictions = [prediction.statement for prediction in predictions]

        job_data.job_params = job_params
