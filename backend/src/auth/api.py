from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from kink import di
from src.auth.authentication import get_authenticated_user
from typing import Annotated
from src.user_management.users.domain.dtos import UserDto
from src.core.api.models import ErrorMessageResponse
from src.core.api.exceptions import UNAUTHORIZED
import json
import base64


router = APIRouter(prefix="/auth")


@router.get("", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def auth(
    request: Request,
    redirect_uri: str,
    oauth: Annotated[OAuth, Depends(lambda: di[OAuth])],
) -> Response:
    """Redirects to IAM login page"""

    request.session["post_authorization_redirect"] = redirect_uri
    return await oauth.iam.authorize_redirect(
        request, request.url_for("callback")
    )


@router.get("/callback", status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def callback(
    request: Request, oauth: Annotated[OAuth, Depends(lambda: di[OAuth])]
) -> RedirectResponse:
    """Returns user token after successful authorization"""

    token = await oauth.iam.authorize_access_token(request)
    encoded_token = base64.b64encode(json.dumps(token).encode()).decode()

    return RedirectResponse(
        f"{request.session.pop('post_authorization_redirect')}"
        f"?token={encoded_token}"
    )


@router.get(
    "/test",
    status_code=status.HTTP_200_OK,
    responses={UNAUTHORIZED.status_code: ErrorMessageResponse},
)
async def test(
    current_user: Annotated[UserDto, Depends(get_authenticated_user)]
) -> Response:
    return Response(
        content=f"User: {current_user.email} successfully authenticated",
        status_code=200,
    )
