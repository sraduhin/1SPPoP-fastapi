from functools import lru_cache
from typing import Optional, List
from fastapi import Depends
from api.dependencies import get_genre_elastic_repository, \
    get_genre_redis_repository
from schemas.genre import Genre
from utils.repositories import RedisRepository, ESRepository


class GenreService:

    def __init__(self, redis_repo: RedisRepository, es_repo: ESRepository):
        self.redis = redis_repo
        self.elastic = es_repo

    async def get_by_id(self, item_id: str) -> Optional[Genre]:
        item = await self.redis.get_one(item_id)
        if not item:
            item = await self.elastic.get_one(item_id)
            if not item:
                return None
            await self.redis.add_one(item)

        return item

    async def get_by_params(self, params) -> Optional[List[Genre]]:
        print(params)
        items = await self.redis.get_all(params)
        if not items:
            items = await self.elastic.get_all(params)
            if not items:
                return None
            await self.redis.add_all(params, items)

        return items


@lru_cache
def genre_service(
    redis_repo: RedisRepository = Depends(get_genre_redis_repository),
    elastic_repo: ESRepository = Depends(get_genre_elastic_repository),
):
    return GenreService(redis_repo, elastic_repo)
