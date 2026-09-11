from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def criar_produto(
    db: Session,
    dados: ProdutoCreate
) -> Produto:
    produto = Produto(**dados.model_dump())

    try:
        db.add(produto)
        db.commit()
        db.refresh(produto)

        return produto

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Já existe um produto com este SKU."
        )


def listar_produtos(
    db: Session
) -> list[Produto]:
    resultado = db.execute(
        select(Produto)
    )

    return list(resultado.scalars().all())


def buscar_produto_por_id(
    db: Session,
    produto_id: int
) -> Produto | None:
    return db.get(
        Produto,
        produto_id
    )


def atualizar_produto(
    db: Session,
    produto: Produto,
    dados: ProdutoUpdate
) -> Produto:
    campos = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in campos.items():
        setattr(
            produto,
            campo,
            valor
        )

    try:
        db.commit()
        db.refresh(produto)

        return produto

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Já existe um produto com este SKU."
        )


def deletar_produto(
    db: Session,
    produto: Produto
) -> None:
    try:
        db.delete(produto)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Não é possível excluir este produto porque ele possui estoque ou movimentações vinculadas."
        )