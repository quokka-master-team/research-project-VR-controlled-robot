from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "Vr-controlled-robot"
    PROJECT_ROOT: str = os.path.abspath((os.path.dirname(__name__)))
    URL_PREFIX_FORMAT: str = "/api/{prefix}"
    ROUTERS: list[tuple[str, str]] = []  # module, prefix


class DevSettings(Settings):
    SQLALCHEMY_DB_URI: str = (
        "postgresql://{user}:{password}@{host}:{port}/{db}".format(
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
            db=os.environ.get("POSTGRES_DB"),
        )
    )
