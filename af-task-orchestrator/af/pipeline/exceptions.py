class DpoException(Exception):
    pass


class AnalysisError(Exception):
    pass


class RequiredAnalysisRequest(DpoException):
    pass


class InvalidAnalysisRequest(DpoException):
    pass


class FileParseException(Exception):
    pass


class InvalidFilePath(Exception):
    pass


class InvalidVariance(ValueError):
    def __init__(self, message="Variance value should be between 0 and 1", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class InvalidAverageStandardError(ValueError):
    def __init__(self, message="Average standard error value should be between 0 and 1", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
