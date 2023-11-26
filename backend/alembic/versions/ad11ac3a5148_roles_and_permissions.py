"""roles and permissions

Revision ID: ad11ac3a5148
Revises: 9905f06718fa
Create Date: 2023-09-05 18:58:41.466911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ad11ac3a5148"
down_revision: Union[str, None] = "9905f06718fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="permission_pkey"),
        sa.UniqueConstraint("name", name="permissions_name_unique"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="role_pkey"),
        sa.UniqueConstraint("name", name="role_name_unique"),
    )
    op.create_table(
        "roles_permissions",
        sa.Column("role_id", sa.UUID(), nullable=True),
        sa.Column("permission_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
    )
    op.create_table(
        "users_roles",
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("role_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
    )
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'test_permission', now(), now());"""
    )
    op.execute(
        """INSERT INTO roles VALUES (gen_random_uuid(), 'admin', now(), now())"""
    )
    op.execute(
        """INSERT INTO roles VALUES (gen_random_uuid(), 'default', now(), now())"""
    )
    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'test_permission' WHERE r.name='admin');"""
    )


def downgrade() -> None:
    op.drop_table("users_roles")
    op.drop_table("roles_permissions")
    op.drop_table("roles")
    op.drop_table("permissions")
