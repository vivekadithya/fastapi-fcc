"""add content column to posts table

Revision ID: 36c5fdb2c304
Revises: e1818d9bd0e3
Create Date: 2024-09-15 22:37:32.925788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36c5fdb2c304'
down_revision: Union[str, None] = 'e1818d9bd0e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
