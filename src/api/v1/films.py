from http import HTTPStatus
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.film import FilmResponse

from services.film import film_service
from utils.paginator import Paginator
from utils.service import BaseService

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=FilmResponse,
    summary="Film's detail",
    description="Get film by id",
    response_description="Film's name and rating",
)
async def film_details(
    film_id: str, service: BaseService = Depends(film_service)
) -> FilmResponse:
    film = await service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Film not found"
        )
    return FilmResponse(id=film.id, title=film.title)


@router.get(
    "/",
    response_model=List[FilmResponse],
    summary="Film's list",
    description="Get films",
    response_description="Films with name and rating",
)
async def film_list(
    service: Annotated[BaseService, Depends(film_service)],
    paginator_params: Paginator = Depends(),
    genres: List[str] = Query(None),
) -> List[FilmResponse]:
    params = paginator_params.__dict__
    params["genres"] = genres
    films = await service.get_by_params(params)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Films not found"
        )
    return [FilmResponse(id=film.id, title=film.title) for film in films]