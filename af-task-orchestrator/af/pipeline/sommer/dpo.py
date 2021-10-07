from af.pipeline.dpo import ProcessData
import os
import pathlib


class SommeRProcessData(ProcessData):
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def seml(self):
        pass

    def sesl(self):
        pass

    def mesl(self):
        pass

    def meml(self):
        pass

    def __get_job_name(self):
        # TODO: put this in ProcessData
        return f"{self.analysis_request.requestId}"


    def __prepare_inputfile_csv(self) -> dict:
        



    def run(self):
        """Preprocess input data for SommeR Analysis"""

        return [
            self.__prepare_inputfile_csv()
        ]
        
