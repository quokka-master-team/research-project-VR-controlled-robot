"""add new permissions

Revision ID: afa509c218c4
Revises: 133c768d9505
Create Date: 2023-10-11 17:47:35.349791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afa509c218c4"
down_revision: Union[str, None] = "133c768d9505"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'manage_owned_stream_units', now(), now());"""
    )
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'manage_all_stream_units', now(), now());"""
    )
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'view_stream_units', now(), now());"""
    )
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'book_stream_unit', now(), now());"""
    )

    op.execute(
        """INSERT INTO roles VALUES (gen_random_uuid(), 'stream_units_owner', now(), now())"""
    )
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'add_stream_units', now(), now());"""
    )

    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'manage_all_stream_units' WHERE r.name='admin');"""
    )
    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'view_stream_units' WHERE r.name='admin');"""
    )
    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'book_stream_unit' WHERE r.name='admin');"""
    )
    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'add_stream_units' WHERE r.name='admin');"""
    )

    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'view_stream_units' WHERE r.name='default');"""
    )
    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'book_stream_unit' WHERE r.name='default');"""
    )

    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'manage_owned_stream_units' WHERE r.name='stream_units_owner');"""
    )
    op.execute(
        """INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'add_stream_units' WHERE r.name='stream_units_owner');"""
    )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name = 'stream_units_owner'")
