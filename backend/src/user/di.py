from src.di.module import Module
from src.user.domain.interfaces import (
    UserUnitOfWorkInterface,
    UserServiceInterface,
)
from src.user.infrastructure.unit_of_work import UserUnitOfWork
from src.user.domain.services import UserService
from src.core.infrastructure.database import SessionProvider


class UserModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        cls.container[UserUnitOfWorkInterface] = UserUnitOfWork(
            cls.container[SessionProvider]
        )
        cls.container[UserServiceInterface] = UserService(
            cls.container[UserUnitOfWorkInterface]
        )
