from typing import Protocol
from src.user.domain.dtos import UserDto


class IAMTokenVerificationService(Protocol):
    def process_token(self, token: str) -> UserDto:
        ...
