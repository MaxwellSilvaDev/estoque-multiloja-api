from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.loja import (
    criar_loja,
    listar_lojas,
    buscar_loja_por_id,
    atualizar_loja,
    deletar_loja
)
from app.db.session import get_db
from app.schemas.loja import LojaCreate, LojaResponse, LojaUpdate


router = APIRouter(
    prefix="/lojas",
    tags=["Lojas"]
)


@router.post(
    "",
    response_model=LojaResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_loja(
    dados: LojaCreate,
    db: Session = Depends(get_db)
):
    return criar_loja(db, dados)


@router.get(
    "",
    response_model=list[LojaResponse]
)
def consultar_lojas(
    db: Session = Depends(get_db)
):
    return listar_lojas(db)


@router.get(
    "/{loja_id}",
    response_model=LojaResponse
)
def consultar_loja_por_id(
    loja_id: int,
    db: Session = Depends(get_db)
):
    loja = buscar_loja_por_id(db, loja_id)

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    return loja


@router.patch(
    "/{loja_id}",
    response_model=LojaResponse
)
def editar_loja(
    loja_id: int,
    dados: LojaUpdate,
    db: Session = Depends(get_db)
):
    loja = buscar_loja_por_id(db, loja_id)

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    return atualizar_loja(db, loja, dados)


@router.delete(
    "/{loja_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_loja(
    loja_id: int,
    db: Session = Depends(get_db)
):
    loja = buscar_loja_por_id(db, loja_id)

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    deletar_loja(db, loja)

    return None