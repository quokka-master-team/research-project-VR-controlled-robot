from src.core.infrastructure.database import Model
from uuid import UUID, uuid4
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from src.consts import EMAIL_MAX_LENGTH


class User(Model):
    __tablename__ = "users"
    __table_args__ = (
        sqla.PrimaryKeyConstraint("id", name="user_pkey"),
        sqla.UniqueConstraint("iam_id", name="user_iam_id_unique"),
        sqla.UniqueConstraint("email", name="user_email_unique"),
    )

    id: orm.Mapped[UUID] = orm.mapped_column(sqla.UUID(), default=uuid4)
    iam_id: orm.Mapped[str] = orm.mapped_column(sqla.String())

    email: orm.Mapped[str] = orm.mapped_column(sqla.String(EMAIL_MAX_LENGTH))
