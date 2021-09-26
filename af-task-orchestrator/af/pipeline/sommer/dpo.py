from af.pipeline.dpo import ProcessData


class SommeRProcessData(ProcessData):
    def __init__(self, analysis_request, *args, **kwargs):
        self.analysis_request = analysis_request

    def get_traits(self):
        pass

    def seml(self):
        pass

    def sesl(self):
        pass

    def run(self):
        pass
