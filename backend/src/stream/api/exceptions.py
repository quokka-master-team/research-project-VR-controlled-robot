from fastapi import HTTPException, status
from src.stream.api.messages import Errors

STREAM_UNIT_NOT_FOUND = HTTPException(
    status.HTTP_404_NOT_FOUND, Errors.stream_unit_not_found
)

STREAM_UNIT_ALREADY_EXIST = HTTPException(
    status.HTTP_400_BAD_REQUEST, Errors.stream_unit_already_exists
)

STREAM_UNIT_IN_USE = HTTPException(
    status.HTTP_400_BAD_REQUEST, Errors.stream_unit_in_use
)
