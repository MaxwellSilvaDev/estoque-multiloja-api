from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


def criar_headers_admin(
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

    return {
        "Authorization": f"Bearer {token}",
    }


def test_criar_produto(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Notebook Teste",
            "categoria": "Informática",
            "preco": 3500.00,
            "sku": "NOTE-TESTE-001",
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Notebook Teste"
    assert dados["categoria"] == "Informática"
    assert dados["preco"] == "3500.00"
    assert dados["sku"] == "NOTE-TESTE-001"
    assert "id" in dados


def test_criar_produto_com_preco_invalido(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Produto Inválido",
            "categoria": "Teste",
            "preco": -10.00,
            "sku": "INVALIDO-001",
        },
    )

    assert resposta.status_code == 422


def test_criar_produto_com_sku_duplicado(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    produto = {
        "nome": "Mouse Teste",
        "categoria": "Periféricos",
        "preco": 99.90,
        "sku": "MOUSE-001",
    }

    primeira_resposta = client.post(
        "/produtos",
        headers=headers,
        json=produto,
    )

    segunda_resposta = client.post(
        "/produtos",
        headers=headers,
        json=produto,
    )

    assert primeira_resposta.status_code == 201
    assert segunda_resposta.status_code == 409

    assert segunda_resposta.json()["detail"] == (
        "Já existe um produto com este SKU."
    )


def test_nao_excluir_produto_com_movimentacoes(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Produto",
            "endereco": "Rua Produto, 100",
            "tipo": "matriz",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Produto Protegido",
            "categoria": "Teste",
            "preco": 500.00,
            "sku": "PROTEGIDO-001",
        },
    )

    loja_id = resposta_loja.json()["id"]
    produto_id = resposta_produto.json()["id"]

    resposta_entrada = client.post(
        "/movimentacoes/entrada",
        headers=headers,
        json={
            "produto_id": produto_id,
            "loja_id": loja_id,
            "quantidade": 10,
        },
    )

    assert resposta_entrada.status_code == 201

    resposta_exclusao = client.delete(
        f"/produtos/{produto_id}",
        headers=headers,
    )

    assert resposta_exclusao.status_code == 409

    assert resposta_exclusao.json()["detail"] == (
        "Não é possível excluir este produto porque ele possui estoque ou movimentações vinculadas."
    )

    resposta_consulta = client.get(
        f"/produtos/{produto_id}",
        headers=headers,
    )

    assert resposta_consulta.status_code == 200