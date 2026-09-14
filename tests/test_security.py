def test_hash_senha_nao_armazena_texto_puro():
    from app.core.security import gerar_hash_senha, verificar_senha

    senha = "SenhaSegura123"

    senha_hash = gerar_hash_senha(senha)

    assert senha_hash != senha
    assert verificar_senha(senha, senha_hash) is True
    assert verificar_senha("SenhaErrada123", senha_hash) is False