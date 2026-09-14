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


def test_consultar_estoque_por_loja(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Estoque",
            "endereco": "Rua Estoque, 100",
            "tipo": "matriz",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Produto Estoque",
            "categoria": "Teste",
            "preco": 150.00,
            "sku": "ESTOQUE-001",
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
            "quantidade": 8,
        },
    )

    assert resposta_entrada.status_code == 201

    resposta = client.get(
        f"/estoques/loja/{loja_id}",
        headers=headers,
    )

    assert resposta.status_code == 200

    estoques = resposta.json()

    assert len(estoques) == 1
    assert estoques[0]["produto_id"] == produto_id
    assert estoques[0]["loja_id"] == loja_id
    assert estoques[0]["quantidade"] == 8


def test_consultar_estoque_por_produto_e_loja(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Consulta",
            "endereco": "Rua Consulta, 200",
            "tipo": "filial",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Produto Consulta",
            "categoria": "Teste",
            "preco": 250.00,
            "sku": "ESTOQUE-002",
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
            "quantidade": 12,
        },
    )

    assert resposta_entrada.status_code == 201

    resposta = client.get(
        f"/estoques/loja/{loja_id}/produto/{produto_id}",
        headers=headers,
    )

    assert resposta.status_code == 200

    estoque = resposta.json()

    assert estoque["produto_id"] == produto_id
    assert estoque["loja_id"] == loja_id
    assert estoque["quantidade"] == 12


def test_consultar_estoque_inexistente(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/estoques/loja/999/produto/999",
        headers=headers,
    )

    assert resposta.status_code == 404

    assert resposta.json()["detail"] == (
        "Estoque não encontrado."
    )