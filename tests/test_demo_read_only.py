from tests.conftest import client


def test_demo_read_only_bloqueia_operacao_de_escrita(monkeypatch):
    monkeypatch.setenv("DEMO_READ_ONLY", "true")

    resposta = client.post(
        "/lojas",
        json={
            "nome": "Loja Demo",
            "endereco": "Endereço fictício",
            "tipo": "filial"
        }
    )

    assert resposta.status_code == 403

    assert resposta.json()["detail"] == (
        "Ambiente de demonstração: operações de escrita estão desativadas."
    )
