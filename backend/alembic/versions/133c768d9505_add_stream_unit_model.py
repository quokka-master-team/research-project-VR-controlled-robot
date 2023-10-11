"""add stream unit model

Revision ID: 133c768d9505
Revises: ad11ac3a5148
Create Date: 2023-10-11 17:30:33.668827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '133c768d9505'
down_revision: Union[str, None] = 'ad11ac3a5148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stream_units',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('secret', sa.String(), nullable=True),
        sa.Column('video_url', sa.String(), nullable=False),
        sa.Column('api_url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='stream_unit_pkey'),
        sa.UniqueConstraint('api_url', name='stream_unit_api_uri_uniq'),
        sa.UniqueConstraint('name', name='stream_unit_name_uniq'),
        sa.UniqueConstraint('video_url', name='stream_unit_video_uri_uniq')
    )


def downgrade() -> None:
    op.drop_table('stream_units')
