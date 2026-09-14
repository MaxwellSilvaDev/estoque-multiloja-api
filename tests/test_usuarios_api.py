from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.models.loja import Loja
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


def criar_loja_teste(
    db_session,
    nome: str = "Loja Teste",
) -> Loja:
    loja = Loja(
        nome=nome,
        endereco="Rua Teste, 123",
        tipo="filial",
    )

    db_session.add(loja)
    db_session.commit()
    db_session.refresh(loja)

    return loja


def criar_admin_com_token(
    db_session,
):
    admin = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Administrador",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    token = criar_token_acesso(
        usuario_id=admin.id,
        chave_secreta=settings.jwt_secret,
    )

    return admin, token


def test_admin_cria_operador(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja Operador",
    )

    _, token = criar_admin_com_token(
        db_session,
    )

    resposta = client.post(
        "/usuarios",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Operador Teste",
            "email": "operador@example.com",
            "senha": "SenhaSegura123",
            "perfil": "operador",
            "loja_id": loja.id,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Operador Teste"
    assert dados["email"] == "operador@example.com"
    assert dados["perfil"] == "operador"
    assert dados["ativo"] is True
    assert dados["loja_id"] == loja.id
    assert "senha" not in dados
    assert "senha_hash" not in dados


def test_operador_nao_pode_criar_usuario(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    token = criar_token_acesso(
        usuario_id=operador.id,
        chave_secreta=settings.jwt_secret,
    )

    resposta = client.post(
        "/usuarios",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Outro Operador",
            "email": "outro@example.com",
            "senha": "SenhaSegura123",
            "perfil": "operador",
            "loja_id": loja.id,
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_usuario_anonimo_nao_pode_criar_usuario():
    resposta = client.post(
        "/usuarios",
        json={
            "nome": "Operador Teste",
            "email": "operador@example.com",
            "senha": "SenhaSegura123",
            "perfil": "operador",
            "loja_id": 1,
        },
    )

    assert resposta.status_code == 401


def test_email_duplicado_retorna_409(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    _, token = criar_admin_com_token(
        db_session,
    )

    criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador Existente",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    resposta = client.post(
        "/usuarios",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Operador Duplicado",
            "email": "operador@example.com",
            "senha": "SenhaSegura123",
            "perfil": "operador",
            "loja_id": loja.id,
        },
    )

    assert resposta.status_code == 409
    assert resposta.json()["detail"] == (
        "Já existe um usuário com este e-mail."
    )


def test_admin_desativa_usuario(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    _, token = criar_admin_com_token(
        db_session,
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    resposta = client.patch(
        f"/usuarios/{operador.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "ativo": False,
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["id"] == operador.id
    assert dados["ativo"] is False


def test_admin_lista_usuarios(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    admin, token = criar_admin_com_token(
        db_session,
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    resposta = client.get(
        "/usuarios",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 2

    ids = {
        usuario["id"]
        for usuario in dados
    }

    assert admin.id in ids
    assert operador.id in ids

    for usuario in dados:
        assert "senha" not in usuario
        assert "senha_hash" not in usuario


def test_admin_busca_usuario_por_id(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    _, token = criar_admin_com_token(
        db_session,
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    resposta = client.get(
        f"/usuarios/{operador.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["id"] == operador.id
    assert dados["nome"] == "Operador"
    assert dados["email"] == "operador@example.com"
    assert dados["perfil"] == "operador"
    assert dados["ativo"] is True
    assert dados["loja_id"] == loja.id
    assert "senha" not in dados
    assert "senha_hash" not in dados


def test_usuario_desativado_nao_pode_fazer_login(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    _, token = criar_admin_com_token(
        db_session,
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    resposta_desativacao = client.patch(
        f"/usuarios/{operador.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "ativo": False,
        },
    )

    assert resposta_desativacao.status_code == 200

    resposta_login = client.post(
        "/auth/login",
        json={
            "email": "operador@example.com",
            "senha": "SenhaSegura123",
        },
    )

    assert resposta_login.status_code == 401