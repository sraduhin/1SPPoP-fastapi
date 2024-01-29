from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.genre import GenreResponse

from services.genre import GenreService, get_genre_service


router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
    summary="Genre's detail",
    description="Get Genre by id",
    response_description="Genre's name",
)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> GenreResponse:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Genre not found"
        )
    return GenreResponse(id=genre.id, title=genre.title)


@router.get(
    "/",
    response_model=List[GenreResponse],
    summary="Genre's list",
    description="Get genres",
    response_description="Genres names",
)
async def genres_list(
    size: int = 10,
    from_: int = 0,
    genre_service: GenreService = Depends(get_genre_service),
) -> List[GenreResponse]:
    params = {"size": size, "from_": from_}
    genres = await genre_service.get_by_params(**params)
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Genres not found"
        )
    return [GenreResponse(id=genre.id, title=genre.title) for genre in genres]
