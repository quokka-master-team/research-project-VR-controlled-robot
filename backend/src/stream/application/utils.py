from uuid import UUID
from abc import ABC, abstractmethod
from fastapi import WebSocket
from src.stream.domain.enums import ContentType, InfoMessage
from typing import Any


class WebSocketMessage:
    def __init__(self, message: str, content_type: ContentType) -> None:
        self._msg = message
        self._type = content_type

    def json(self) -> dict[str, Any]:
        return dict(content=self._msg, type=self._type)


class Connection:
    def __init__(self, websocket: WebSocket) -> None:
        pass


class ConnectionManager(ABC):
    @abstractmethod
    def _bind_with_stream_unit(
        self, stream_unit_id: UUID, connection: WebSocket
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def _remove_connection(self, connection: WebSocket) -> None:
        raise NotImplementedError

    @abstractmethod
    def _connection_to_stream_unit_exist(self, stream_unit_id: UUID) -> bool:
        raise NotImplementedError

    @staticmethod
    async def connect(connection: WebSocket) -> None:
        await connection.accept()
        await connection.send_json(
            WebSocketMessage(InfoMessage.connected, ContentType.info).json()
        )

    def bind_stream_unit_with_connection(
        self, stream_unit_id: UUID, connection: WebSocket
    ) -> None:
        self._bind_with_stream_unit(stream_unit_id, connection)

    async def disconnect(self, connection: WebSocket) -> None:
        await connection.send_json(
            WebSocketMessage(InfoMessage.disconnected, ContentType.info).json()
        )
        self._remove_connection(connection)
        await connection.close()

    def stream_unit_in_use(self, stream_unit_id: UUID) -> bool:
        return self._connection_to_stream_unit_exist(stream_unit_id)

    def handle_runtime_error(self, connection: WebSocket) -> None:
        self._remove_connection(connection)


class InMemoryConnectionManager(ConnectionManager):
    def __init__(self) -> None:
        self._stream_units_connections: dict[WebSocket, UUID] = {}

    def _bind_with_stream_unit(
        self, stream_unit_id: UUID, connection: WebSocket
    ) -> None:
        self._stream_units_connections[connection] = stream_unit_id

    def _remove_connection(self, connection: WebSocket) -> None:
        self._stream_units_connections.pop(connection, None)

    def _connection_to_stream_unit_exist(self, stream_unit_id: UUID) -> bool:
        return stream_unit_id in self._stream_units_connections.values()
