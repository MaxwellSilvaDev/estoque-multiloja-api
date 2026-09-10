from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def criar_produto(db: Session, dados: ProdutoCreate) -> Produto:
    produto = Produto(**dados.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def listar_produtos(db: Session) -> list[Produto]:
    resultado = db.execute(select(Produto))
    return list(resultado.scalars().all())


def buscar_produto_por_id(
    db: Session,
    produto_id: int
) -> Produto | None:
    return db.get(Produto, produto_id)


def atualizar_produto(
    db: Session,
    produto: Produto,
    dados: ProdutoUpdate
) -> Produto:
    campos = dados.model_dump(exclude_unset=True)

    for campo, valor in campos.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


def deletar_produto(
    db: Session,
    produto: Produto
) -> None:
    db.delete(produto)
    db.commit()