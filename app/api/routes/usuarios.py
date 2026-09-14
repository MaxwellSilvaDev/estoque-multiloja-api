from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.permissoes import exigir_admin
from app.crud.usuario import (
    atualizar_usuario,
    buscar_usuario_por_id,
    criar_usuario,
    listar_usuarios,
)
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
)


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
) -> Usuario:
    try:
        return criar_usuario(
            db,
            dados,
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        )


@router.get(
    "",
    response_model=list[UsuarioResponse],
)
def obter_usuarios(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
) -> list[Usuario]:
    return listar_usuarios(
        db,
    )


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
)
def obter_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
) -> Usuario:
    usuario = buscar_usuario_por_id(
        db,
        usuario_id,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return usuario


@router.patch(
    "/{usuario_id}",
    response_model=UsuarioResponse,
)
def editar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(exigir_admin),
) -> Usuario:
    usuario = atualizar_usuario(
        db,
        usuario_id,
        dados,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return usuario