from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.schemas.usuario import UsuarioCreate


def test_obter_usuario_atual_com_token_valido(
    db_session,
):
    from app.api.dependencies.auth import obter_usuario_atual

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Admin Teste",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    token = criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )

    credenciais = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    usuario_atual = obter_usuario_atual(
        credenciais=credenciais,
        db=db_session,
    )

    assert usuario_atual.id == usuario.id
    assert usuario_atual.email == "admin@example.com"


def test_obter_usuario_atual_com_token_invalido_retorna_401(
    db_session,
):
    from app.api.dependencies.auth import obter_usuario_atual

    credenciais = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="token-invalido",
    )

    with pytest.raises(HTTPException) as erro:
        obter_usuario_atual(
            credenciais=credenciais,
            db=db_session,
        )

    assert erro.value.status_code == 401
    assert erro.value.detail == "Token inválido ou expirado."


def test_obter_usuario_atual_inativo_retorna_401(
    db_session,
):
    from app.api.dependencies.auth import obter_usuario_atual

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Admin Inativo",
            email="inativo@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    token = criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )

    usuario.ativo = False
    db_session.commit()

    credenciais = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as erro:
        obter_usuario_atual(
            credenciais=credenciais,
            db=db_session,
        )

    assert erro.value.status_code == 401
    assert erro.value.detail == "Usuário inválido ou inativo."


def test_obter_usuario_atual_com_sub_invalido_retorna_401(
    db_session,
):
    from app.api.dependencies.auth import obter_usuario_atual

    token = jwt.encode(
        {
            "sub": "abc",
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

    credenciais = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as erro:
        obter_usuario_atual(
            credenciais=credenciais,
            db=db_session,
        )

    assert erro.value.status_code == 401
    assert erro.value.detail == "Token inválido ou expirado."


def test_obter_usuario_atual_sem_sub_retorna_401(
    db_session,
):
    from app.api.dependencies.auth import obter_usuario_atual

    token = jwt.encode(
        {
            "tipo": "access",
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

    credenciais = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as erro:
        obter_usuario_atual(
            credenciais=credenciais,
            db=db_session,
        )

    assert erro.value.status_code == 401
    assert erro.value.detail == "Token inválido ou expirado."


def test_obter_usuario_atual_com_token_expirado_retorna_401(
    db_session,
):
    from app.api.dependencies.auth import obter_usuario_atual

    agora = datetime.now(timezone.utc)

    token = jwt.encode(
        {
            "sub": "1",
            "iat": agora - timedelta(hours=2),
            "exp": agora - timedelta(hours=1),
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

    credenciais = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )

    with pytest.raises(HTTPException) as erro:
        obter_usuario_atual(
            credenciais=credenciais,
            db=db_session,
        )

    assert erro.value.status_code == 401
    assert erro.value.detail == "Token inválido ou expirado."