"""add content colum to post table

Revision ID: a8dc5127eeb4
Revises: e13a3746bf37
Create Date: 2025-07-11 13:06:57.105447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8dc5127eeb4'
down_revision: Union[str, Sequence[str], None] = 'e13a3746bf37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('posts','content')
    pass
