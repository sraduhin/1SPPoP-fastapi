from schemas.film import Film
from utils.repositories import ESRepository, RedisRepository


class FilmESRepository(ESRepository):
    model = Film
    index = "movies"


class FilmRedisRepository(RedisRepository):
    model = Film
    index = "movies"
