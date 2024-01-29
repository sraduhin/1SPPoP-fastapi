from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.person import PersonResponse

from services.person import PersonService, get_person_service


router = APIRouter()


@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Person's detail",
    description="Get Person by id",
    response_description="Person's full name",
)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
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
    size: int = 10,
    from_: int = 0,
    person_service: PersonService = Depends(get_person_service),
) -> List[PersonResponse]:
    params = {"size": size, "from_": from_}
    persons = await person_service.get_by_params(**params)
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Persons not found"
        )
    return [
        PersonResponse(id=person.id, name=person.name) for person in persons
    ]
