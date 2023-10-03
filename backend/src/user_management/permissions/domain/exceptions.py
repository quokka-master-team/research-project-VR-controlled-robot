from src.user_management.users.domain.exceptions import (
    UserManagementDomainException,
)


class RoleNotFound(UserManagementDomainException):
    pass
