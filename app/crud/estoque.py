from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estoque import Estoque


def buscar_estoque(
    db: Session,
    produto_id: int,
    loja_id: int
) -> Estoque | None:
    resultado = db.execute(
        select(Estoque).where(
            Estoque.produto_id == produto_id,
            Estoque.loja_id == loja_id
        )
    )

    return resultado.scalar_one_or_none()


def listar_estoque_por_loja(
    db: Session,
    loja_id: int
) -> list[Estoque]:
    resultado = db.execute(
        select(Estoque).where(
            Estoque.loja_id == loja_id
        )
    )

    return list(resultado.scalars().all())