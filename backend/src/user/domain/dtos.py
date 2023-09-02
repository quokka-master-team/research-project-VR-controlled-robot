from dataclasses import dataclass
from uuid import UUID
from src.core.types import Email


@dataclass
class UserDto:
    id: UUID
    iam_id: str

    email: Email
