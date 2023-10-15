from src.di.module import Module
from src.user_management.users.domain.ports import (
    UserUowInterface,
    UserServiceInterface,
)
from src.user_management.users.infrastructure.unit_of_work import (
    UserUow,
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
        cls.container[UserUowInterface] = UserUow(
            cls.container[SessionProvider]
        )
        cls.container[UserServiceInterface] = UserService(
            cls.container[UserUowInterface]  # type: ignore
        )
        cls.container[PermissionValidator] = UserPermissionValidator(
            cls.container[SessionProvider]  # type: ignore
        )
