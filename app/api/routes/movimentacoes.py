from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.loja import buscar_loja_por_id
from app.crud.produto import buscar_produto_por_id
from app.crud.movimentacao import (
    listar_movimentacoes,
    registrar_entrada,
    registrar_saida
)
from app.db.session import get_db
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse


router = APIRouter(
    prefix="/movimentacoes",
    tags=["Movimentações"]
)


@router.get(
    "",
    response_model=list[MovimentacaoResponse]
)
def consultar_movimentacoes(
    loja_id: int | None = None,
    produto_id: int | None = None,
    db: Session = Depends(get_db)
):
    return listar_movimentacoes(
        db,
        loja_id=loja_id,
        produto_id=produto_id
    )


@router.post(
    "/entrada",
    response_model=MovimentacaoResponse,
    status_code=status.HTTP_201_CREATED
)
def entrada_estoque(
    dados: MovimentacaoCreate,
    db: Session = Depends(get_db)
):
    if buscar_produto_por_id(db, dados.produto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    if buscar_loja_por_id(db, dados.loja_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    if dados.quantidade <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A quantidade deve ser maior que zero."
        )

    return registrar_entrada(db, dados)


@router.post(
    "/saida",
    response_model=MovimentacaoResponse,
    status_code=status.HTTP_201_CREATED
)
def saida_estoque(
    dados: MovimentacaoCreate,
    db: Session = Depends(get_db)
):
    if buscar_produto_por_id(db, dados.produto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    if buscar_loja_por_id(db, dados.loja_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada."
        )

    if dados.quantidade <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A quantidade deve ser maior que zero."
        )

    try:
        return registrar_saida(db, dados)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )