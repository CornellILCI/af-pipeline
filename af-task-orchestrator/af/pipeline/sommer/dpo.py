import csv
import os
import json


from af.pipeline.dpo import ProcessData
from af.pipeline.analysis_request import AnalysisRequest

from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.job_data import JobData
from af.pipeline.data_reader.models import Trait


"""
# !!! where am i getting the db config, line 59ish
"""


class SommeRProcessData(ProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def __get_job_name(self):
        # TODO: put this in ProcessData
        return f"{self.analysis_request.requestId}"

    def __get_traits(self) -> list[Trait]:
        traits = []
        for trait_id in self.trait_ids:
            trait: Trait = self.data_reader.get_trait(trait_id)
            traits.append(trait)
        return traits

    def __prepare_inputfile_csv(self) -> dict:

        # there can be multiple experiments
        job_folder = self.get_job_folder(self.__get_job_name())
        data_file = os.path.join(job_folder, f"{self.__get_job_name()}.csv")
        headers_written = False
        with open(data_file, "w") as f:
            writer = csv.writer(f)

            for exp_id in self.experiment_ids:
                germplasm, plot_data, headers = self.data_reader.get_observation_units_table(occurrence_id=exp_id)
                if not headers_written:
                    writer.writerow(headers)
                    headers_written = True
                for data in plot_data:
                    writer.writerow(data)

        return data_file

    def __prepare_Sommer_settings_file(self) -> dict:

        self.trait_names = []
        # traits: list[Trait] = self.__get_traits()
        for trait in self.analysis_request.traits:
            self.trait_names.append(trait.traitName)
        # print(f"\n\nself.analysis_request.traits={self.analysis_request.traits}")
        # print(f"self.trait_ids={self.trait_ids}\n")

        settings_dict = {}
        data_file = self.__prepare_inputfile_csv()

        settings_dict["path"] = str(data_file)

        residual = services.get_property(self.db_session, self.analysis_request.configResidualPropertyId)
        formula = services.get_property(self.db_session, self.analysis_request.configFormulaPropertyId)


        # HOW IS FORMULA STATEMENT FORMATTED IN ASREML DPO
        # print(formula_statement)
        # trait = Trait
        print("\n",formula.statement,":)\n")
        # formula_statement = formula.statement.format(trait_name=trait.abbreviation)


        job_folder = self.get_job_folder(self.__get_job_name())
        settings_file = os.path.join(job_folder, "settings.json")
        settings_dict["input_phenotypic_data"] = data_file
        # settings_dict["grm"] = os.path.join(job_folder, "/grm.txt")
        settings_dict["output_var"] = os.path.join(job_folder, "/var.csv")
        settings_dict["output_statmodel"] = os.path.join(job_folder, "/output_statmodel.csv")
        settings_dict["output_BV"] = os.path.join(job_folder, "/BVs.csv")
        settings_dict["output_pred"] = os.path.join(job_folder, "/output_pred.csv")
        settings_dict["output_yhat"] = os.path.join(job_folder, "/Yhat.csv")
        settings_dict["output_outliers"] = os.path.join(job_folder, "/outliers.csv")
        settings_dict["formula"] = self.trait_names[0]+" "+formula.statement # check w Pedro
        settings_dict["rcov"] = residual.statement
        settings_dict["raw_analysis_out"] = os.path.join(job_folder, "/raw_analysis_out.rds")
        # print(f"\nsettings_dict[formula] = {f}")
        # print(f"settings_dict[formula] = {self.trait_ids[0]+f}\n")

        with open(settings_file, 'w') as f:
            json.dump(settings_dict, f)

        job_data = JobData()
        job_data.job_name = self.__get_job_name()
        job_data.job_file = settings_file

        return job_data
        

    def run(self):
        """Preprocess input data for SommeR Analysis"""
        return [ self.__prepare_Sommer_settings_file() ]



