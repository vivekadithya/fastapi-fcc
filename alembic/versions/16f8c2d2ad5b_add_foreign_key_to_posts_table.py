"""add foreign key to posts table

Revision ID: 16f8c2d2ad5b
Revises: 51f14e27f9f3
Create Date: 2024-09-16 18:47:43.501081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16f8c2d2ad5b'
down_revision: Union[str, None] = '51f14e27f9f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')