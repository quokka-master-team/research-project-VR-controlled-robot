from src.core.infrastructure.database import SessionProvider
from uuid import UUID
from src.user_management.permissions.domain.enums import Permissions
from src.user_management.permissions.infrastructure.repositories import (
    user_has_permission,
)


class UserPermissionValidator:
    def __init__(self, session_provider: SessionProvider) -> None:
        self._session_provider = session_provider

    def validate(self, entity_id: UUID, permission: Permissions) -> bool:
        with self._session_provider.get_session() as session:
            return user_has_permission(
                session=session, user_id=entity_id, permission=permission
            )
