import json
from functools import lru_cache
from typing import Optional, List, Union, Dict

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 minutes


class GenreService:
    INDEX = "genres"

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre

    async def get_by_params(self, **params) -> Optional[List[Genre]]:
        genres = await self._genres_from_cache(json.dumps(params))
        if not genres:
            genres = await self._get_genres_from_elastic(**params)
            if not genres:
                return None
            data = {
                "genres": genres,
                "key": self.INDEX + ":" + json.dumps(params),
            }
            await self._put_genres_to_cache(data)

        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index=self.INDEX, id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])

    async def _get_genres_from_elastic(self, **params) -> Optional[List[Genre]]:
        size = params.get("size")
        from_ = params.get("from_")
        try:
            docs = await self.elastic.search(
                index=self.INDEX, size=size, from_=from_
            )
        except NotFoundError:
            return None
        return [Genre(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None

        genre = Genre.model_validate_json(data)
        return genre

    async def _genres_from_cache(self, key: str) -> Optional[List[Genre]]:
        data = await self.redis.get(key)
        if not data:
            return None

        genres = [
            Genre.model_validate_json(genre) for genre in json.loads(data)
        ]
        return genres

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(
            genre.id, genre.model_dump_json(), GENRE_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_genres_to_cache(
        self, data: Dict[str, Union[str, List[Genre]]]
    ):
        genre = [genre.model_dump_json() for genre in data["genres"]]
        await self.redis.set(
            data["key"], json.dumps(genre), GENRE_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
