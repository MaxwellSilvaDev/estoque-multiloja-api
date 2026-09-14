from decimal import Decimal

from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.models.estoque import Estoque
from app.models.loja import Loja
from app.models.produto import Produto
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


def criar_loja_teste(
    db_session,
    nome: str,
    endereco: str,
) -> Loja:
    loja = Loja(
        nome=nome,
        endereco=endereco,
        tipo="filial",
    )

    db_session.add(loja)
    db_session.commit()
    db_session.refresh(loja)

    return loja


def criar_produto_teste(
    db_session,
) -> Produto:
    produto = Produto(
        nome="Produto de Estoque",
        categoria="Teste",
        preco=Decimal("99.90"),
        sku="ESTOQUE-PERM-001",
    )

    db_session.add(produto)
    db_session.commit()
    db_session.refresh(produto)

    return produto


def criar_estoque_teste(
    db_session,
    produto_id: int,
    loja_id: int,
    quantidade: int,
) -> Estoque:
    estoque = Estoque(
        produto_id=produto_id,
        loja_id=loja_id,
        quantidade=quantidade,
    )

    db_session.add(estoque)
    db_session.commit()
    db_session.refresh(estoque)

    return estoque


def criar_token_usuario(
    usuario,
) -> str:
    return criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )


def test_consultar_estoque_da_loja_sem_autenticacao_retorna_401():
    resposta = client.get(
        "/estoques/loja/1",
    )

    assert resposta.status_code == 401


def test_consultar_estoque_do_produto_sem_autenticacao_retorna_401():
    resposta = client.get(
        "/estoques/loja/1/produto/1",
    )

    assert resposta.status_code == 401


def test_operador_pode_consultar_estoque_da_propria_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
        endereco="Rua Própria, 100",
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

    resposta = client.get(
        f"/estoques/loja/{loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_operador_nao_pode_consultar_estoque_de_outra_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
        endereco="Rua Própria, 100",
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Outra Loja",
        endereco="Rua Outra, 200",
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
        f"/estoques/loja/{outra_loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )


def test_operador_nao_pode_consultar_produto_de_outra_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
        endereco="Rua Própria, 100",
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Outra Loja",
        endereco="Rua Outra, 200",
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
        f"/estoques/loja/{outra_loja.id}/produto/1",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )


def test_operador_pode_consultar_produto_da_propria_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
        endereco="Rua Própria, 100",
    )

    produto = criar_produto_teste(
        db_session,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        quantidade=15,
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

    resposta = client.get(
        f"/estoques/loja/{loja.id}/produto/{produto.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["quantidade"] == 15


def test_admin_pode_consultar_estoque_de_qualquer_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja Administrada",
        endereco="Rua Admin, 300",
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
        f"/estoques/loja/{loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_admin_pode_consultar_produto_de_qualquer_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
        nome="Loja Administrada",
        endereco="Rua Admin, 300",
    )

    produto = criar_produto_teste(
        db_session,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        quantidade=25,
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
        f"/estoques/loja/{loja.id}/produto/{produto.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["quantidade"] == 25