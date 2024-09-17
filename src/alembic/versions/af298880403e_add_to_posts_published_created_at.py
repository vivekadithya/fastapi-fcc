"""add to posts - published, created_at

Revision ID: af298880403e
Revises: 16f8c2d2ad5b
Create Date: 2024-09-16 18:57:34.385692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af298880403e'
down_revision: Union[str, None] = '16f8c2d2ad5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()"))
    sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False)


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="created_at")
    op.drop_column(table_name="posts", column_name="published")