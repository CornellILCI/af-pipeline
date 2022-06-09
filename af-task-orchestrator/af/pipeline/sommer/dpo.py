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

                plot = self.data_reader.get_plots(occurrence_id=occurrence_id)
                plot_measurements = self.data_reader.get_plot_measurements(
                    occurrence_id=occurrence_id, trait_id=trait.traitId
                )

                # input job data
                plot_measurements = plots.merge(plot_measurements, on="observationUnitDbId", how="left")

                plots_and_measurements = self.format_input_data(plots_and_measurements, trait)

                job = JobData()

        return data_file

    def seml(self):
        pass

    def mesl(self):
        raise NotImplementedError

    def meml(self):
        raise NotImplementedError
