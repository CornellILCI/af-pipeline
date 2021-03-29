from pydantic import BaseModel


class Experiment(BaseModel):
    id: int
    experiment_name: str
