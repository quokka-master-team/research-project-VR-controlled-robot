class UserManagementDomainException(Exception):
    pass


class UserNotFound(UserManagementDomainException):
    pass


class EmailMismatch(UserManagementDomainException):
    pass
