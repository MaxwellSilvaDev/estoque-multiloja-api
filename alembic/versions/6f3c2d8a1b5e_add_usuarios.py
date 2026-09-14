"""add usuarios

Revision ID: 6f3c2d8a1b5e
Revises: af208599f2bd
Create Date: 2026-09-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f3c2d8a1b5e"
down_revision: Union[str, Sequence[str], None] = "af208599f2bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("perfil", sa.String(length=20), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.Column("loja_id", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "perfil IN ('admin', 'operador')",
            name="ck_usuarios_perfil",
        ),
        sa.CheckConstraint(
            "perfil = 'admin' OR loja_id IS NOT NULL",
            name="ck_usuarios_operador_exige_loja",
        ),
        sa.ForeignKeyConstraint(
            ["loja_id"],
            ["lojas.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_usuarios_email"),
        "usuarios",
        ["email"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_usuarios_email"),
        table_name="usuarios",
    )

    op.drop_table("usuarios")