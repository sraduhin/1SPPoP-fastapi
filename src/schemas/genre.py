from typing import Optional

from utils.models import AbstractModel


class GenreResponse(AbstractModel):
    title: str

    class Config:
        from_attributes = True


class Genre(GenreResponse):
    description: Optional[str]

    class Config:
        from_attributes = True
