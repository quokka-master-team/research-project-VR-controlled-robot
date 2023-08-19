from fastapi import FastAPI
from src.core.utils import import_from
from src.config import DevSettings, Settings
from src.di import all_modules, container


def create_app(settings: type[Settings] = DevSettings) -> FastAPI:
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
    register_routers(app, app_settings)

    return app


def configure_di(settings: Settings) -> None:
    """
    Configures dependency injection container.
    Args:
        settings (Settings: application settings
    """

    container[Settings] = settings
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
