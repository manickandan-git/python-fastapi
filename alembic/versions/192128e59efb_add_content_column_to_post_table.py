"""add content column to post table

Revision ID: 192128e59efb
Revises: 5b674df7b7cd
Create Date: 2025-10-24 15:21:42.485105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '192128e59efb'
down_revision: Union[str, Sequence[str], None] = '5b674df7b7cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
