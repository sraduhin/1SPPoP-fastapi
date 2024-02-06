from http import HTTPStatus
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.genre import GenreResponse

from services.genre import genre_service
from utils.paginator import Paginator
from utils.service import BaseService

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
    summary="Genre's detail",
    description="Get Genre by id",
    response_description="Genre's name",
)
async def genre_details(
    genre_id: str, service: BaseService = Depends(genre_service)
) -> GenreResponse:
    genre = await service.get_by_id(genre_id)
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
    service: Annotated[BaseService, Depends(genre_service)],
    paginator_params: Paginator = Depends(),
) -> List[GenreResponse]:
    genres = await service.get_by_params(paginator_params.__dict__)
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Genres not found"
        )
    return [GenreResponse(id=genre.id, title=genre.title) for genre in genres]
