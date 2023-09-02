from src.user.domain.interfaces import UserUnitOfWorkInterface
from uuid import UUID
from src.user.domain.dtos import UserDto
from src.core.types import Email
from src.user.domain.exceptions import UserNotFound, EmailMismatch


class UserService:
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
            self._uow.commit()

        return self.get_user(new_user_id)
