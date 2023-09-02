from fastapi_class import View
from fastapi import APIRouter, Request, Response, Depends
from src.di import container
from authlib.integrations.starlette_client import OAuth
from kink import inject
from src.auth.authentication import get_authenticated_user
from typing import Annotated
from src.user.domain.dtos import UserDto

router = APIRouter()


@View(router)
@inject(container=container)
class AuthResource:
    """Redirects to IAM login page"""

    def __init__(self, oauth: OAuth) -> None:
        self.oauth = oauth

    async def get(self, request: Request) -> Response:
        redirect_uri = request.url_for("Get Auth Callback Resource")
        return await self.oauth.iam.authorize_redirect(request, redirect_uri)


@View(router, path="/callback")
@inject(container=container)
class AuthCallbackResource:
    """Returns user token after successful authorization"""

    def __init__(self, oauth: OAuth) -> None:
        self.oauth = oauth

    async def get(self, request: Request) -> Response:
        return await self.oauth.iam.authorize_access_token(request)


@View(router, path="/test")
class AuthTestResource:
    @staticmethod
    async def get(
        current_user: Annotated[UserDto, Depends(get_authenticated_user)]
    ) -> Response:
        return Response(
            content=f"User: {current_user.email} successfully authenticated",
            status_code=200,
        )
