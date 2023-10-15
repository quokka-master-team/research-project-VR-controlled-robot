from typing import Any, Self
from abc import ABC, abstractmethod
from src.core.infrastructure.database import SessionProvider


class UnitOfWork(ABC):
    def __init__(self, session_provider: SessionProvider) -> None:
        self._session_provider = session_provider

    @abstractmethod
    def __enter__(self) -> Self:
        self._session = self._session_provider.create_session()

        return self

    def __exit__(self, *args: Any) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
