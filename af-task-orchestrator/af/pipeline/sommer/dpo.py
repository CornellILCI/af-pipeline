import csv
import json
import os

from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.job_data import JobData
from af.pipeline import data_reader

"""
# !!! where am i getting the db config, line 59ish
"""


class SommeRProcessData(ProcessData):


    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def __get_job_name(self):
        # TODO: put this in ProcessData
        return f"{self.analysis_request.requestId}"

    def sesl(self):
        """Preprocess input data for SommeR Analysis"""

        jobs = []

        for occurrence_id in self.occurrence_ids:

            for req_trait in self.analysis_request.traits:

                trait: data_reader.models.Trait = data_reader.models.Trait(
                    trait_id=req_trait.traitId, trait_name=req_trait.traitName, abbreviation=req_trait.traitName
                )

                # pre process input job data
                plot = self.data_reader.get_plots(occurrence_id=occurrence_id)
                plot_measurements = self.data_reader.get_plot_measurements(
                    occurrence_id=occurrence_id, trait_id=trait.traitId
                )

                plot_measurements = plots.merge(plot_measurements, on="observationUnitDbId", how="left")

                plots_and_measurements = self.format_input_data(plots_and_measurements, trait)
                
                job_name = f"{self.analysis_request.requestId}_{occurrence_id}_{trait.trait_id}" 
                job = JobData(
                    job_name=job_name,
                    trait_name=trait.trait_name,
                    job_result_dir=self.get_job_folder(job_name)
                )

                data_file_path = os.path.join(job_data.job_result_dir, f"{job_data.job_name}.csv")
                
                dpo.ProcessData._set_job_params(self, job_data, trait)

                jobs.append(job_data)

        return jobs

    def seml(self):
        pass

    def mesl(self):
        raise NotImplementedError

    def meml(self):
        raise NotImplementedError
