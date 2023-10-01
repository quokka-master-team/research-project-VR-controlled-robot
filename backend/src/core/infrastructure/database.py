import sqlalchemy.orm as orm
import sqlalchemy as sqla
from datetime import datetime
from src.core.utils import get_current_time
from contextlib import contextmanager
from typing import Iterator


class SessionProvider:
    """Helps to manage ORM sessions."""

    def __init__(self, engine: sqla.Engine) -> None:
        self.session_maker = orm.sessionmaker(engine)

    def create_session(self) -> orm.Session:
        return self.session_maker()

    @contextmanager
    def get_session(self) -> Iterator[orm.Session]:
        """
        Creates ORM session and closes after program get out of this context.
        Returns:
            session (Session):
        """

        session: orm.Session = self.create_session()

        yield session

        session.close()


class Model(orm.DeclarativeBase):
    """Base database ORM model"""

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sqla.DateTime, default=get_current_time
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        sqla.DateTime, default=get_current_time, onupdate=get_current_time
    )
