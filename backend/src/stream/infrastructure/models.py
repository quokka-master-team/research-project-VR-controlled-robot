from src.core.infrastructure.database import Model
from uuid import UUID, uuid4
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from src.consts import STREAM_UNIT_NAME_MAX_LENGTH


class StreamUnit(Model):
    __tablename__ = "stream_units"
    __table_args__ = (
        sqla.PrimaryKeyConstraint("id", name="stream_unit_pkey"),
        sqla.UniqueConstraint("name", name="stream_unit_name_uniq"),
        sqla.UniqueConstraint("host", "port", name="stream_unit_host_port_uniq"),
        sqla.UniqueConstraint("api_url", name="stream_unit_api_uri_uniq"),
    )

    id: orm.Mapped[UUID] = orm.mapped_column(sqla.UUID(), default=uuid4)
    owner_id: orm.Mapped[UUID] = orm.mapped_column(sqla.UUID(), nullable=False)

    name: orm.Mapped[str] = orm.mapped_column(
        sqla.String(STREAM_UNIT_NAME_MAX_LENGTH), nullable=False
    )
    location: orm.Mapped[str] = orm.mapped_column(
        sqla.String(), nullable=False
    )
    description: orm.Mapped[str] = orm.mapped_column(
        sqla.Text(), nullable=False
    )

    secret: orm.Mapped[str] = orm.mapped_column(sqla.String(), nullable=True)

    host: orm.Mapped[str] = orm.mapped_column(sqla.String(), nullable=True)
    port: orm.Mapped[int] = orm.mapped_column(sqla.Integer(), nullable=True)
    api_url: orm.Mapped[str] = orm.mapped_column(sqla.String(), nullable=True)
