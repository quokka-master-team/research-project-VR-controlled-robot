from typing import Any
from src.stream.domain.dtos import StreamUnitDto


class Transmission:
    def __init__(self, unit: StreamUnitDto) -> None:
        self._unit = unit

    @staticmethod
    def receive_data() -> Any:
        return "content"
