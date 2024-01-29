import json
from functools import lru_cache
from typing import Optional, List, Union, Dict

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 minutes


class PersonService:
    INDEX = "persons"

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def get_by_params(self, **params) -> Optional[List[Person]]:
        persons = await self._persons_from_cache(json.dumps(params))
        if not persons:
            persons = await self._get_persons_from_elastic(**params)
            if not persons:
                return None
            data = {
                "persons": persons,
                "key": self.INDEX + ":" + json.dumps(params),
            }
            await self._put_persons_to_cache(data)

        return persons

    async def _get_person_from_elastic(
        self, person_id: str
    ) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index=self.INDEX, id=person_id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])

    async def _get_persons_from_elastic(
        self, **params
    ) -> Optional[List[Person]]:
        size = params.get("size")
        from_ = params.get("from_")
        try:
            docs = await self.elastic.search(
                index=self.INDEX, size=size, from_=from_
            )
        except NotFoundError:
            return None
        return [Person(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None

        person = Person.model_validate_json(data)
        return person

    async def _persons_from_cache(self, key: str) -> Optional[List[Person]]:
        data = await self.redis.get(key)
        if not data:
            return None

        persons = [
            Person.model_validate_json(person) for person in json.loads(data)
        ]
        return persons

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(
            person.id, person.model_dump_json(), PERSON_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_persons_to_cache(
        self, data: Dict[str, Union[str, List[Person]]]
    ):
        person = [person.model_dump_json() for person in data["persons"]]
        await self.redis.set(
            data["key"], json.dumps(person), PERSON_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
