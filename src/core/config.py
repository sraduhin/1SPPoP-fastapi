import os
from logging import config as logging_config

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv("PROJECT_NAME", "Pet-movies")
PROJECT_DESC = os.getenv("PROJECT_DESC", "Put your description here")
PROJECT_VERSION = os.getenv("PROJECT_VERSION", "1.0.0")


REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
