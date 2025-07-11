"""add votes table

Revision ID: 549ea69f6a55
Revises: 4ef74a32c3ad
Create Date: 2025-07-11 13:36:44.874747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '549ea69f6a55'
down_revision: Union[str, Sequence[str], None] = '4ef74a32c3ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema: Create votes table."""
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    )

def downgrade() -> None:
    """Downgrade schema: Drop votes table."""
    op.drop_table('votes')