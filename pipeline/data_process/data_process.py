from .data_reader import DataReaderFactory

from pipline import config

class DataProcess:

    def __init__(self, data_process_request):
        self.data_process_request = data_process_request

    def run(self):
        pass
