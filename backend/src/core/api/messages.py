from enum import StrEnum, auto


class ApiErrors(StrEnum):
    unauthorized = auto()
    forbidden = auto()


class Errors(StrEnum):
    maximum_length_exceeded = auto()
    invalid_email = auto()
