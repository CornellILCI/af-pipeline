

class DataReaderException(Exception):
    pass


class ApiConnectionError(DataReaderException):
    def __init__(self, api_url):
        self.api_url = api_url

    def __str__(self):
        return repr("Unable to connect to the API {0}".format(self.api_url))
