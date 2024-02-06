from typing import Optional

from utils.models import AbstractModel


class GenreResponse(AbstractModel):
    title: str


class Genre(GenreResponse):
    description: Optional[str]
