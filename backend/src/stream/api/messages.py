from enum import auto
from src.core.api.messages import BaseError


class Errors(BaseError):
    stream_unit_not_found = auto()
    stream_unit_already_exists = auto()
    insufficient_permissions_to_start_transmission = auto()
    stream_unit_in_use = auto()
    timeout = auto()