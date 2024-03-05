import enum


class JobStatus(enum.Enum):
    INPROGRESS = "IN-PROGRESS"
    ERROR = "ERROR"
    FAILED = "FAILED"
    FINISHED = "FINISHED"
