from typing import TYPE_CHECKING
from dataclasses import dataclass
from uuid import UUID
from typing import Self
from pydantic import BaseModel

from src.core.types import URL
from src.stream.domain.value_objects import StreamUnitName, StreamUnitLocation

if TYPE_CHECKING:
    from src.stream.api.models import PostStreamUnit


@dataclass(frozen=True)
class StreamUnitDto:
    id: UUID
    host: str
    port: int
    api_url: URL
    secret: str | None


class StreamUnitReadModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: UUID
    name: StreamUnitName
    description: str
    location: StreamUnitLocation


@dataclass(frozen=True)
class WriteStreamUnit:
    name: StreamUnitName
    description: str
    location: StreamUnitLocation
    host: str
    port: int
    api_url: URL
    secret: str | None

    @classmethod
    def from_post_stream_unit_model(
        cls, stream_unit: "PostStreamUnit"
    ) -> Self:
        return cls(
            name=StreamUnitName(stream_unit.name),
            description=stream_unit.description,
            location=StreamUnitLocation(stream_unit.location),
            host=stream_unit.host,
            port=stream_unit.port,
            api_url=URL(stream_unit.api_url),
            secret=stream_unit.secret,
        )
