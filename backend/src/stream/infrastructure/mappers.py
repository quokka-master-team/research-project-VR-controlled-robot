from typing import TYPE_CHECKING
from src.stream.domain.dtos import StreamUnitReadModel, StreamUnitDto
from src.core.types import URL
from src.stream.domain.value_objects import StreamUnitName, StreamUnitLocation

if TYPE_CHECKING:
    from src.stream.infrastructure.models import StreamUnit


def stream_unit_to_dto_mapper(stream_unit: "StreamUnit") -> StreamUnitDto:
    return StreamUnitDto(
        id=stream_unit.id,
        secret=stream_unit.secret,
        host=stream_unit.host,
        port=stream_unit.port,
        api_url=URL(stream_unit.api_url),
    )


def stream_unit_to_read_model_mapper(
    stream_unit: "StreamUnit",
) -> StreamUnitReadModel:
    return StreamUnitReadModel(
        id=stream_unit.id,
        name=StreamUnitName(stream_unit.name),
        description=stream_unit.description,
        location=StreamUnitLocation(stream_unit.location),
    )
