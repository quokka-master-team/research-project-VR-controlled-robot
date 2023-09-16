from src.user.users.domain.ports import UserUnitOfWorkInterface
from uuid import UUID
from src.user.users.domain.dtos import UserDto
from src.core.types import Email
from src.user.users.domain.exceptions import UserNotFound, EmailMismatch
from src.consts import Roles
from src.user.roles.exceptions import RoleNotFound


class UserService:
    """Responsible for operations in user domain"""

    def __init__(self, uow: UserUnitOfWorkInterface) -> None:
        self._uow = uow

    def get_user(self, user_id: UUID) -> UserDto:
        with self._uow:
            if user := self._uow.user_repository.get_user(user_id):
                return user

            raise UserNotFound

    def verify_or_create_user(self, iam_id: str, email: Email) -> UserDto:
        with self._uow:
            if user := self._uow.user_repository.get_user_by_iam_id(iam_id):
                if user.email != email:
                    raise EmailMismatch

                return user

            new_user_id = self._uow.user_repository.add_user(
                iam_id=iam_id, email=email
            )

            if not (
                role := self._uow.role_repository.get_role_by_name(
                    Roles.default
                )
            ):
                raise RoleNotFound

            self._uow.role_repository.assign_role(
                user_id=new_user_id, role_id=role.id
            )

            self._uow.commit()

        return self.get_user(new_user_id)
