from uuid import UUID, uuid4
from src.stream.domain.ports import StreamUnitUowInterface
from src.stream.domain.ports import (
    StreamUnitViewInterface,
    StreamUnitListViewInterface,
    Actor,
)
from src.stream.domain.dtos import StreamUnitReadModel, WriteStreamUnit
from src.user_management.permissions.domain.ports import PermissionValidator
from src.user_management.permissions.domain.enums import Permissions
from src.stream.domain.exceptions import (
    InsufficientPermissionsToGetStreamUnits,
    StreamUnitNotFound,
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
                video_url=stream_unit.video_url,
                api_url=stream_unit.api_url,
            ):
                raise StreamUnitAlreadyExists

            uow.stream_unit_repository.add_stream_unit(
                stream_unit_id=uuid4(),
                owner_id=actor.id,
                name=stream_unit.name,
                location=stream_unit.location,
                description=stream_unit.description,
                video_url=stream_unit.video_url,
                api_url=stream_unit.api_url,
                secret=stream_unit.secret,
            )
            uow.commit()


class StreamUnitQueryService:
    def __init__(
        self,
        view: StreamUnitViewInterface,
        list_view: StreamUnitListViewInterface,
        permission_validator: PermissionValidator,
    ) -> None:
        self._view = view
        self._list_view = list_view
        self._permission_validator = permission_validator

    def get(self, actor: Actor, stream_unit_id: UUID) -> StreamUnitReadModel:
        if not self._permission_validator.validate(
            actor.id, Permissions.view_stream_units
        ):
            raise InsufficientPermissionsToGetStreamUnits

        if stream_unit := self._view.get(stream_unit_id):
            return stream_unit

        raise StreamUnitNotFound

    def get_list(self, actor: Actor) -> list[StreamUnitReadModel]:
        if not self._permission_validator.validate(
            actor.id, Permissions.view_stream_units
        ):
            raise InsufficientPermissionsToGetStreamUnits

        return self._list_view.get_list()

    def get_actor_stream_units(
        self, actor: Actor
    ) -> list[StreamUnitReadModel]:
        if self._permission_validator.validate(
            actor.id, Permissions.manage_all_stream_units
        ):
            return self._list_view.get_list()

        if self._permission_validator.validate(
            actor.id, Permissions.manage_owned_stream_units
        ):
            return self._list_view.get_user_stream_units(actor.id)

        raise InsufficientPermissionsToGetStreamUnits
