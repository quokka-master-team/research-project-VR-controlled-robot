from enum import StrEnum


class ContentType(StrEnum):
    data = "DATA"
    info = "INFO"
    error = "ERROR"


class InfoMessage(StrEnum):
    connected = "Connection established"
    disconnected = "Connection closed"
