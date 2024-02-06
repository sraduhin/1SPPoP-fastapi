from typing import Optional, List
from schemas.genre import Genre
from utils.repositories import ReadWriteRepository, ReadOnlyRepository


class BaseService:
    def __init__(
        self, redis_repo: ReadWriteRepository, es_repo: ReadOnlyRepository
    ):
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
        items = await self.redis.get_all(params)
        if not items:
            items = await self.elastic.get_all(params)
            if not items:
                return None
            await self.redis.add_all(params, items)

        return items
