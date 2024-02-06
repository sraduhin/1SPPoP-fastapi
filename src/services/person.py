from functools import lru_cache
from typing import Optional, List
from fastapi import Depends
from api.dependencies import get_person_elastic_repository, \
    get_person_redis_repository
from schemas.genre import Genre
from utils.repositories import AbstractRepository


class PersonService:
    def __init__(self, redis_repo: AbstractRepository, es_repo: AbstractRepository):
        self.redis = redis_repo
        self.elastic = es_repo

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self.redis.get_one(genre_id)
        if not genre:
            genre = await self.elastic.get_one(genre_id)
            if not genre:
                return None
            await self.redis.add_one(genre)

        return genre

    async def get_by_params(self, params) -> Optional[List[Genre]]:
        print(params)
        genres = await self.redis.get_all(params)
        if not genres:
            genres = await self.elastic.get_all(params)
            if not genres:
                return None
            await self.redis.add_all(params, genres)

        return genres


@lru_cache()
def person_service(
    redis_repo: AbstractRepository = Depends(get_person_redis_repository),
    elastic_repo: AbstractRepository = Depends(get_person_elastic_repository),
) -> PersonService:
    return PersonService(redis_repo, elastic_repo)

