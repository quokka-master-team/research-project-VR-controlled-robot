from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from kink import di
from src.auth.ports import IAMTokenVerificationService
from src.user_management.users.domain.dtos import UserDto
from src.core.types.exceptions import InvalidEmail, MaximumLengthExceeded
from src.user_management.users.domain.exceptions import EmailMismatch
from fastapi import HTTPException, status
from src.auth.exceptions import (
    InvalidToken,
)
from src.core.api.messages import ApiErrors, Errors


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_authenticated_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_verification_service: Annotated[
        IAMTokenVerificationService,
        Depends(lambda: di[IAMTokenVerificationService]),
    ],
) -> UserDto:
    """Verifies token and return user linked with this token"""

    try:
        return token_verification_service.process_token(token)
    except (
        EmailMismatch,
        InvalidToken,
    ) as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiErrors.unauthorized,
        )

    except MaximumLengthExceeded:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"email": Errors.maximum_length_exceeded},
        )
    except InvalidEmail:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"email": Errors.invalid_email},
        )
