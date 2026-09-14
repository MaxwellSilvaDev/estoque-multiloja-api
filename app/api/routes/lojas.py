from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obter_usuario_atual
from app.api.dependencies.permissoes import (
    exigir_admin,
    validar_acesso_loja,
)
from app.crud.loja import (
    atualizar_loja,
    buscar_loja_por_id,
    criar_loja,
    deletar_loja,
    listar_lojas,
)
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.loja import (
    LojaCreate,
    LojaResponse,
    LojaUpdate,
)


router = APIRouter(
    prefix="/lojas",
    tags=["Lojas"],
)


@router.post(
    "",
    response_model=LojaResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_loja(
    dados: LojaCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
):
    return criar_loja(
        db,
        dados,
    )


@router.get(
    "",
    response_model=list[LojaResponse],
)
def consultar_lojas(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    if usuario_atual.perfil == "operador":
        loja = buscar_loja_por_id(
            db,
            usuario_atual.loja_id,
        )

        if loja is None:
            return []

        return [loja]

    return listar_lojas(
        db,
    )


@router.get(
    "/{loja_id}",
    response_model=LojaResponse,
)
def consultar_loja_por_id(
    loja_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    validar_acesso_loja(
        usuario_atual=usuario_atual,
        loja_id=loja_id,
    )

    loja = buscar_loja_por_id(
        db,
        loja_id,
    )

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    return loja


@router.patch(
    "/{loja_id}",
    response_model=LojaResponse,
)
def editar_loja(
    loja_id: int,
    dados: LojaUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
):
    loja = buscar_loja_por_id(
        db,
        loja_id,
    )

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    return atualizar_loja(
        db,
        loja,
        dados,
    )


@router.delete(
    "/{loja_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_loja(
    loja_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
):
    loja = buscar_loja_por_id(
        db,
        loja_id,
    )

    if loja is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada.",
        )

    try:
        deletar_loja(
            db,
            loja,
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        )

    return None