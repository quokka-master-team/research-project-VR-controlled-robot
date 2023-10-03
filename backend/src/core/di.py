from sqlalchemy import create_engine
from src.core.infrastructure.database import (
    SessionProvider,
)
from src.di.module import Module
from src.config import Settings


class CoreModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        engine = create_engine(cls.container[Settings].SQLALCHEMY_DB_URI)
        cls.container[SessionProvider] = SessionProvider(engine)
