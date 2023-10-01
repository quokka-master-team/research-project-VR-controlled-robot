from src.consts import EMAIL_MAX_LENGTH
from src.core.types.exceptions import MaximumLengthExceeded, InvalidEmail
import re


EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class Email(str):
    def __init__(self, value: str) -> None:
        self._value = self._clean(value)
        self._validate()

    @staticmethod
    def _clean(value: str) -> str:
        return value.strip()

    def _validate(self) -> None:
        if len(self._value) > EMAIL_MAX_LENGTH:
            raise MaximumLengthExceeded(
                f"Maximum length exceeded, emails "
                f"can have only {EMAIL_MAX_LENGTH} characters"
            )

        if not re.match(EMAIL_PATTERN, self._value):
            raise InvalidEmail(f"{self._value} is not an email")
