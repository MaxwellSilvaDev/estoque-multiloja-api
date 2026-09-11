from tests.conftest import client


def test_criar_produto():
    resposta = client.post(
        "/produtos",
        json={
            "nome": "Notebook Teste",
            "categoria": "Informática",
            "preco": 3500.00,
            "sku": "NOTE-TESTE-001"
        }
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Notebook Teste"
    assert dados["categoria"] == "Informática"
    assert dados["preco"] == "3500.00"
    assert dados["sku"] == "NOTE-TESTE-001"
    assert "id" in dados


def test_criar_produto_com_preco_invalido():
    resposta = client.post(
        "/produtos",
        json={
            "nome": "Produto Inválido",
            "categoria": "Teste",
            "preco": -10.00,
            "sku": "INVALIDO-001"
        }
    )

    assert resposta.status_code == 422


def test_criar_produto_com_sku_duplicado():
    produto = {
        "nome": "Mouse Teste",
        "categoria": "Periféricos",
        "preco": 99.90,
        "sku": "MOUSE-001"
    }

    primeira_resposta = client.post(
        "/produtos",
        json=produto
    )

    segunda_resposta = client.post(
        "/produtos",
        json=produto
    )

    assert primeira_resposta.status_code == 201
    assert segunda_resposta.status_code == 409

    assert segunda_resposta.json()["detail"] == (
        "Já existe um produto com este SKU."
    )