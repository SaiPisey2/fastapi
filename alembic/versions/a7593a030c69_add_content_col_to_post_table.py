"""add content col to post table

Revision ID: a7593a030c69
Revises: b13924d35086
Create Date: 2024-11-12 21:25:49.540496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7593a030c69'
down_revision: Union[str, None] = 'b13924d35086'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
