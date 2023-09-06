from sqlalchemy.orm import Session
import sqlalchemy as sqla
from uuid import UUID
from src.consts import Permissions
from src.user.roles.models import (
    roles_permissions,
    users_roles,
    Permission,
    Role,
)
from src.consts import Roles
from src.user.roles.dtos import RoleDto


def user_has_permission(
    session: Session, user_id: UUID, permission: Permissions
) -> bool:
    stmt = (
        sqla.select(roles_permissions.c.role_id)
        .join(
            users_roles, users_roles.c.role_id == roles_permissions.c.role_id
        )
        .join(Permission, Permission.id == roles_permissions.c.permission_id)
        .where(users_roles.c.user_id == user_id, Permission.name == permission)
    )
    return bool(session.scalar(stmt))


class RoleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_role_by_name(self, role_name: Roles) -> RoleDto | None:
        if role := self._session.scalar(
            sqla.select(Role).where(Role.name == role_name)
        ):
            return RoleDto(id=role.id, name=Roles(role.name))

        return None

    def assign_role(self, user_id: UUID, role_id: UUID) -> None:
        self._session.execute(
            sqla.insert(users_roles).values(user_id=user_id, role_id=role_id)
        )
