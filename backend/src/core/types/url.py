from urllib.parse import urlparse
from src.core.types.exceptions import InvalidURL


class URL:
    def __init__(self, val: str) -> None:
        self._value = self._clean(val)
        self._validate()

    def __str__(self) -> str:
        return self._value

    def _validate(self) -> None:
        url = urlparse(self._value)
        if not all((url.scheme, url.netloc)):
            raise InvalidURL

    @staticmethod
    def _clean(val: str) -> str:
        return val.strip()
