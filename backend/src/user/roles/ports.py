from typing import Protocol
from uuid import UUID
from src.consts import Permissions, Roles
from src.user.roles.dtos import RoleDto


class PermissionValidator(Protocol):
    def validate_user_permission(
        self, user_id: UUID, permission: Permissions
    ) -> bool:
        ...


class RoleRepositoryInterface(Protocol):
    def get_role_by_name(self, role_name: Roles) -> RoleDto | None:
        ...

    def assign_role(self, user_id: UUID, role_id: UUID) -> None:
        ...
