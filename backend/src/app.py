from fastapi import FastAPI
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from src.core.utils import import_from
from src.config import Settings
from src.di import all_modules
from kink import di


def create_app(settings: type[Settings] = Settings) -> FastAPI:
    """
    Creates FastAPI app.
    Args:
        settings (Settings): application settings

    Returns:
        app (FastAPI):
    """

    app = FastAPI()
    app_settings = settings()

    configure_di(app_settings)
    configure_extensions(app_settings)
    configure_middleware(app, app_settings)
    register_routers(app, app_settings)

    return app


def configure_di(settings: Settings) -> None:
    """
    Configures dependency injection container.
    Args:
        settings (Settings: application settings
    """

    di[Settings] = settings
    for module in all_modules:
        module.bootstrap()


def register_routers(app: FastAPI, settings: Settings) -> None:
    """
    Registers app routes.
    Args:
        app (FastAPI): FastAPI application
        settings (Settings): application settings
    """

    for module, prefix in settings.ROUTERS:
        router = import_from(module, "router")
        app.include_router(
            router,
            prefix=settings.URL_PREFIX_FORMAT.format(prefix=prefix),
        )


def configure_extensions(settings: Settings) -> None:
    oauth = OAuth()
    oauth.register(
        "iam",
        client_id=settings.IAM_CLIENT_ID,
        client_secret=settings.IAM_CLIENT_SECRET,
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f"https://{settings.IAM_DOMAIN}/"
        f".well-known/openid-configuration",
    )
    di[OAuth] = oauth


def configure_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(SessionMiddleware, secret_key=settings.APP_SECRET)
