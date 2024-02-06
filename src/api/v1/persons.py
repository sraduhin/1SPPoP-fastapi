from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from schemas.person import PersonResponse

from services.person import PersonService, person_service
from utils.paginator import Paginator

router = APIRouter()


@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Person's detail",
    description="Get Person by id",
    response_description="Person's full name",
)
async def person_details(
    person_id: str, person_service: PersonService = Depends(person_service)
) -> PersonResponse:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Person not found"
        )
    return PersonResponse(id=person.id, name=person.name)


@router.get(
    "/",
    response_model=List[PersonResponse],
    summary="Person's list",
    description="Get persons",
    response_description="Persons full names",
)
async def persons_list(
    person_service: PersonService = Depends(person_service),
    paginator_params: Paginator = Depends(),
) -> List[PersonResponse]:
    persons = await person_service.get_by_params(paginator_params.__dict__)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Persons not found"
        )
    return [
        PersonResponse(id=person.id, name=person.name) for person in persons
    ]
