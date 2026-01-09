"""pass changed to hash_pass

Revision ID: 65060e712e77
Revises: 1cbaf81cd8be
Create Date: 2025-12-10 20:45:49.719004

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "65060e712e77"
down_revision: Union[str, None] = "1cbaf81cd8be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("hashed_password", sa.String(length=100), nullable=False))
    op.drop_column("users", "password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("password", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.drop_column("users", "hashed_password")
