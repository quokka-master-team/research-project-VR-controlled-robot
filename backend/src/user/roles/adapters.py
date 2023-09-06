from src.core.infrastructure.database import SessionProvider
from uuid import UUID
from src.consts import Permissions
from src.user.roles.repositories import user_has_permission


class PermissionValidatorAdapter:
    def __init__(self, session_provider: SessionProvider) -> None:
        self._session_provider = session_provider

    def validate_user_permission(
        self, user_id: UUID, permission: Permissions
    ) -> bool:
        with self._session_provider.get_session() as session:
            return user_has_permission(
                session=session, user_id=user_id, permission=permission
            )
