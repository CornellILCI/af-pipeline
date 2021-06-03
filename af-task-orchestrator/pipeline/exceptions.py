
class DpoException(Exception):
    pass


class AnalysisError(Exception):
    pass


class RequiredAnalysisRequest(DpoException):
    pass


class RequiredAnalysisConfig(DpoException):
    pass


class InvalidAnalysisRequest(DpoException):
    pass


class InvalidAnalysisConfig(DpoException):
    pass


class InvalidExptLocAnalysisPattern(InvalidAnalysisRequest):
    pass
