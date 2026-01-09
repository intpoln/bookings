"""bookings model added column

Revision ID: c3bcb16f69fe
Revises: 6c19a5219dbb
Create Date: 2025-12-23 17:14:44.332576

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = "c3bcb16f69fe"
down_revision: Union[str, None] = "6c19a5219dbb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=func.now()),
    )


def downgrade() -> None:
    op.drop_column("bookings", "created_at")
