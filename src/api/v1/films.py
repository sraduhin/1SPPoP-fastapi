from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from models.film import FilmResponse

from services.film import FilmService, get_film_service


router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=FilmResponse,
    summary="Film's detail",
    description="Get film by id",
    response_description="Film's name and rating",
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return FilmResponse(id=film.id, title=film.title)


@router.get(
    "/",
    response_model=List[FilmResponse],
    summary="Film's list",
    description="Get films",
    response_description="Films with name and rating",
)
async def film_list(
    genres: List[str] = Query(None),
    size: int = 10,
    from_: int = 0,
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmResponse]:
    params = {
        "genres": genres or [], "size": size, "from_": from_
    }
    films = await film_service.get_by_params(**params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return [FilmResponse(id=film.id, title=film.title) for film in films]
