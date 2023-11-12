from uuid import uuid4
from src.stream.domain.ports import StreamUnitUowInterface
from src.stream.domain.ports import (
    Actor,
)
from src.stream.domain.dtos import WriteStreamUnit
from src.user_management.permissions.domain.ports import PermissionValidator
from src.user_management.permissions.domain.enums import Permissions
from src.stream.domain.exceptions import (
    InsufficientPermissionsToAddStreamUnit,
    StreamUnitAlreadyExists,
)


class StreamUnitCommandService:
    def __init__(
        self,
        uow: StreamUnitUowInterface,
        permission_validator: PermissionValidator,
    ) -> None:
        self._uow = uow
        self._permission_validator = permission_validator

    def add_stream_unit(
        self, actor: Actor, stream_unit: WriteStreamUnit
    ) -> None:
        if not self._permission_validator.validate(
            actor.id, Permissions.add_stream_units
        ):
            raise InsufficientPermissionsToAddStreamUnit

        with self._uow as uow:
            if uow.stream_unit_repository.stream_unit_with_unique_params_exist(
                name=stream_unit.name,
                host=stream_unit.host,
                port=stream_unit.port,
                api_url=stream_unit.api_url,
            ):
                raise StreamUnitAlreadyExists

            uow.stream_unit_repository.add_stream_unit(
                stream_unit_id=uuid4(),
                owner_id=actor.id,
                name=stream_unit.name,
                location=stream_unit.location,
                description=stream_unit.description,
                host=stream_unit.host,
                port=stream_unit.port,
                api_url=stream_unit.api_url,
                secret=stream_unit.secret,
            )
            uow.commit()
