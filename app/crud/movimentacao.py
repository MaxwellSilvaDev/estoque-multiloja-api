from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estoque import Estoque
from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreate


def listar_movimentacoes(
    db: Session,
    loja_id: int | None = None,
    produto_id: int | None = None,
    limit: int = 20,
    offset: int = 0
) -> list[Movimentacao]:
    consulta = select(Movimentacao)

    if loja_id is not None:
        consulta = consulta.where(
            Movimentacao.loja_id == loja_id
        )

    if produto_id is not None:
        consulta = consulta.where(
            Movimentacao.produto_id == produto_id
        )

    consulta = (
        consulta
        .order_by(Movimentacao.data.desc())
        .limit(limit)
        .offset(offset)
    )

    resultado = db.execute(consulta)

    return list(resultado.scalars().all())


def registrar_entrada(
    db: Session,
    dados: MovimentacaoCreate
) -> Movimentacao:
    try:
        estoque = db.execute(
            select(Estoque).where(
                Estoque.produto_id == dados.produto_id,
                Estoque.loja_id == dados.loja_id
            )
        ).scalar_one_or_none()

        if estoque is None:
            estoque = Estoque(
                produto_id=dados.produto_id,
                loja_id=dados.loja_id,
                quantidade=0
            )
            db.add(estoque)
            db.flush()

        estoque.quantidade += dados.quantidade

        movimentacao = Movimentacao(
            produto_id=dados.produto_id,
            loja_id=dados.loja_id,
            tipo="entrada",
            quantidade=dados.quantidade
        )

        db.add(movimentacao)
        db.commit()
        db.refresh(movimentacao)

        return movimentacao

    except Exception:
        db.rollback()
        raise


def registrar_saida(
    db: Session,
    dados: MovimentacaoCreate
) -> Movimentacao:
    try:
        estoque = db.execute(
            select(Estoque).where(
                Estoque.produto_id == dados.produto_id,
                Estoque.loja_id == dados.loja_id
            ).with_for_update()
        ).scalar_one_or_none()

        if estoque is None:
            raise ValueError(
                "Estoque não encontrado para este produto e loja."
            )

        if estoque.quantidade < dados.quantidade:
            raise ValueError(
                "Saldo de estoque insuficiente."
            )

        estoque.quantidade -= dados.quantidade

        movimentacao = Movimentacao(
            produto_id=dados.produto_id,
            loja_id=dados.loja_id,
            tipo="saida",
            quantidade=dados.quantidade
        )

        db.add(movimentacao)
        db.commit()
        db.refresh(movimentacao)

        return movimentacao

    except Exception:
        db.rollback()
        raise