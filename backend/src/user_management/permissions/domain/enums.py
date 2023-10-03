from enum import StrEnum, auto


class Permissions(StrEnum):
    test_permission = auto()


class Roles(StrEnum):
    admin = auto()
    default = auto()
