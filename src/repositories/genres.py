from schemas.genre import Genre
from utils.repositories import ESRepository, RedisRepository


class GenreESRepository(ESRepository):
    model = Genre
    index = "genres"


class GenreRedisRepository(RedisRepository):
    model = Genre
    index = "genres"
