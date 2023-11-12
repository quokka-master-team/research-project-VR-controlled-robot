from uuid import UUID
from pydantic import BaseModel, field_validator
from src.stream.domain.value_objects import StreamUnitName, StreamUnitLocation
from src.core.api.models import ResponseModel
from src.core.types import URL


class PostStreamUnit(BaseModel):
    name: str
    location: str
    description: str
    host: str
    port: int
    api_url: str
    secret: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        StreamUnitName(value)
        return value

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str) -> str:
        StreamUnitLocation(value)
        return value


class StreamUnit(ResponseModel):
    id: UUID
    name: str
    location: str
    description: str
