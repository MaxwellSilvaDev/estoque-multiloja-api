from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.estoque import (
    buscar_estoque,
    listar_estoque_por_loja
)
from app.db.session import get_db
from app.schemas.estoque import EstoqueResponse


router = APIRouter(
    prefix="/estoques",
    tags=["Estoques"]
)


@router.get(
    "/loja/{loja_id}",
    response_model=list[EstoqueResponse]
)
def consultar_estoque_da_loja(
    loja_id: int,
    db: Session = Depends(get_db)
):
    return listar_estoque_por_loja(db, loja_id)


@router.get(
    "/loja/{loja_id}/produto/{produto_id}",
    response_model=EstoqueResponse
)
def consultar_estoque_do_produto(
    loja_id: int,
    produto_id: int,
    db: Session = Depends(get_db)
):
    estoque = buscar_estoque(
        db,
        produto_id=produto_id,
        loja_id=loja_id
    )

    if estoque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado."
        )

    return estoque