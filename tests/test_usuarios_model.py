import pytest
from sqlalchemy.exc import IntegrityError


def test_operador_exige_loja(db_session):
    from app.models.usuario import Usuario

    usuario = Usuario(
        nome="Operador Teste",
        email="operador@example.com",
        senha_hash="hash",
        perfil="operador",
        ativo=True,
        loja_id=None,
    )

    db_session.add(usuario)

    with pytest.raises(IntegrityError):
        db_session.commit()