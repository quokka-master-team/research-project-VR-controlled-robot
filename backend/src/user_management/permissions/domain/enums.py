from enum import StrEnum, auto


class Permissions(StrEnum):
    test_permission = auto()

    add_stream_units = auto()
    manage_owned_stream_units = auto()
    manage_all_stream_units = auto()

    view_stream_units = auto()
    book_stream_unit = auto()
    connect_to_stream_unit = auto()


class Roles(StrEnum):
    admin = auto()
    stream_units_owner = auto()
    default = auto()
