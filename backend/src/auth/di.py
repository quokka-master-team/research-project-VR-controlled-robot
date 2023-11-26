from src.di.module import Module
from src.auth.adapters import Auth0TokenVerificationService
from src.auth.ports import IAMTokenVerificationService
from jwt import PyJWKClient
from src.config import Settings
from src.user_management.users.domain.ports import UserServiceInterface


class AuthModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        settings = cls.container[Settings]
        jwk_client = PyJWKClient(
            f"https://{settings.IAM_DOMAIN}/.well-known/jwks.json"
        )

        cls.container[
            IAMTokenVerificationService
        ] = Auth0TokenVerificationService(
            user_service=cls.container[UserServiceInterface],  # type: ignore
            jwk_client=jwk_client,
            algorithms=settings.IAM_ALGORITHMS,
            audience=settings.IAM_CLIENT_ID,
            issuer=f"https://{settings.IAM_DOMAIN}/",
        )
