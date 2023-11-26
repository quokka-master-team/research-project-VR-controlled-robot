from src.consts import STREAM_UNIT_NAME_MAX_LENGTH
from src.stream.domain.exceptions import (
    StreamUnitNameTooLong,
    InvalidLocationFormat,
)


class StreamUnitName(str):
    def __init__(self, val: str) -> None:
        self._value = self._clean_and_capitalize(val)
        self._validate()

    def _validate(self) -> None:
        if len(self._value) > STREAM_UNIT_NAME_MAX_LENGTH:
            raise StreamUnitNameTooLong

    @staticmethod
    def _clean_and_capitalize(val: str) -> str:
        return val.strip().capitalize()


class StreamUnitLocation:
    def __init__(self, val: str) -> None:
        self._extract_country_and_city(val)
        self._validate()

    def __repr__(self) -> str:
        return f"{self._country}, {self._city}"

    def __str__(self) -> str:
        return f"{self._country}, {self._city}"

    def _extract_country_and_city(self, val: str) -> None:
        try:
            country, city = val.split(",", maxsplit=1)
        except ValueError:
            raise InvalidLocationFormat

        self._country = country.strip()
        self._city = city.strip()

    def _validate(self) -> None:
        pass

    @property
    def city(self) -> str:
        return self._city

    @property
    def country(self) -> str:
        return self._country
