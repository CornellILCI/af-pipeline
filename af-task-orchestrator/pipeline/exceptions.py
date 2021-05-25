class ProcessDataException(Exception):
    pass


class RequiredAnalysisRequest(ProcessDataException):
    pass


class RequiredAnalysisConfig(ProcessDataException):
    pass


class InvalidAnalysisRequest(ProcessDataException):
    pass


class InvalidAnalysisConfig(ProcessDataException):
    pass


class InvalidExptLocAnalysisPattern(InvalidAnalysisRequest):
    pass
