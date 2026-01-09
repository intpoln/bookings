"""fixed users model

Revision ID: 511ae89b574d
Revises: 65060e712e77
Create Date: 2025-12-10 21:24:45.866700

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "511ae89b574d"
down_revision: Union[str, None] = "65060e712e77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["username"])
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
