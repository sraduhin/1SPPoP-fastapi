from functools import lru_cache
from fastapi import Depends
from api.dependencies import get_film_elastic_repository, get_film_redis_repository
from utils.repositories import RedisRepository, ESRepository
from utils.service import BaseService


@lru_cache
def film_service(
    redis_repo: RedisRepository = Depends(get_film_redis_repository),
    elastic_repo: ESRepository = Depends(get_film_elastic_repository),
):
    return BaseService(redis_repo, elastic_repo)
