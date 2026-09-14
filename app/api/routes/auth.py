from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import criar_token_acesso, verificar_senha
from app.crud.usuario import buscar_usuario_por_email
from app.db.session import get_db
from app.schemas.usuario import LoginRequest, TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    usuario = buscar_usuario_por_email(
        db,
        dados.email,
    )

    if (
        usuario is None
        or not usuario.ativo
        or not verificar_senha(
            dados.senha,
            usuario.senha_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )

    token = criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )
