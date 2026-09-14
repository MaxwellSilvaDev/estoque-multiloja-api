import pytest
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.models.loja import Loja
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


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


def criar_token_usuario(
    usuario,
) -> str:
    return criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )


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


def test_criar_loja_sem_autenticacao_retorna_401():
    resposta = client.post(
        "/lojas",
        json={
            "nome": "Loja Sem Autenticação",
            "endereco": "Rua Teste, 100",
            "tipo": "filial",
        },
    )

    assert resposta.status_code == 401


def test_operador_nao_pode_criar_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja_operador.id,
        ),
    )

    token = criar_token_usuario(
        operador,
    )

    resposta = client.post(
        "/lojas",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Nova Loja",
            "endereco": "Rua Nova, 200",
            "tipo": "filial",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_admin_pode_criar_loja(
    db_session,
):
    admin = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Administrador",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    token = criar_token_usuario(
        admin,
    )

    resposta = client.post(
        "/lojas",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Nova Loja",
            "endereco": "Rua Nova, 200",
            "tipo": "filial",
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["nome"] == "Nova Loja"
    assert dados["endereco"] == "Rua Nova, 200"
    assert dados["tipo"] == "filial"


def test_operador_nao_pode_editar_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja Original",
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    token = criar_token_usuario(
        operador,
    )

    resposta = client.patch(
        f"/lojas/{loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": "Loja Alterada",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_operador_nao_pode_excluir_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja para Exclusão",
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja.id,
        ),
    )

    token = criar_token_usuario(
        operador,
    )

    resposta = client.delete(
        f"/lojas/{loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_listar_lojas_sem_autenticacao_retorna_401():
    resposta = client.get(
        "/lojas",
    )

    assert resposta.status_code == 401


def test_operador_lista_apenas_propria_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
    )

    criar_loja_teste(
        db_session,
        nome="Outra Loja",
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja_operador.id,
        ),
    )

    token = criar_token_usuario(
        operador,
    )

    resposta = client.get(
        "/lojas",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == loja_operador.id
    assert dados[0]["nome"] == "Loja do Operador"


def test_admin_lista_todas_as_lojas(
    db_session,
):
    loja_1 = criar_loja_teste(
        db_session,
        nome="Loja Matriz",
    )

    loja_2 = criar_loja_teste(
        db_session,
        nome="Loja Filial",
    )

    admin = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Administrador",
            email="admin@example.com",
            senha="SenhaSegura123",
            perfil="admin",
            loja_id=None,
        ),
    )

    token = criar_token_usuario(
        admin,
    )

    resposta = client.get(
        "/lojas",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 2
    assert {loja["id"] for loja in dados} == {
        loja_1.id,
        loja_2.id,
    }


def test_consultar_loja_por_id_sem_autenticacao_retorna_401(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja Protegida",
    )

    resposta = client.get(
        f"/lojas/{loja.id}",
    )

    assert resposta.status_code == 401


def test_operador_nao_pode_consultar_outra_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Loja de Outro Operador",
    )

    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja_operador.id,
        ),
    )

    token = criar_token_usuario(
        operador,
    )

    resposta = client.get(
        f"/lojas/{outra_loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )