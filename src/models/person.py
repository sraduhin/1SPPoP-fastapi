from typing import Optional

from pydantic import BaseModel


class PersonResponse(BaseModel):
    id: str
    name: str


class Person(PersonResponse):
    male: Optional[str]
