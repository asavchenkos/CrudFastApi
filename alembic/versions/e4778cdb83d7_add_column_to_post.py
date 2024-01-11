"""Add column to Post

Revision ID: e4778cdb83d7
Revises: 
Create Date: 2024-01-11 01:50:49.341653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4778cdb83d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('author', sa.String, nullable=True))

def downgrade():
    op.drop_column('posts', 'author')
