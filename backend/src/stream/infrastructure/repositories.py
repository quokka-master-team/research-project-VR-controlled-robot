import sqlalchemy as sqla
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.types import URL
from src.stream.domain.value_objects import StreamUnitName, StreamUnitLocation
from src.stream.infrastructure.models import StreamUnit
from src.stream.domain.dtos import StreamUnitDto
from src.stream.infrastructure.mappers import stream_unit_to_dto_mapper


class StreamUnitRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_stream_unit(self, stream_unit_id: UUID) -> StreamUnitDto | None:
        if stream_unit := self._session.scalar(
            sqla.select(StreamUnit).where(StreamUnit.id == stream_unit_id)
        ):
            return stream_unit_to_dto_mapper(stream_unit)
        return None

    def add_stream_unit(
        self,
        stream_unit_id: UUID,
        owner_id: UUID,
        name: StreamUnitName,
        location: StreamUnitLocation,
        description: str,
        host: str,
        port: int,
        api_url: URL,
        secret: str | None,
    ) -> None:
        self._session.execute(
            sqla.insert(StreamUnit).values(
                id=stream_unit_id,
                owner_id=owner_id,
                name=name,
                location=str(location),
                description=description,
                host=host,
                port=port,
                api_url=str(api_url),
                secret=secret,
            )
        )

    def stream_unit_with_unique_params_exist(
        self, name: StreamUnitName, host: str, port: int, api_url: URL
    ) -> bool:
        return self._session.query(
            sqla.exists().where(
                sqla.or_(
                    StreamUnit.name == name,
                    StreamUnit.api_url == str(api_url),
                    sqla.and_(
                        StreamUnit.port == port, StreamUnit.host == host
                    ),
                )
            )
        ).scalar()
