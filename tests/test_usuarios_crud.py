import pytest

from app.core.security import verificar_senha
from app.schemas.usuario import UsuarioCreate


def test_criar_usuario_armazena_somente_hash(db_session):
    from app.crud.usuario import criar_usuario

    dados = UsuarioCreate(
        nome="Admin Teste",
        email="admin@example.com",
        senha="SenhaSegura123",
        perfil="admin",
        loja_id=None,
    )

    usuario = criar_usuario(
        db_session,
        dados,
    )

    assert usuario.senha_hash != dados.senha
    assert verificar_senha(
        dados.senha,
        usuario.senha_hash,
    ) is True
    assert not hasattr(usuario, "senha")


def test_criar_usuario_com_email_duplicado_retorna_erro_amigavel(
    db_session,
):
    from app.crud.usuario import criar_usuario

    primeiro_usuario = UsuarioCreate(
        nome="Admin Um",
        email="admin@example.com",
        senha="SenhaSegura123",
        perfil="admin",
        loja_id=None,
    )

    segundo_usuario = UsuarioCreate(
        nome="Admin Dois",
        email="admin@example.com",
        senha="OutraSenha123",
        perfil="admin",
        loja_id=None,
    )

    criar_usuario(
        db_session,
        primeiro_usuario,
    )

    with pytest.raises(
        ValueError,
        match="Já existe um usuário com este e-mail.",
    ):
        criar_usuario(
            db_session,
            segundo_usuario,
        )