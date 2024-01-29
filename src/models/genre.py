from typing import Optional

from pydantic import BaseModel


class GenreResponse(BaseModel):
    id: str
    title: str


class Genre(GenreResponse):
    description: Optional[str]
