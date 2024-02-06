from typing import Optional

from utils.models import AbstractModel


class FilmResponse(AbstractModel):
    title: str


class Film(FilmResponse):
    description: Optional[str]
