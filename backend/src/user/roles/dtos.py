from dataclasses import dataclass
from uuid import UUID
from src.consts import Roles


@dataclass
class RoleDto:
    id: UUID
    name: Roles
