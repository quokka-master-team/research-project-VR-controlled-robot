from enum import StrEnum, auto


EMAIL_MAX_LENGTH = 320


class Permissions(StrEnum):
    test_permission = auto()


class Roles(StrEnum):
    admin = auto()
    default = auto()
