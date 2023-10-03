from fastapi_class import View
from fastapi import APIRouter, Response, Depends, HTTPException, status
from src.auth.authentication import get_authenticated_user
from typing import Annotated
from kink import di
from src.user_management.users.domain.dtos import UserDto
from src.user_management.permissions.domain.ports import PermissionValidator
from src.user_management.permissions.domain.enums import Permissions
from src.core.api.messages import ApiErrors

router = APIRouter()


@View(router, path="/test")
class UserTestResource:
    @staticmethod
    async def get(
        current_user: Annotated[UserDto, Depends(get_authenticated_user)],
        permission_validator: PermissionValidator = Depends(
            lambda: di[PermissionValidator]
        ),
    ) -> Response:
        if not permission_validator.validate(
            entity_id=current_user.id, permission=Permissions.test_permission
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ApiErrors.forbidden,
            )

        return Response(
            content=f"User: {current_user.email} has required permission",
            status_code=200,
        )
