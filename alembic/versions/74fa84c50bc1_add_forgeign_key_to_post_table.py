"""add foreign key to post table

Revision ID: 74fa84c50bc1
Revises: ddbd3459ab07
Create Date: 2025-07-11 13:23:33.879206
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '74fa84c50bc1'
down_revision: Union[str, Sequence[str], None] = 'ddbd3459ab07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema: Add owner_id foreign key to posts."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_users_fk',
        source_table="posts",
        referent_table="users",
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    """Downgrade schema: Remove owner_id foreign key from posts."""
    op.drop_constraint('post_users_fk', "posts", type_="foreignkey")
    op.drop_column('posts', 'owner_id')
