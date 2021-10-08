from af.pipeline.dpo import ProcessData
import os
import csv


class SommeRProcessData(ProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def __get_job_name(self):
        # TODO: put this in ProcessData
        return f"{self.analysis_request.requestId}"

    def __prepare_inputfile_csv(self) -> dict:
        germplasm, plot_data, headers = self.data_reader.get_observation_units_table()

        job_folder = self.get_job_folder(self.__get_job_name())
        data_file = os.path.join(job_folder, f"{self.__get_job_name()}.csv")
        with open(data_file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for data in plot_data:
                writer.writerow(data)

        return {"job_name": self.__get_job_name(), "data_file": data_file}

    def run(self):
        """Preprocess input data for SommeR Analysis"""

        return [self.__prepare_inputfile_csv()]
