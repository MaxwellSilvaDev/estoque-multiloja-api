from tests.conftest import client


def test_consultar_estoque_por_loja():
    resposta_loja = client.post(
        "/lojas",
        json={
            "nome": "Loja Estoque",
            "endereco": "Rua Estoque, 100",
            "tipo": "matriz"
        }
    )

    resposta_produto = client.post(
        "/produtos",
        json={
            "nome": "Produto Estoque",
            "categoria": "Teste",
            "preco": 150.00,
            "sku": "ESTOQUE-001"
        }
    )

    loja_id = resposta_loja.json()["id"]
    produto_id = resposta_produto.json()["id"]

    resposta_entrada = client.post(
        "/movimentacoes/entrada",
        json={
            "produto_id": produto_id,
            "loja_id": loja_id,
            "quantidade": 8
        }
    )

    assert resposta_entrada.status_code == 201

    resposta = client.get(
        f"/estoques/loja/{loja_id}"
    )

    assert resposta.status_code == 200

    estoques = resposta.json()

    assert len(estoques) == 1
    assert estoques[0]["produto_id"] == produto_id
    assert estoques[0]["loja_id"] == loja_id
    assert estoques[0]["quantidade"] == 8


def test_consultar_estoque_por_produto_e_loja():
    resposta_loja = client.post(
        "/lojas",
        json={
            "nome": "Loja Consulta",
            "endereco": "Rua Consulta, 200",
            "tipo": "filial"
        }
    )

    resposta_produto = client.post(
        "/produtos",
        json={
            "nome": "Produto Consulta",
            "categoria": "Teste",
            "preco": 250.00,
            "sku": "ESTOQUE-002"
        }
    )

    loja_id = resposta_loja.json()["id"]
    produto_id = resposta_produto.json()["id"]

    client.post(
        "/movimentacoes/entrada",
        json={
            "produto_id": produto_id,
            "loja_id": loja_id,
            "quantidade": 12
        }
    )

    resposta = client.get(
        f"/estoques/loja/{loja_id}/produto/{produto_id}"
    )

    assert resposta.status_code == 200

    estoque = resposta.json()

    assert estoque["produto_id"] == produto_id
    assert estoque["loja_id"] == loja_id
    assert estoque["quantidade"] == 12


def test_consultar_estoque_inexistente():
    resposta = client.get(
        "/estoques/loja/999/produto/999"
    )

    assert resposta.status_code == 404

    assert resposta.json()["detail"] == (
        "Estoque não encontrado."
    )