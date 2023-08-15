from sqlalchemy import Engine, create_engine
from src.core.database import SessionProvider, SessionProviderFactory
from src.di.module import Module
from src.config import Settings


class CoreModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        cls.container[Engine] = create_engine(
            cls.container[Settings].SQLALCHEMY_DB_URI
        )
        cls.container.add_factory(
            SessionProvider,
            SessionProviderFactory(engine=cls.container[Engine]),
        )
