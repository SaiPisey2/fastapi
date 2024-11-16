"""add user table

Revision ID: 80899a0a9f00
Revises: a7593a030c69
Create Date: 2024-11-12 21:36:04.138722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80899a0a9f00'
down_revision: Union[str, None] = 'a7593a030c69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
