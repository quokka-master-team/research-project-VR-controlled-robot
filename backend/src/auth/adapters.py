from kink import inject
from src.di import container
from jwt import PyJWKClient, PyJWKClientError, DecodeError, decode
from src.user.domain.interfaces import UserServiceInterface
from src.core.types import Email
from src.user.domain.dtos import UserDto
from src.auth.exceptions import (
    InvalidToken,
)


@inject(container=container)  # type: ignore
class Auth0TokenVerificationService:
    """Service responsible for auth0 token verification"""

    def __init__(
        self,
        user_service: UserServiceInterface,
        jwk_client: PyJWKClient,
        algorithms: list[str],
        audience: str,
        issuer: str,
    ) -> None:
        self._user_service = user_service
        self._jwk_client = jwk_client
        self._algorithms = algorithms
        self._audience = audience
        self._issuer = issuer

    def _decode_token(self, token: str) -> dict[str, str | bool]:
        signing_key = self._jwk_client.get_signing_key_from_jwt(token).key
        return decode(
            token,
            signing_key,
            algorithms=self._algorithms,
            audience=self._audience,
            issuer=self._issuer,
        )

    def process_token(self, token: str) -> UserDto:
        try:
            decoded_token = self._decode_token(token)
        except (PyJWKClientError, DecodeError):
            raise InvalidToken

        return self._user_service.verify_or_create_user(
            iam_id=decoded_token["sub"],  # type: ignore
            email=Email(decoded_token["email"]),  # type: ignore
        )
