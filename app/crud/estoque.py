from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estoque import Estoque


def buscar_estoque(
    db: Session,
    produto_id: int,
    loja_id: int,
) -> Estoque | None:
    resultado = db.execute(
        select(Estoque).where(
            Estoque.produto_id == produto_id,
            Estoque.loja_id == loja_id,
        )
    )

    return resultado.scalar_one_or_none()


def listar_estoque_por_loja(
    db: Session,
    loja_id: int,
) -> list[Estoque]:
    resultado = db.execute(
        select(Estoque).where(
            Estoque.loja_id == loja_id,
        )
    )

    return list(resultado.scalars().all())


def listar_estoques_baixos_por_loja(
    db: Session,
    loja_id: int,
) -> list[Estoque]:
    resultado = db.execute(
        select(Estoque).where(
            Estoque.loja_id == loja_id,
            Estoque.estoque_minimo > 0,
            Estoque.quantidade <= Estoque.estoque_minimo,
        )
    )

    return list(resultado.scalars().all())


def atualizar_estoque_minimo(
    db: Session,
    estoque: Estoque,
    estoque_minimo: int,
) -> Estoque:
    estoque.estoque_minimo = estoque_minimo

    db.commit()
    db.refresh(estoque)

    return estoque