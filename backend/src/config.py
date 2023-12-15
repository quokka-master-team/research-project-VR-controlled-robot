import logging

from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "Vr-controlled-robot"
    APP_SECRET: str = os.environ.get("APP_SECRET_KEY", "super-secret")
    PROJECT_ROOT: str = os.path.abspath((os.path.dirname(__name__)))
    LOGGING_LEVEL: int = logging.INFO
    URL_PREFIX: str = "/api"
    ROUTERS: list[str] = [
        "src.auth.api",
        "src.user_management.api",
        "src.stream.api.router",
    ]

    SQLALCHEMY_DB_URI: str = (
        "postgresql://{user}:{password}@{host}:{port}/{db}".format(
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
            db=os.environ.get("POSTGRES_DB"),
        )
    )

    IAM_CLIENT_ID: str = os.environ.get("IAM_CLIENT_ID", "client-id")
    IAM_CLIENT_SECRET: str = os.environ.get(
        "IAM_CLIENT_SECRET", "client-secret"
    )
    IAM_DOMAIN: str = os.environ.get("IAM_DOMAIN", "client-domain")
    IAM_ALGORITHMS: list[str] = [os.environ.get("IAM_ALGORITHMS", "RS256")]

    STREAM_PIPELINE: str = os.environ.get("STREAM_PIPELINE")
    STREAM_DESTINATION_IP: str = os.environ.get("STREAM_DESTINATION_IP")
    STREAM_DESTINATION_PORT: int = int(
        os.environ.get("STREAM_DESTINATION_PORT")
    )
