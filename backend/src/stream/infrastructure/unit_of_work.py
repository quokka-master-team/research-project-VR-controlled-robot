from typing import Self

from src.core.infrastructure.unit_of_work import UnitOfWork
from src.stream.infrastructure.repositories import StreamUnitRepository


class StreamUnitUow(UnitOfWork):
    def __enter__(self) -> Self:
        self._session = self._session_provider.create_session()
        self.stream_unit_repository = StreamUnitRepository(self._session)

        return self
