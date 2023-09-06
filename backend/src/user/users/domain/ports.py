from typing import Protocol, Any
from src.core.types import Email
from uuid import UUID
from src.user.users.domain.dtos import UserDto
from src.user.roles.ports import RoleRepositoryInterface


class UserRepositoryInterface(Protocol):
    def get_user(self, user_id: UUID) -> UserDto | None:
        ...

    def get_user_by_iam_id(self, iam_id: str) -> UserDto | None:
        ...

    def add_user(self, iam_id: str, email: Email) -> UUID:
        ...


class UserUnitOfWorkInterface(Protocol):
    user_repository: UserRepositoryInterface
    role_repository: RoleRepositoryInterface

    def __enter__(self) -> None:
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
