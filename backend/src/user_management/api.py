from fastapi import APIRouter, Response, Depends, status
from src.auth.authentication import get_authenticated_user
from typing import Annotated
from kink import di
from src.user_management.users.domain.dtos import UserDto
from src.user_management.permissions.domain.ports import PermissionValidator
from src.user_management.permissions.domain.enums import Permissions
from src.core.api.exceptions import FORBIDDEN, UNAUTHORIZED
from src.core.api.models import ErrorMessageResponse


router = APIRouter(prefix="/users")


@router.get(
    "/test",
    status_code=status.HTTP_200_OK,
    responses={
        FORBIDDEN.status_code: ErrorMessageResponse,
        UNAUTHORIZED.status_code: ErrorMessageResponse,
    },
)
async def test(
    current_user: Annotated[UserDto, Depends(get_authenticated_user)],
    permission_validator: Annotated[
        PermissionValidator, Depends(lambda: di[PermissionValidator])
    ],
) -> Response:
    if not permission_validator.validate(
        entity_id=current_user.id, permission=Permissions.test_permission
    ):
        raise FORBIDDEN

    return Response(
        content=f"User: {current_user.email} has required permission",
        status_code=status.HTTP_200_OK,
    )
