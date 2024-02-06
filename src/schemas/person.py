from typing import Optional

from utils.models import AbstractModel


class PersonResponse(AbstractModel):
    name: str


class Person(PersonResponse):
    male: Optional[str]
