from typing import Protocol
from src.user.users.domain.dtos import UserDto


class IAMTokenVerificationService(Protocol):
    def process_token(self, token: str) -> UserDto:
        ...
