import pytest
from fastapi import HTTPException

from app.crud.usuario import criar_usuario
from app.models.loja import Loja
from app.schemas.usuario import UsuarioCreate


def criar_loja_teste(
    db_session,
    nome: str = "Loja Teste",
) -> Loja:
    loja = Loja(
        nome=nome,
        endereco="Rua Teste, 123",
        tipo="filial",
    )

    db_session.add(loja)
    db_session.commit()
    db_session.refresh(loja)

    return loja


def test_exigir_admin_permite_usuario_admin(
    db_session,
):
    from app.api.dependencies.permissoes import exigir_admin

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Administrador",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    resultado = exigir_admin(
        usuario_atual=usuario,
    )

    assert resultado.id == usuario.id
    assert resultado.perfil == "admin"


def test_exigir_admin_bloqueia_operador_com_403(
    db_session,
):
    from app.api.dependencies.permissoes import exigir_admin

    loja = criar_loja_teste(
        db_session,
    )

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    with pytest.raises(HTTPException) as erro:
        exigir_admin(
            usuario_atual=usuario,
        )

    assert erro.value.status_code == 403
    assert erro.value.detail == "Acesso restrito a administradores."


def test_validar_acesso_loja_permite_operador_na_propria_loja(
    db_session,
):
    from app.api.dependencies.permissoes import validar_acesso_loja

    loja = criar_loja_teste(
        db_session,
    )

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    resultado = validar_acesso_loja(
        usuario_atual=usuario,
        loja_id=loja.id,
    )

    assert resultado.id == usuario.id
    assert resultado.loja_id == loja.id


def test_validar_acesso_loja_bloqueia_operador_em_outra_loja(
    db_session,
):
    from app.api.dependencies.permissoes import validar_acesso_loja

    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Outra Loja",
    )

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja_operador.id,
        ),
    )

    with pytest.raises(HTTPException) as erro:
        validar_acesso_loja(
            usuario_atual=usuario,
            loja_id=outra_loja.id,
        )

    assert erro.value.status_code == 403
    assert erro.value.detail == "Acesso não permitido a esta loja."


def test_validar_acesso_loja_permite_admin_em_qualquer_loja(
    db_session,
):
    from app.api.dependencies.permissoes import validar_acesso_loja

    loja = criar_loja_teste(
        db_session,
        nome="Loja Filial",
    )

    usuario = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Administrador",
            email="admin-loja@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    resultado = validar_acesso_loja(
        usuario_atual=usuario,
        loja_id=loja.id,
    )

    assert resultado.id == usuario.id
    assert resultado.perfil == "admin"