class UserDomainException(Exception):
    pass


class UserNotFound(UserDomainException):
    pass


class EmailMismatch(UserDomainException):
    pass
