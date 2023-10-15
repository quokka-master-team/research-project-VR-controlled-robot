from fastapi import HTTPException, status
from src.core.api.messages import ApiErrors


UNAUTHORIZED = HTTPException(
    status.HTTP_401_UNAUTHORIZED, ApiErrors.unauthorized
)
FORBIDDEN = HTTPException(status.HTTP_403_FORBIDDEN, ApiErrors.forbidden)
