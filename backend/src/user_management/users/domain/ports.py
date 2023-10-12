from typing import Protocol, Self, Any
from src.core.types import Email
from uuid import UUID
from src.user_management.users.domain.dtos import UserDto
from src.user_management.permissions.domain.ports import (
    RoleRepositoryInterface,
)


class UserRepositoryInterface(Protocol):
    def get_user(self, user_id: UUID) -> UserDto | None:
        ...

    def get_user_by_iam_id(self, iam_id: str) -> UserDto | None:
        ...

    def add_user(self, iam_id: str, email: Email) -> UUID:
        ...


class UserUowInterface(Protocol):
    user_repository: UserRepositoryInterface
    role_repository: RoleRepositoryInterface

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args: Any) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class UserServiceInterface(Protocol):
    def get_user(self, user_id: UUID) -> UserDto:
        ...

    def verify_or_create_user(self, iam_id: str, email: Email) -> UserDto:
        ...
