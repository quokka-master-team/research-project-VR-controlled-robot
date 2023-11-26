class StreamUnitNameTooLong(ValueError):
    def __init__(self, msg: str = "name too long") -> None:
        super().__init__(msg)


class InvalidLocationFormat(ValueError):
    def __init__(
        self, msg: str = "invalid format, change it to '{country}, {city}'"
    ) -> None:
        super().__init__(msg)


class StreamDomainException(Exception):
    pass


class InsufficientPermissionsToGetStreamUnits(StreamDomainException):
    pass


class InsufficientPermissionsToAddStreamUnit(StreamDomainException):
    pass


class InsufficientPermissionsToStartTransmission(StreamDomainException):
    pass


class StreamUnitNotFound(StreamDomainException):
    pass


class StreamUnitAlreadyExists(StreamDomainException):
    pass


class StreamUnitInUse(StreamDomainException):
    pass
