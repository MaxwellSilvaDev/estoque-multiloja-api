from decimal import Decimal

from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.produto import buscar_produto_por_id
from app.crud.usuario import criar_usuario
from app.models.loja import Loja
from app.models.produto import Produto
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


def criar_loja_teste(
    db_session,
) -> Loja:
    loja = Loja(
        nome="Loja do Operador",
        endereco="Rua Teste, 123",
        tipo="filial",
    )

    db_session.add(loja)
    db_session.commit()
    db_session.refresh(loja)

    return loja


def criar_produto_teste(
    db_session,
) -> Produto:
    produto = Produto(
        nome="Produto de Teste",
        categoria="Teste",
        preco=Decimal("59.90"),
        sku="PROD-TESTE-001",
    )

    db_session.add(produto)
    db_session.commit()
    db_session.refresh(produto)

    return produto


def criar_token_usuario(
    usuario,
) -> str:
    return criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )


def test_criar_produto_sem_autenticacao_retorna_401():
    resposta = client.post(
        "/produtos",
        json={
            "nome": "Produto Protegido",
            "categoria": "Teste",
            "preco": 99.90,
            "sku": "PROD-PROTEGIDO-001",
        },
    )

    assert resposta.status_code == 401


def test_operador_nao_pode_criar_produto(
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

    token = criar_token_usuario(
        operador,
    )

    resposta = client.post(
        "/produtos",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Produto Bloqueado",
            "categoria": "Teste",
            "preco": 79.90,
            "sku": "PROD-BLOQUEADO-001",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_admin_pode_criar_produto(
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

    token = criar_token_usuario(
        admin,
    )

    resposta = client.post(
        "/produtos",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Produto Permitido",
            "categoria": "Teste",
            "preco": 149.90,
            "sku": "PROD-PERMITIDO-001",
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Produto Permitido"
    assert dados["categoria"] == "Teste"
    assert dados["sku"] == "PROD-PERMITIDO-001"


def test_listar_produtos_sem_autenticacao_retorna_401():
    resposta = client.get(
        "/produtos",
    )

    assert resposta.status_code == 401


def test_operador_pode_listar_produtos(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
    )

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

    token = criar_token_usuario(
        operador,
    )

    resposta = client.get(
        "/produtos",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == produto.id
    assert dados[0]["nome"] == "Produto de Teste"
    assert dados[0]["sku"] == "PROD-TESTE-001"


def test_consultar_produto_por_id_sem_autenticacao_retorna_401(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
    )

    resposta = client.get(
        f"/produtos/{produto.id}",
    )

    assert resposta.status_code == 401


def test_operador_nao_pode_editar_produto(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
    )

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

    token = criar_token_usuario(
        operador,
    )

    resposta = client.patch(
        f"/produtos/{produto.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Produto Alterado",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_operador_nao_pode_excluir_produto(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
    )

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

    token = criar_token_usuario(
        operador,
    )

    resposta = client.delete(
        f"/produtos/{produto.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_admin_pode_excluir_produto(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
    )

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

    token = criar_token_usuario(
        admin,
    )

    produto_id = produto.id

    resposta = client.delete(
        f"/produtos/{produto_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 204

    db_session.expire_all()

    produto_excluido = buscar_produto_por_id(
        db_session,
        produto_id,
    )

    assert produto_excluido is None