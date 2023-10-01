from src.user_management.users.domain.dtos import UserDto
from typing import TYPE_CHECKING
from src.core.types import Email


if TYPE_CHECKING:
    from src.user_management.users.infrastructure.models import User


def user_mapper(user: "User") -> UserDto:
    return UserDto(id=user.id, iam_id=user.iam_id, email=Email(user.email))
