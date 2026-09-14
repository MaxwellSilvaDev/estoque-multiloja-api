import jwt

from app.core.security import gerar_hash_senha, verificar_senha


def test_hash_senha_nao_armazena_texto_puro():
    senha = "SenhaSegura123"

    senha_hash = gerar_hash_senha(senha)

    assert senha_hash != senha
    assert verificar_senha(senha, senha_hash) is True
    assert verificar_senha("SenhaErrada123", senha_hash) is False


def test_token_acesso_expira_em_60_minutos():
    from app.core.security import criar_token_acesso

    chave_secreta = "segredo-apenas-para-teste"

    token = criar_token_acesso(
        usuario_id=42,
        chave_secreta=chave_secreta,
    )

    payload = jwt.decode(
        token,
        chave_secreta,
        algorithms=["HS256"],
    )

    assert payload["sub"] == "42"
    assert payload["exp"] - payload["iat"] == 3600