from uuid import UUID
from fastapi import WebSocket
from src.stream.domain.ports import StreamUnitUowInterface, Actor
from src.stream.application.utils import ConnectionManager
from src.stream.domain.exceptions import (
    StreamUnitInUse,
    StreamUnitNotFound,
    InsufficientPermissionsToStartTransmission
)
from src.user_management.permissions.domain.ports import PermissionValidator
from src.user_management.permissions.domain.enums import Permissions
from src.stream.domain.entites import Transmission
from src.stream.domain.dtos import StreamUnitDto
from src.config import Settings
from src.stream.api.messages import Errors
from src.core.api.messages import ApiErrors, BaseError
from src.auth.exceptions import InvalidToken
from src.auth.ports import IAMTokenVerificationService
from base64 import b64encode


class StreamingService:
    def __init__(
        self,
        uow: StreamUnitUowInterface,
        connection_manager: ConnectionManager,
        permission_validator: PermissionValidator,
        token_verification: IAMTokenVerificationService,
        settings: Settings,
    ) -> None:
        self._uow = uow
        self._connection_manager = connection_manager
        self._permission_validator = permission_validator
        self._token_verification = token_verification
        self._settings = settings

    @staticmethod
    def _transmit() -> bool:
        return True

    @staticmethod
    async def _send_error_message_and_disconnect(
        connection: WebSocket, message: BaseError
    ) -> None:
        await connection.send_text(message)
        await connection.close()

    def _authorize_user(self, token: str) -> Actor:
        actor = self._token_verification.process_token(token)

        if not self._permission_validator.validate(
            actor.id, Permissions.connect_to_stream_unit
        ):
            raise InsufficientPermissionsToStartTransmission

        return actor

    def _validate_actor_can_start_transmission(
            self, stream_unit_id: UUID
    ) -> None:
        if self._connection_manager.stream_unit_in_use(stream_unit_id):
            raise StreamUnitInUse

    def _get_stream_unit(self, stream_unit_id: UUID) -> StreamUnitDto:
        with self._uow as uow:
            stream_unit = uow.stream_unit_repository.get_stream_unit(
                stream_unit_id
            )

        if not stream_unit:
            raise StreamUnitNotFound

        return stream_unit

    async def _start_transmission(
            self, stream_unit: StreamUnitDto, connection: WebSocket
    ) -> None:
        with Transmission(stream_unit, self._settings) as t:
            for packet in t.av_container.demux(video=0):
                for frame in packet.decode():
                    await connection.send_bytes(frame)
                    await connection.receive()

    async def start(
            self, token: str, stream_unit_id: UUID, connection: WebSocket
    ) -> None:
        try:
            actor = self._authorize_user(token)
            self._validate_actor_can_start_transmission(stream_unit_id)
        except InvalidToken:
            await self._send_error_message_and_disconnect(
                connection, ApiErrors.unauthorized
            )

        except InsufficientPermissionsToStartTransmission:
            await self._send_error_message_and_disconnect(
                connection,
                Errors.insufficient_permissions_to_start_transmission,
            )

        except StreamUnitInUse:
            await self._send_error_message_and_disconnect(
                connection, Errors.stream_unit_in_use
            )

        try:
            self._connection_manager.bind_stream_unit_with_actor(stream_unit_id, actor.id)
            stream_unit = self._get_stream_unit(stream_unit_id)
            await self._start_transmission(stream_unit, connection)

        except StreamUnitNotFound:
            await self._send_error_message_and_disconnect(
                connection, Errors.stream_unit_not_found
            )

        finally:
            self._connection_manager.release_stream_unit(actor.id)
            await connection.close()
