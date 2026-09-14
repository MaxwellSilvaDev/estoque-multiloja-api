import pytest
from pydantic import ValidationError


def test_usuario_rejeita_senha_com_menos_de_8_caracteres():
    from app.schemas.usuario import UsuarioCreate

    with pytest.raises(ValidationError):
        UsuarioCreate(
            nome="Admin Teste",
            email="admin@example.com",
            senha="1234567",
            perfil="admin",
            loja_id=None,
        )


def test_usuario_aceita_senha_com_8_caracteres():
    from app.schemas.usuario import UsuarioCreate

    usuario = UsuarioCreate(
        nome="Admin Teste",
        email="admin@example.com",
        senha="12345678",
        perfil="admin",
        loja_id=None,
    )

    assert usuario.senha == "12345678"