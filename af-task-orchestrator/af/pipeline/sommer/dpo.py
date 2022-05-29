import csv
import json
import os

from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.job_data import JobData

"""
# !!! where am i getting the db config, line 59ish
"""


class SommeRProcessData(ProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def __get_job_name(self):
        # TODO: put this in ProcessData
        return f"{self.analysis_request.requestId}"

    def __prepare_inputfile_csv(self) -> dict:

        # there can be multiple experiments
        job_folder = self.get_job_folder(self.__get_job_name())
        data_file = os.path.join(job_folder, f"{self.__get_job_name()}.csv")
        # headers_written = False
        # with open(data_file, "w") as f:
        #     writer = csv.writer(f)

        #     for exp_id in self.experiment_ids:
        #         germplasm, plot_data, headers = self.data_reader.get_plots_from_search(occurrence_id=exp_id, crop=self.analysis_request.crop)
        #         if not headers_written:
        #             writer.writerow(headers)
        #             headers_written = True
        #         for data in plot_data:
        #             writer.writerow(data)

        # NOTE: using a loop here because of the structure of experiments but
        # we assume there is only one experiment in the `experiment_ids``
        for exp_id in self.experiment_ids:
            plot_df = self.data_reader.get_plots_from_search(exp_id=exp_id, crop=self.analysis_request.crop)
            plot_df.to_csv(data_file, index=True)

        return data_file

    def __prepare_Sommer_settings_file(self) -> dict:

        name = self.analysis_request.traits[0].traitName

        settings_dict = {}
        data_file = self.__prepare_inputfile_csv()
        settings_dict["path"] = str(data_file)

        residual = services.get_property(self.db_session, self.analysis_request.configResidualPropertyId)
        formula = services.get_property(self.db_session, self.analysis_request.configFormulaPropertyId)

        # formula_statement = formula.statement.format(trait_name=trait.abbreviation)

        job_folder = self.get_job_folder(self.__get_job_name())
        settings_file = os.path.join(job_folder, "settings.json")
        settings_dict["input_phenotypic_data"] = data_file
        # settings_dict["grm"] = os.path.join(job_folder, "/grm.txt")
        settings_dict["output_var"] = os.path.join(job_folder, "var.csv")
        settings_dict["output_statmodel"] = os.path.join(job_folder, "output_statmodel.csv")
        settings_dict["output_BV"] = os.path.join(job_folder, "BVs.csv")
        settings_dict["output_pred"] = os.path.join(job_folder, "output_pred.csv")
        settings_dict["output_yhat"] = os.path.join(job_folder, "Yhat.csv")
        settings_dict["output_outliers"] = os.path.join(job_folder, "outliers.csv")
        settings_dict["formula"] = str(formula.statement).format(trait_name=name)
        settings_dict["rcov"] = residual.statement
        settings_dict["raw_analysis_out"] = os.path.join(job_folder, "raw_analysis_out.rds")
        settings_dict["trait"] = name
        settings_dict["rep"] = 1

        with open(settings_file, "w") as f:
            json.dump(settings_dict, f)

        job_data = JobData()
        job_data.job_name = self.__get_job_name()
        job_data.job_file = settings_file

        return job_data

    def sesl(self):
        """Preprocess input data for SommeR Analysis"""
        return [self.__prepare_Sommer_settings_file()]

    def seml(self):
        raise NotImplementedError

    def mesl(self):
        raise NotImplementedError

    def meml(self):
        raise NotImplementedError
