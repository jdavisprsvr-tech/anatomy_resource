import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv(Path(__file__).resolve().with_name(".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "1"))
    )
    CONTENT_EDITOR_INVITE_CODE = os.getenv("CONTENT_EDITOR_INVITE_CODE")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set")

    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET environment variable must be set")


class DevelopmentConfig(Config):
    DEBUG = True
    ENV_NAME = "development"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///dev.db"
    )


class TestingConfig(Config):
    TESTING = True
    ENV_NAME = "testing"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = False
    ENV_NAME = "production"

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}