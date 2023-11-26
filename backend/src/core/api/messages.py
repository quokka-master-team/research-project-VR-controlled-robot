from enum import StrEnum, auto
from typing import Any


class BaseError(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any:
        return name.replace("_", "-")


class ApiErrors(BaseError):
    unauthorized = auto()
    forbidden = auto()


class Errors(BaseError):
    maximum_length_exceeded = auto()
    invalid_email = auto()
