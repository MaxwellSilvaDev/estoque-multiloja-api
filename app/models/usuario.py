from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    perfil: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    loja_id: Mapped[int | None] = mapped_column(
        ForeignKey("lojas.id"),
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "perfil IN ('admin', 'operador')",
            name="ck_usuarios_perfil"
        ),
        CheckConstraint(
            "perfil = 'admin' OR loja_id IS NOT NULL",
            name="ck_usuarios_operador_exige_loja"
        ),
    )