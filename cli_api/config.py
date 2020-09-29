"""
config.py

Defines application level configuration objects.
"""
import logging
import os


logger = logging.getLogger(__name__)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    BCRYPT_LOG_ROUNDS = int(os.getenv("BCRYPT_LOG_ROUNDS", 12))
    DEBUG = False
    CACHE_OBJECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENABLE_DEV_APIS = False

    # Postgres config
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")

    # Redis/RQ config
    REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"
    RQ_REDIS_URL = REDIS_URL


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///cli_api.db"


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    test=TestConfig,
)
