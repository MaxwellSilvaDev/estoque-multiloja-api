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