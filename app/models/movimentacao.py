from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id: Mapped[int] = mapped_column(primary_key=True)

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False
    )

    loja_id: Mapped[int] = mapped_column(
        ForeignKey("lojas.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        nullable=False
    )

    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('entrada', 'saida', 'ajuste')",
            name="ck_movimentacoes_tipo"
        ),
        CheckConstraint(
            "quantidade > 0",
            name="ck_movimentacoes_quantidade_positiva"
        ),
    )