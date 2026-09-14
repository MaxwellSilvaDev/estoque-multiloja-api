from app.crud.usuario import criar_usuario
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


def test_login_valido_retorna_token(db_session):
    criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Admin Teste",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    resposta = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "senha": "SenhaSegura123",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["token_type"] == "bearer"
    assert isinstance(dados["access_token"], str)
    assert dados["access_token"]


def test_login_permitido_em_modo_demo(
    db_session,
    monkeypatch,
):
    criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Usuario Demo",
            email="demo@example.com",
            senha="SenhaDemo123",
            perfil="admin",
            loja_id=None,
        ),
    )

    monkeypatch.setenv(
        "DEMO_READ_ONLY",
        "true",
    )

    resposta = client.post(
        "/auth/login",
        json={
            "email": "demo@example.com",
            "senha": "SenhaDemo123",
        },
    )

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()


def test_login_com_senha_invalida_retorna_401(
    db_session,
):
    criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Admin Teste",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    resposta = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "senha": "SenhaErrada123",
        },
    )

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Credenciais inválidas."


def test_login_usuario_inativo_retorna_401(
    db_session,
):
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

    usuario.ativo = False
    db_session.commit()

    resposta = client.post(
        "/auth/login",
        json={
            "email": "inativo@example.com",
            "senha": "SenhaSegura123",
        },
    )

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Credenciais inválidas."