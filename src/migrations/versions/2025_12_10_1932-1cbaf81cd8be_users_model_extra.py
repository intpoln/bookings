"""users model extra

Revision ID: 1cbaf81cd8be
Revises: b7307a7f9626
Create Date: 2025-12-10 19:32:55.499570

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1cbaf81cd8be"
down_revision: Union[str, None] = "b7307a7f9626"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=50), nullable=False))
    op.add_column("users", sa.Column("first_name", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(length=50), nullable=True))
    op.alter_column(
        "users",
        "email",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "username")
