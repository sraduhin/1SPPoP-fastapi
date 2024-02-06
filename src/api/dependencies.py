from db.elastic import get_elastic
from db.redis import get_redis
from repositories.genres import GenreRedisRepository, GenreESRepository
from repositories.persons import PersonRedisRepository, PersonESRepository
from repositories.films import FilmRedisRepository, FilmESRepository

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis


def get_person_redis_repository(redis: Redis = Depends(get_redis)):
    return PersonRedisRepository(redis)


def get_person_elastic_repository(elastic: AsyncElasticsearch = Depends(get_elastic)):
    return PersonESRepository(elastic)


def get_genre_redis_repository(redis: Redis = Depends(get_redis)):
    return GenreRedisRepository(redis)


def get_genre_elastic_repository(elastic: AsyncElasticsearch = Depends(get_elastic)):
    return GenreESRepository(elastic)


def get_film_redis_repository(redis: Redis = Depends(get_redis)):
    return FilmRedisRepository(redis)


def get_film_elastic_repository(elastic: AsyncElasticsearch = Depends(get_elastic)):
    return FilmESRepository(elastic)