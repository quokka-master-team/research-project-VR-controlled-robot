from typing import Any
from src.core.infrastructure.database import SessionProvider
from src.user.infrastructure.repository import UserRepository


class UserUnitOfWork:
    def __init__(self, session_provider: SessionProvider) -> None:
        self._session_provider = session_provider

    def __enter__(self) -> None:
        self._session = self._session_provider.create_session()
        self.user_repository = UserRepository(self._session)

    def __exit__(self, *args: Any) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
