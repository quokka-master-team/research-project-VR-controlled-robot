class MaximumLengthExceeded(Exception):
    pass


class InvalidEmail(TypeError):
    pass


class InvalidURL(ValueError):
    def __init__(self, msg: str = "invalid URL") -> None:
        super().__init__(msg)
