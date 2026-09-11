from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.produto import (
    criar_produto,
    listar_produtos,
    buscar_produto_por_id,
    atualizar_produto,
    deletar_produto
)
from app.db.session import get_db
from app.schemas.produto import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate
)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post(
    "",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_produto(
    dados: ProdutoCreate,
    db: Session = Depends(get_db)
):
    try:
        return criar_produto(db, dados)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )


@router.get(
    "",
    response_model=list[ProdutoResponse]
)
def consultar_produtos(
    db: Session = Depends(get_db)
):
    return listar_produtos(db)


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def consultar_produto_por_id(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = buscar_produto_por_id(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    return produto


@router.patch(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def editar_produto(
    produto_id: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    produto = buscar_produto_por_id(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    try:
        return atualizar_produto(
            db,
            produto,
            dados
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )


@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = buscar_produto_por_id(db, produto_id)

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    try:
        deletar_produto(db, produto)

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )

    return None