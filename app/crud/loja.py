from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.loja import Loja
from app.schemas.loja import LojaCreate, LojaUpdate


def criar_loja(
    db: Session,
    dados: LojaCreate
) -> Loja:
    loja = Loja(**dados.model_dump())

    db.add(loja)
    db.commit()
    db.refresh(loja)

    return loja


def listar_lojas(
    db: Session
) -> list[Loja]:
    resultado = db.execute(
        select(Loja)
    )

    return list(resultado.scalars().all())


def buscar_loja_por_id(
    db: Session,
    loja_id: int
) -> Loja | None:
    return db.get(
        Loja,
        loja_id
    )


def atualizar_loja(
    db: Session,
    loja: Loja,
    dados: LojaUpdate
) -> Loja:
    campos = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in campos.items():
        setattr(
            loja,
            campo,
            valor
        )

    db.commit()
    db.refresh(loja)

    return loja


def deletar_loja(
    db: Session,
    loja: Loja
) -> None:
    try:
        db.delete(loja)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Não é possível excluir esta loja porque ela possui estoque ou movimentações vinculadas."
        )