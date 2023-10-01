import sqlalchemy as sqla
import sqlalchemy.orm as orm
from src.core.infrastructure.database import Model
from uuid import UUID, uuid4


roles_permissions = sqla.Table(
    "roles_permissions",
    Model.metadata,
    sqla.Column("role_id", sqla.ForeignKey("roles.id")),
    sqla.Column("permission_id", sqla.ForeignKey("permissions.id")),
)


users_roles = sqla.Table(
    "users_roles",
    Model.metadata,
    sqla.Column("user_id", sqla.ForeignKey("users.id")),
    sqla.Column("role_id", sqla.ForeignKey("roles.id")),
)


class Permission(Model):
    __tablename__ = "permissions"
    __table_args__ = (
        sqla.PrimaryKeyConstraint("id", name="permission_pkey"),
        sqla.UniqueConstraint("name", name="permissions_name_unique"),
    )

    id: orm.Mapped[UUID] = orm.mapped_column(sqla.UUID(), default=uuid4)
    name: orm.Mapped[str] = orm.mapped_column(sqla.String(), nullable=False)


class Role(Model):
    """Permissions aggregate"""

    __tablename__ = "roles"
    __table_args__ = (
        sqla.PrimaryKeyConstraint("id", name="role_pkey"),
        sqla.UniqueConstraint("name", name="role_name_unique"),
    )

    id: orm.Mapped[UUID] = orm.mapped_column(sqla.UUID(), default=uuid4())
    name: orm.Mapped[str] = orm.mapped_column(sqla.String(), nullable=False)
    permissions: orm.Mapped[list[Permission]] = orm.relationship(
        secondary=roles_permissions
    )
