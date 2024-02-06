from schemas.person import Person
from utils.repositories import ESRepository, RedisRepository


class PersonESRepository(ESRepository):
    model = Person
    index = "persons"


class PersonRedisRepository(RedisRepository):
    model = Person
    index = "persons"
