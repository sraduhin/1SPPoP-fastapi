import json
from functools import lru_cache
from typing import Optional, List, Union, Dict

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 minutes


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_by_params(self, **params) -> Optional[List[Film]]:

        films = await self._films_from_cache(json.dumps(params))
        if not films:
            films = await self._get_films_from_elastic(**params)
            if not films:
                return None
            data = {"films": films, "key": json.dumps(params)}
            await self._put_films_to_cache(data)

        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _get_films_from_elastic(
            self, **params
    ) -> Optional[List[Film]]:
        genres = params.get("genres")
        size = params.get("size")
        from_ = params.get("from_")
        try:
            query = {"bool": {"must": []}}
            for genre in genres:
                query["bool"]["must"].append({"term": {"genre": genre}})
            docs = await self.elastic.search(
                index="movies", query=query, size=size, from_=from_
            )
        except NotFoundError:
            return None
        return [Film(**doc["_source"]) for doc in docs["hits"]["hits"]]

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.model_validate_json(data)
        return film

    async def _films_from_cache(self, key: str) -> Optional[List[Film]]:
        data = await self.redis.get(key)
        if not data:
            return None

        films = [Film.model_validate_json(film) for film in json.loads(data)]
        return films

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(
            film.id, film.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_films_to_cache(self, data: Dict[str, Union[str, List[Film]]]):
        films = [film.model_dump_json() for film in data["films"]]
        await self.redis.set(
            data["key"], json.dumps(films), FILM_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
