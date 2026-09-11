from tests.conftest import client


def test_criar_loja():
    resposta = client.post(
        "/lojas",
        json={
            "nome": "Loja Teste",
            "endereco": "Rua dos Testes, 100",
            "tipo": "filial"
        }
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Loja Teste"
    assert dados["endereco"] == "Rua dos Testes, 100"
    assert dados["tipo"] == "filial"
    assert "id" in dados


def test_criar_loja_com_tipo_invalido():
    resposta = client.post(
        "/lojas",
        json={
            "nome": "Loja Inválida",
            "endereco": "Rua Teste, 200",
            "tipo": "franquia"
        }
    )

    assert resposta.status_code == 422


def test_nao_excluir_loja_com_movimentacoes():
    resposta_loja = client.post(
        "/lojas",
        json={
            "nome": "Loja Protegida",
            "endereco": "Rua Protegida, 300",
            "tipo": "matriz"
        }
    )

    resposta_produto = client.post(
        "/produtos",
        json={
            "nome": "Produto Loja",
            "categoria": "Teste",
            "preco": 400.00,
            "sku": "LOJA-PROTEGIDA-001"
        }
    )

    loja_id = resposta_loja.json()["id"]
    produto_id = resposta_produto.json()["id"]

    resposta_entrada = client.post(
        "/movimentacoes/entrada",
        json={
            "produto_id": produto_id,
            "loja_id": loja_id,
            "quantidade": 5
        }
    )

    assert resposta_entrada.status_code == 201

    resposta_exclusao = client.delete(
        f"/lojas/{loja_id}"
    )

    assert resposta_exclusao.status_code == 409

    assert resposta_exclusao.json()["detail"] == (
        "Não é possível excluir esta loja porque ela possui estoque ou movimentações vinculadas."
    )

    resposta_consulta = client.get(
        f"/lojas/{loja_id}"
    )

    assert resposta_consulta.status_code == 200