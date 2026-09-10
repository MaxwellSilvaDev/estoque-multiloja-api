from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id: Mapped[int] = mapped_column(primary_key=True)

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        nullable=False
    )

    loja_id: Mapped[int] = mapped_column(
        ForeignKey("lojas.id"),
        nullable=False
    )

    quantidade: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )

    __table_args__ = (
        UniqueConstraint(
            "produto_id",
            "loja_id",
            name="uq_estoque_produto_loja"
        ),
        CheckConstraint(
            "quantidade >= 0",
            name="ck_estoque_quantidade_nao_negativa"
        ),
    )