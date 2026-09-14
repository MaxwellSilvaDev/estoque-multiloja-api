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


def test_registrar_entrada_e_atualizar_estoque(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Teste",
            "endereco": "Rua Teste, 100",
            "tipo": "matriz",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Notebook Teste",
            "categoria": "Informática",
            "preco": 3500.00,
            "sku": "NOTE-MOV-001",
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

    movimentacao = resposta_entrada.json()

    assert movimentacao["tipo"] == "entrada"
    assert movimentacao["quantidade"] == 10

    resposta_estoque = client.get(
        f"/estoques/loja/{loja_id}/produto/{produto_id}",
        headers=headers,
    )

    assert resposta_estoque.status_code == 200

    estoque = resposta_estoque.json()

    assert estoque["quantidade"] == 10


def test_registrar_saida_e_atualizar_estoque(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Saída",
            "endereco": "Rua Saída, 200",
            "tipo": "filial",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Mouse Teste",
            "categoria": "Periféricos",
            "preco": 100.00,
            "sku": "MOUSE-MOV-001",
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

    resposta_saida = client.post(
        "/movimentacoes/saida",
        headers=headers,
        json={
            "produto_id": produto_id,
            "loja_id": loja_id,
            "quantidade": 3,
        },
    )

    assert resposta_saida.status_code == 201

    movimentacao = resposta_saida.json()

    assert movimentacao["tipo"] == "saida"
    assert movimentacao["quantidade"] == 3

    resposta_estoque = client.get(
        f"/estoques/loja/{loja_id}/produto/{produto_id}",
        headers=headers,
    )

    assert resposta_estoque.status_code == 200

    estoque = resposta_estoque.json()

    assert estoque["quantidade"] == 7


def test_saida_com_saldo_insuficiente(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Saldo",
            "endereco": "Rua Saldo, 300",
            "tipo": "matriz",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Teclado Teste",
            "categoria": "Periféricos",
            "preco": 200.00,
            "sku": "TECLADO-MOV-001",
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
            "quantidade": 5,
        },
    )

    assert resposta_entrada.status_code == 201

    resposta_saida = client.post(
        "/movimentacoes/saida",
        headers=headers,
        json={
            "produto_id": produto_id,
            "loja_id": loja_id,
            "quantidade": 10,
        },
    )

    assert resposta_saida.status_code == 400

    assert resposta_saida.json()["detail"] == (
        "Saldo de estoque insuficiente."
    )

    resposta_estoque = client.get(
        f"/estoques/loja/{loja_id}/produto/{produto_id}",
        headers=headers,
    )

    assert resposta_estoque.status_code == 200

    estoque = resposta_estoque.json()

    assert estoque["quantidade"] == 5


def test_filtrar_movimentacoes_por_loja(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja_1 = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja 1",
            "endereco": "Rua Um, 100",
            "tipo": "matriz",
        },
    )

    resposta_loja_2 = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja 2",
            "endereco": "Rua Dois, 200",
            "tipo": "filial",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Monitor Teste",
            "categoria": "Informática",
            "preco": 1200.00,
            "sku": "MONITOR-MOV-001",
        },
    )

    loja_1_id = resposta_loja_1.json()["id"]
    loja_2_id = resposta_loja_2.json()["id"]
    produto_id = resposta_produto.json()["id"]

    resposta_entrada_loja_1 = client.post(
        "/movimentacoes/entrada",
        headers=headers,
        json={
            "produto_id": produto_id,
            "loja_id": loja_1_id,
            "quantidade": 10,
        },
    )

    resposta_entrada_loja_2 = client.post(
        "/movimentacoes/entrada",
        headers=headers,
        json={
            "produto_id": produto_id,
            "loja_id": loja_2_id,
            "quantidade": 20,
        },
    )

    assert resposta_entrada_loja_1.status_code == 201
    assert resposta_entrada_loja_2.status_code == 201

    resposta = client.get(
        f"/movimentacoes?loja_id={loja_1_id}",
        headers=headers,
    )

    assert resposta.status_code == 200

    movimentacoes = resposta.json()

    assert len(movimentacoes) == 1
    assert movimentacoes[0]["loja_id"] == loja_1_id
    assert movimentacoes[0]["produto_id"] == produto_id
    assert movimentacoes[0]["tipo"] == "entrada"
    assert movimentacoes[0]["quantidade"] == 10


def test_paginacao_movimentacoes(
    db_session,
):
    headers = criar_headers_admin(
        db_session,
    )

    resposta_loja = client.post(
        "/lojas",
        headers=headers,
        json={
            "nome": "Loja Paginação",
            "endereco": "Rua Paginação, 400",
            "tipo": "matriz",
        },
    )

    resposta_produto = client.post(
        "/produtos",
        headers=headers,
        json={
            "nome": "Produto Paginação",
            "categoria": "Teste",
            "preco": 300.00,
            "sku": "PAGINACAO-001",
        },
    )

    loja_id = resposta_loja.json()["id"]
    produto_id = resposta_produto.json()["id"]

    for quantidade in [5, 3, 2]:
        resposta = client.post(
            "/movimentacoes/entrada",
            headers=headers,
            json={
                "produto_id": produto_id,
                "loja_id": loja_id,
                "quantidade": quantidade,
            },
        )

        assert resposta.status_code == 201

    primeira_pagina = client.get(
        "/movimentacoes?limit=2&offset=0",
        headers=headers,
    )

    segunda_pagina = client.get(
        "/movimentacoes?limit=2&offset=2",
        headers=headers,
    )

    assert primeira_pagina.status_code == 200
    assert segunda_pagina.status_code == 200

    dados_primeira_pagina = primeira_pagina.json()
    dados_segunda_pagina = segunda_pagina.json()

    assert len(dados_primeira_pagina) == 2
    assert len(dados_segunda_pagina) == 1

    ids = {
        movimentacao["id"]
        for movimentacao in (
            dados_primeira_pagina
            + dados_segunda_pagina
        )
    }

    assert len(ids) == 3