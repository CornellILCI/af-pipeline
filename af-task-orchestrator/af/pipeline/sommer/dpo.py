import csv
import os
import json


from af.pipeline.dpo import ProcessData
from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData

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
        experiment_ids = self.analysis_request.experimentIds
        job_folder = self.get_job_folder(self.__get_job_name())
        data_file = os.path.join(job_folder, f"{self.__get_job_name()}.csv")
        headers_written = False
        with open(data_file, "w") as f:
            writer = csv.writer(f)

            for exp_id in experiment_ids:
                germplasm, plot_data, headers = self.data_reader.get_observation_units_table(occurrence_id=exp_id)
                if not headers_written:
                    writer.writerow(headers)
                    headers_written = True
                for data in plot_data:
                    writer.writerow(data)

        return {"job_name": self.__get_job_name(), "data_file": data_file}

    def __prepare_settings_file(self) -> dict:

        settings_dict = {}
        data_file = self.__prepare_inputfile_csv
        settings_dict["path"] = str(data_file)

        residual = services.get_property(self.db_session, self.analysis_request.configResidualPropertyId)
        settings_dict["rcov"] = residual.statement
        formula = services.get_property(self.db_session, self.analysis_request.configFormulaPropertyId)
        settings_dict["formula"] = formula.statement
        # formula_statement = formula.statement.format(trait_name=trait.abbreviation)
        settings_file = json.dumps(settings_dict)
        loaded_settings = json.loads(settings_file)

        return loaded_settings

    def __prepare_additional_csvs(self) -> dict:

        job_folder = self.get_job_folder(self.__get_job_name())
        var_csv = os.path.join(job_folder, "/var.csv")
        statmodel_csv = os.path.join(job_folder, "/statmodel.csv")
        BVs_csv = os.path.join(job_folder, "/BVs.csv")
        pvs_csv = os.path.join(job_folder, "/pvs.csv")
        Yhat_csv = os.path.join(job_folder, "/Yhat.csv")
        outliers_csv = os.path.join(job_folder, "/outliers.csv")
        out_rds = os.path.join(job_folder, "/out.rds")

        return {
            "job_name": self.__get_job_name(),
            "var": var_csv,
            "statmodel": statmodel_csv,
            "BVs": BVs_csv,
            "pvs": pvs_csv,
            "Yhat": Yhat_csv,
            "outliers": outliers_csv,
            "out": out_rds,
        }

    def run(self):
        """Preprocess input data for SommeR Analysis"""
        return [self.__prepare_inputfile_csv(), self.__prepare_settings_file(), self.__prepare_additional_csvs()]
