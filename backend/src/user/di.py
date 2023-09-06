from src.di.module import Module
from src.user.users.domain.ports import (
    UserUnitOfWorkInterface,
    UserServiceInterface,
)
from src.user.users.infrastructure.unit_of_work import UserUnitOfWork
from src.user.users.domain.services import UserService
from src.core.infrastructure.database import SessionProvider
from src.user.roles.ports import PermissionValidator
from src.user.roles.adapters import PermissionValidatorAdapter


class UserModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        cls.container[UserUnitOfWorkInterface] = UserUnitOfWork(
            cls.container[SessionProvider]
        )
        cls.container[UserServiceInterface] = UserService(
            cls.container[UserUnitOfWorkInterface]
        )
        cls.container[PermissionValidator] = PermissionValidatorAdapter(
            cls.container[SessionProvider]
        )
