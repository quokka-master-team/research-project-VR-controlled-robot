from enum import StrEnum, auto


class Errors(StrEnum):
    stream_unit_not_found = auto()
    stream_unit_already_exists = auto()
