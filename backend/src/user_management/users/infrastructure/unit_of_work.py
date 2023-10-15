from typing import Self

from src.user_management.users.infrastructure.repository import UserRepository
from src.user_management.permissions.infrastructure.repositories import (
    RoleRepository,
)
from src.core.infrastructure.unit_of_work import UnitOfWork


class UserUow(UnitOfWork):
    def __enter__(self) -> Self:
        self._session = self._session_provider.create_session()
        self.user_repository = UserRepository(self._session)
        self.role_repository = RoleRepository(self._session)

        return self
