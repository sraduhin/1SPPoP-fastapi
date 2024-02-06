from typing import Optional

from pydantic import BaseModel


class FilmResponse(BaseModel):
    id: str
    title: str


class Film(FilmResponse):
    description: Optional[str]
