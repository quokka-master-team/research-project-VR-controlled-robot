from src.core.types import Email
import sqlalchemy as sqla
from sqlalchemy.orm import Session
from src.user_management.users.infrastructure.models import User
from uuid import uuid4, UUID
from src.user_management.users.domain.dtos import UserDto
from src.user_management.users.infrastructure.mappers import user_mapper


class UserRepository:
    """Responsible for interacting with user db table"""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_user(self, user_id: UUID) -> UserDto | None:
        if user := self._session.scalar(
            sqla.select(User).where(User.id == user_id)
        ):
            return user_mapper(user)

        return None

    def get_user_by_iam_id(self, iam_id: str) -> UserDto | None:
        if user := self._session.scalar(
            sqla.select(User).where(User.iam_id == iam_id)
        ):
            return user_mapper(user)

        return None

    def add_user(self, iam_id: str, email: Email) -> UUID:
        user_id = uuid4()
        self._session.execute(
            sqla.insert(User).values(
                id=user_id,
                iam_id=iam_id,
                email=email,
            )
        )
        return user_id
