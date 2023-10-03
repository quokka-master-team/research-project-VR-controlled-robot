from dataclasses import dataclass
from uuid import UUID
from src.user_management.permissions.domain.enums import Roles


@dataclass
class RoleDto:
    id: UUID
    name: Roles
