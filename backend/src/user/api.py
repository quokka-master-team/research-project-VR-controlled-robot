from fastapi_class import View
from fastapi import APIRouter, Response, Depends, HTTPException, status
from src.auth.authentication import get_authenticated_user
from typing import Annotated
from src.user.users.domain.dtos import UserDto
from src.user.roles.ports import PermissionValidator
from src.di import container
from src.consts import Permissions
from src.core.api.messages import ApiErrors

router = APIRouter()


@View(router, path="/test")
class UserTestResource:
    @staticmethod
    async def get(
        current_user: Annotated[UserDto, Depends(get_authenticated_user)],
        permission_validator: PermissionValidator = Depends(
            lambda: container[PermissionValidator]
        ),
    ) -> Response:
        if not permission_validator.validate_user_permission(
            user_id=current_user.id, permission=Permissions.test_permission
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ApiErrors.forbidden,
            )

        return Response(
            content=f"User: {current_user.email} has required permission",
            status_code=200,
        )
