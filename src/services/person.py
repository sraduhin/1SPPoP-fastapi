from functools import lru_cache
from fastapi import Depends
from api.dependencies import get_person_elastic_repository, \
    get_person_redis_repository
from utils.repositories import RedisRepository, ESRepository
from utils.service import BaseService

@lru_cache
def person_service(
    redis_repo: RedisRepository = Depends(get_person_redis_repository),
    elastic_repo: ESRepository = Depends(get_person_elastic_repository),
):
    return BaseService(redis_repo, elastic_repo)
