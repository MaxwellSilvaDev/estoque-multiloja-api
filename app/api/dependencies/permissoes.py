from fastapi import Depends, HTTPException, status

from app.api.dependencies.auth import obter_usuario_atual
from app.models.usuario import Usuario


def exigir_admin(
    usuario_atual: Usuario = Depends(
        obter_usuario_atual
    ),
) -> Usuario:
    if usuario_atual.perfil != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )

    return usuario_atual


def validar_acesso_loja(
    usuario_atual: Usuario,
    loja_id: int,
) -> Usuario:
    if (
        usuario_atual.perfil == "operador"
        and usuario_atual.loja_id != loja_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não permitido a esta loja.",
        )

    return usuario_atual