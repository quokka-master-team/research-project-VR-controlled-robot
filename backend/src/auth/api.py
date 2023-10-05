from fastapi_class import View
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from kink import inject
from src.auth.authentication import get_authenticated_user
from typing import Annotated
from src.user_management.users.domain.dtos import UserDto

router = APIRouter()


@View(router)
@inject
class AuthResource:
    """Redirects to IAM login page"""

    def __init__(self, oauth: OAuth) -> None:
        self.oauth = oauth

    async def get(self, request: Request, redirect_uri: str) -> Response:
        request.session["post_authorization_redirect"] = redirect_uri
        return await self.oauth.iam.authorize_redirect(
            request,
            request.url_for("Get Auth Callback Resource")
        )


@View(router, path="/callback")
@inject
class AuthCallbackResource:
    """Returns user token after successful authorization"""

    def __init__(self, oauth: OAuth) -> None:
        self.oauth = oauth

    async def get(self, request: Request) -> RedirectResponse:
        token = await self.oauth.iam.authorize_access_token(request)
        return RedirectResponse(f"{request.session.pop('post_authorization_redirect')}?token={token}")


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
