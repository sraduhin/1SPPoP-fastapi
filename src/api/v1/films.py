from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service


router = APIRouter()


class Film(BaseModel):
    id: str
    title: str


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Film's detail",
    description="Get fiml by id",
    response_description="Film's name and rating",
    tags=["Fulltext search"],
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Film(id="some_id", title="some_title")
