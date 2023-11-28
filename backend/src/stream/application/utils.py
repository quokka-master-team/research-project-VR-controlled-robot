from uuid import UUID
from abc import ABC, abstractmethod


class ConnectionManager(ABC):
    @abstractmethod
    def _bind_with_stream_unit(
        self, stream_unit_id: UUID, actor_id: UUID
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def _connection_to_stream_unit_exist(self, stream_unit_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _release_stream_unit(self, actor_id: UUID) -> None:
        raise NotImplementedError

    def bind_stream_unit_with_actor(
        self, stream_unit_id: UUID, actor_id: UUID
    ) -> None:
        self._bind_with_stream_unit(stream_unit_id, actor_id)

    def release_stream_unit(self, actor_id: UUID) -> None:
        self._release_stream_unit(actor_id)

    def stream_unit_in_use(self, stream_unit_id: UUID) -> bool:
        return self._connection_to_stream_unit_exist(stream_unit_id)


class InMemoryConnectionManager(ConnectionManager):
    def __init__(self) -> None:
        self._stream_units_connections: dict[UUID, UUID] = {}

    def _bind_with_stream_unit(
        self, stream_unit_id: UUID, actor_id: UUID
    ) -> None:
        self._stream_units_connections[actor_id] = stream_unit_id

    def _release_stream_unit(self, actor_id: UUID) -> None:
        self._stream_units_connections.pop(actor_id, None)

    def _connection_to_stream_unit_exist(self, stream_unit_id: UUID) -> bool:
        return stream_unit_id in self._stream_units_connections.values()
