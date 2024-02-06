import json
from abc import ABC, abstractmethod
from fastapi import Depends
from typing import Optional, List

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from utils.models import AbstractModel


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class ESRepository(AbstractRepository):
    model: AbstractModel = None
    index: str = ""

    def __init__(self, elastic: AsyncElasticsearch):
        self.storage = elastic

    async def get_one(self, id_: str):
        try:
            doc = await self.storage.get(index=self.index, id=id_)
        except NotFoundError:
            return None
        return self.model(**doc["_source"])

    async def get_all(self, params: dict):
        size = params.get("limit")
        from_ = params.get("skip")

        filters = params.get("genres")
        query = None
        if filters:
            query = {"bool": {"must": []}}
            for genre in filters:
                query["bool"]["must"].append({"term": {"genre": genre}})
        try:
            docs = await self.storage.search(
                index=self.index, query=query, size=size, from_=from_
            )
        except NotFoundError:
            return None
        return [self.model(**doc["_source"]) for doc in docs["hits"]["hits"]]


class RedisRepository(AbstractRepository):
    model: AbstractModel = None
    index: str = ""
    CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 minutes

    def __init__(self, redis: Redis):
        self.storage = redis

    async def get_one(self, id_: str) -> Optional:
        data = await self.storage.get(id_)
        if not data:
            return None

        item = self.model.model_validate_json(data)
        return item

    async def get_all(self, params) -> Optional[list]:
        data = await self.storage.get(json.dumps(params))
        if not data:
            return None

        items = [
            self.model.model_validate_json(item) for item in json.loads(data)
        ]
        return items

    async def add_one(self, item: AbstractModel):
        await self.storage.set(
            item.id, item.model_dump_json(), self.CACHE_EXPIRE_IN_SECONDS
        )

    async def add_all(
            self, params: dict, items: Optional[List[AbstractModel]]
    ):
        items = [item.model_dump_json() for item in items]
        cache_key = f"{self.index}:{json.dumps(params)}"
        await self.storage.set(
            cache_key, json.dumps(items), self.CACHE_EXPIRE_IN_SECONDS
        )
