"""add estoque minimo

Revision ID: b8d7e843d31e
Revises: 6f3c2d8a1b5e
Create Date: 2026-09-14 15:52:13.910306

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8d7e843d31e"
down_revision: Union[str, Sequence[str], None] = "6f3c2d8a1b5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "estoques",
        sa.Column(
            "estoque_minimo",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )

    op.create_check_constraint(
        "ck_estoque_minimo_nao_negativo",
        "estoques",
        "estoque_minimo >= 0",
    )

    op.alter_column(
        "estoques",
        "estoque_minimo",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "ck_estoque_minimo_nao_negativo",
        "estoques",
        type_="check",
    )

    op.drop_column(
        "estoques",
        "estoque_minimo",
    )