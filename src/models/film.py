from typing import List, Optional

import orjson

from pydantic import BaseModel, Field
from fastapi import Query


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmResponse(BaseModel):
    id: str
    title: str


class Film(FilmResponse):
    description: Optional[str]
