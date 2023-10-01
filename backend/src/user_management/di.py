from src.di.module import Module
from src.user_management.users.domain.ports import (
    UserUnitOfWorkInterface,
    UserServiceInterface,
)
from src.user_management.users.infrastructure.unit_of_work import (
    UserUnitOfWork,
)
from src.user_management.users.application.services import UserService
from src.core.infrastructure.database import SessionProvider
from src.user_management.permissions.domain.ports import PermissionValidator
from src.user_management.permissions.application.adapters import (
    UserPermissionValidator,
)


class UserModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        cls.container[UserUnitOfWorkInterface] = UserUnitOfWork(
            cls.container[SessionProvider]
        )
        cls.container[UserServiceInterface] = UserService(
            cls.container[UserUnitOfWorkInterface]
        )
        cls.container[PermissionValidator] = UserPermissionValidator(
            cls.container[SessionProvider]
        )
