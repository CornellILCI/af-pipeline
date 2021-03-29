from pydantic import BaseModel


class Trait(BaseModel):
    id: int
    trait_name: str
