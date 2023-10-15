"""Add connect_to_stream_unit permission

Revision ID: b01217c92f96
Revises: afa509c218c4
Create Date: 2023-10-15 11:18:11.789645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b01217c92f96'
down_revision: Union[str, None] = 'afa509c218c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """INSERT INTO permissions VALUES (gen_random_uuid(), 'connect_to_stream_unit', now(), now());"""
    )
    op.execute("""INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'connect_to_stream_unit' WHERE r.name='admin');""")
    op.execute("""INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'connect_to_stream_unit' WHERE r.name='stream_unit_owner');""")
    op.execute("""INSERT INTO roles_permissions (role_id, permission_id) (SELECT r.id, p.id FROM roles as r JOIN permissions as p ON p.name = 'connect_to_stream_unit' WHERE r.name='default');""")


def downgrade() -> None:
    pass
