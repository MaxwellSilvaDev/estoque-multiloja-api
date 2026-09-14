import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.usuario import Usuario


seguranca_bearer = HTTPBearer()


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(
        seguranca_bearer
    ),
    db: Session = Depends(get_db),
) -> Usuario:
    try:
        payload = jwt.decode(
            credenciais.credentials,
            settings.jwt_secret,
            algorithms=["HS256"],
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
        )

    try:
        usuario_id = int(payload["sub"])

    except (KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
        )

    usuario = db.get(
        Usuario,
        usuario_id,
    )

    if usuario is None or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inválido ou inativo.",
        )

    return usuario
