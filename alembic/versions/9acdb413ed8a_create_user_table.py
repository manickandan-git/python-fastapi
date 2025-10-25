"""create user table

Revision ID: 9acdb413ed8a
Revises: 192128e59efb
Create Date: 2025-10-24 15:28:46.028738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9acdb413ed8a'
down_revision: Union[str, Sequence[str], None] = '192128e59efb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))  
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
