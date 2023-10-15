import sqlalchemy as sqla
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.types import URL
from src.stream.domain.value_objects import StreamUnitName, StreamUnitLocation
from src.stream.infrastructure.models import StreamUnit


class StreamUnitRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

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
        self._session.execute(
            sqla.insert(StreamUnit).values(
                id=stream_unit_id,
                owner_id=owner_id,
                name=name,
                location=str(location),
                description=description,
                video_url=str(video_url),
                api_url=str(api_url),
                secret=secret,
            )
        )

    def stream_unit_with_unique_params_exist(
        self, name: StreamUnitName, video_url: URL, api_url: URL
    ) -> bool:
        return self._session.query(
            sqla.exists().where(
                sqla.or_(
                    StreamUnit.name == name,
                    StreamUnit.video_url == str(video_url),
                    StreamUnit.api_url == str(api_url),
                )
            )
        ).scalar()
