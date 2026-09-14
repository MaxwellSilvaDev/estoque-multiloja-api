from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obter_usuario_atual
from app.api.dependencies.permissoes import validar_acesso_loja
from app.crud.loja import buscar_loja_por_id
from app.crud.produto import buscar_produto_por_id
from app.crud.movimentacao import (
    listar_movimentacoes,
    registrar_entrada,
    registrar_saida,
)
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.movimentacao import (
    MovimentacaoCreate,
    MovimentacaoResponse,
)


router = APIRouter(
    prefix="/movimentacoes",
    tags=["Movimentações"],
)


@router.get(
    "",
    response_model=list[MovimentacaoResponse],
)
def consultar_movimentacoes(
    loja_id: int | None = None,
    produto_id: int | None = None,
    tipo: str | None = None,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    if loja_id is not None:
        validar_acesso_loja(
            usuario_atual,
            loja_id,
        )

    if usuario_atual.perfil == "operador":
        loja_id = usuario_atual.loja_id

    return listar_movimentacoes(
        db,
        loja_id=loja_id,
        produto_id=produto_id,
        limit=limit,
        offset=offset,
        tipo=tipo,
    )


@router.post(
    "/entrada",
    response_model=MovimentacaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def entrada_estoque(
    dados: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    validar_acesso_loja(
        usuario_atual,
        dados.loja_id,
    )

    if buscar_produto_por_id(db, dados.produto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    if buscar_loja_por_id(db, dados.loja_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    if dados.quantidade <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A quantidade deve ser maior que zero.",
        )

    return registrar_entrada(
        db,
        dados,
    )


@router.post(
    "/saida",
    response_model=MovimentacaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def saida_estoque(
    dados: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    validar_acesso_loja(
        usuario_atual,
        dados.loja_id,
    )

    if buscar_produto_por_id(db, dados.produto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )

    if buscar_loja_por_id(db, dados.loja_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    if dados.quantidade <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A quantidade deve ser maior que zero.",
        )

    try:
        return registrar_saida(
            db,
            dados,
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )