from typing import Protocol, Self, Any
from uuid import UUID

from src.core.types import URL
from src.stream.domain.value_objects import StreamUnitName, StreamUnitLocation
from src.stream.domain.dtos import StreamUnitReadModel, WriteStreamUnit


class Actor(Protocol):
    id: UUID


class StreamUnitRepositoryInterface(Protocol):
    def add_stream_unit(
        self,
        stream_unit_id: UUID,
        owner_id: UUID,
        name: StreamUnitName,
        location: StreamUnitLocation,
        description: str,
        video_url: URL,
        api_url: URL,
        secret: str | None,
    ) -> None:
        ...

    def stream_unit_with_unique_params_exist(
        self, name: StreamUnitName, video_url: URL, api_url: URL
    ) -> bool:
        ...


class StreamUnitViewInterface(Protocol):
    def get(self, stream_unit_id: UUID) -> StreamUnitReadModel | None:
        ...


class StreamUnitListViewInterface(Protocol):
    def get_list(self) -> list[StreamUnitReadModel]:
        ...

    def get_user_stream_units(
        self, user_id: UUID
    ) -> list[StreamUnitReadModel]:
        ...


class StreamUnitCommandServiceInterface(Protocol):
    def add_stream_unit(
        self, actor: Actor, stream_unit: WriteStreamUnit
    ) -> None:
        ...


class StreamUnitQueryServiceInterface(Protocol):
    def get(self, actor: Actor, stream_unit_id: UUID) -> StreamUnitReadModel:
        ...

    def get_list(self, actor: Actor) -> list[StreamUnitReadModel]:
        ...

    def get_actor_stream_units(
        self, actor: Actor
    ) -> list[StreamUnitReadModel]:
        ...


class StreamUnitUowInterface(Protocol):
    stream_unit_repository: StreamUnitRepositoryInterface

    def __enter__(self) -> Self:
        ...

    def __exit__(self, *args: Any) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
