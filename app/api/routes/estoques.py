from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obter_usuario_atual
from app.api.dependencies.permissoes import (
    exigir_admin,
    validar_acesso_loja,
)
from app.crud.estoque import (
    atualizar_estoque_minimo,
    buscar_estoque,
    listar_estoque_por_loja,
    listar_estoques_baixos_por_loja,
)
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.estoque import (
    EstoqueMinimoUpdate,
    EstoqueResponse,
)


router = APIRouter(
    prefix="/estoques",
    tags=["Estoques"],
)


@router.get(
    "/loja/{loja_id}",
    response_model=list[EstoqueResponse],
)
def consultar_estoque_da_loja(
    loja_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    validar_acesso_loja(
        usuario_atual,
        loja_id,
    )

    return listar_estoque_por_loja(
        db,
        loja_id,
    )


@router.get(
    "/loja/{loja_id}/alertas/baixo",
    response_model=list[EstoqueResponse],
)
def consultar_estoques_baixos_da_loja(
    loja_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    validar_acesso_loja(
        usuario_atual,
        loja_id,
    )

    return listar_estoques_baixos_por_loja(
        db,
        loja_id,
    )


@router.get(
    "/loja/{loja_id}/produto/{produto_id}",
    response_model=EstoqueResponse,
)
def consultar_estoque_do_produto(
    loja_id: int,
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    validar_acesso_loja(
        usuario_atual,
        loja_id,
    )

    estoque = buscar_estoque(
        db,
        produto_id=produto_id,
        loja_id=loja_id,
    )

    if estoque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado.",
        )

    return estoque


@router.patch(
    "/loja/{loja_id}/produto/{produto_id}/minimo",
    response_model=EstoqueResponse,
)
def configurar_estoque_minimo(
    loja_id: int,
    produto_id: int,
    dados: EstoqueMinimoUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
):
    estoque = buscar_estoque(
        db,
        produto_id=produto_id,
        loja_id=loja_id,
    )

    if estoque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado.",
        )

    return atualizar_estoque_minimo(
        db,
        estoque,
        dados.estoque_minimo,
    )