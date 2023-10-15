from uuid import UUID
import sqlalchemy as sqla
from src.stream.domain.dtos import StreamUnitReadModel
from src.core.infrastructure.database import SessionProvider
from src.stream.infrastructure.models import StreamUnit
from src.stream.infrastructure.mappers import stream_unit_to_read_model_mapper


class StreamUnitView:
    def __init__(self, session_provider: SessionProvider) -> None:
        self._session_provider = session_provider

    def get(self, stream_unit_id: UUID) -> StreamUnitReadModel | None:
        with self._session_provider.get_session() as session:
            if stream_unit := session.scalar(
                sqla.select(StreamUnit).where(StreamUnit.id == stream_unit_id)
            ):
                return stream_unit_to_read_model_mapper(stream_unit)

        return None


class StreamUnitListView:
    def __init__(self, session_provider: SessionProvider) -> None:
        self._session_provider = session_provider

    def get_list(self) -> list[StreamUnitReadModel]:
        with self._session_provider.get_session() as session:
            return [
                stream_unit_to_read_model_mapper(stream_unit)
                for stream_unit in session.scalars(sqla.select(StreamUnit))
            ]

    def get_user_stream_units(
        self, user_id: UUID
    ) -> list[StreamUnitReadModel]:
        with self._session_provider.get_session() as session:
            return [
                stream_unit_to_read_model_mapper(stream_unit)
                for stream_unit in session.scalars(
                    sqla.select(StreamUnit).where(
                        StreamUnit.owner_id == user_id
                    )
                )
            ]
