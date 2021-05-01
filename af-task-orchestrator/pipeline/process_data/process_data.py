
from .data_reader import DataReaderFactory

from pipeline import config


class ProcessData:

    def __init__(self, process_data_request):
        self.process_data_request = process_data_request


    def run(self):
        pass
