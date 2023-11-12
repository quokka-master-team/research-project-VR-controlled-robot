from typing import Any, Self
from src.stream.domain.dtos import StreamUnitDto
import socket


BUFF_SIZE = 65536
TIMEOUT = 10


class Transmission:
    def __init__(self, unit: StreamUnitDto) -> None:
        self._unit = unit

    def __enter__(self) -> Self:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self._client.settimeout(TIMEOUT)
        self._client.connect((self._unit.host, self._unit.port))
        return self

    def __exit__(self, *args) -> None:
        self._client.close()

    def receive_data(self) -> Any:
        return self._client.recvfrom(BUFF_SIZE)
