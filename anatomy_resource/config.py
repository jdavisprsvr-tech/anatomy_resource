import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY enviromenr variiable must be set")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV_NAME = "development"


class TestingConfig(Config):
    TESTING = True
    ENV_NAME = "testing"


class ProductionConfig(Config):
    DEBUG = False
    ENV_NAME = "production"


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
