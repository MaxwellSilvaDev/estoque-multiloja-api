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
) -> Loja:
    loja = Loja(
        nome="Loja Estoque Mínimo",
        endereco="Rua Mínimo, 100",
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
        nome="Produto Estoque Mínimo",
        categoria="Teste",
        preco=Decimal("100.00"),
        sku="MINIMO-001",
    )

    db_session.add(produto)
    db_session.commit()
    db_session.refresh(produto)

    return produto


def criar_estoque_teste(
    db_session,
    produto_id: int,
    loja_id: int,
) -> Estoque:
    estoque = Estoque(
        produto_id=produto_id,
        loja_id=loja_id,
        quantidade=20,
    )

    db_session.add(estoque)
    db_session.commit()
    db_session.refresh(estoque)

    return estoque


def criar_headers_admin(
    db_session,
) -> dict[str, str]:
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

    token = criar_token_acesso(
        usuario_id=admin.id,
        chave_secreta=settings.jwt_secret,
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def criar_headers_operador(
    db_session,
    loja_id: int,
) -> dict[str, str]:
    operador = criar_usuario(
        db_session,
        UsuarioCreate(
            nome="Operador",
            email="operador@example.com",
            senha="SenhaSegura123",
            perfil="operador",
            loja_id=loja_id,
        ),
    )

    token = criar_token_acesso(
        usuario_id=operador.id,
        chave_secreta=settings.jwt_secret,
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def test_admin_pode_configurar_estoque_minimo(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.patch(
        (
            f"/estoques/loja/{loja.id}"
            f"/produto/{produto.id}/minimo"
        ),
        headers=headers,
        json={
            "estoque_minimo": 10,
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["quantidade"] == 20
    assert dados["estoque_minimo"] == 10


def test_operador_nao_pode_configurar_estoque_minimo(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
    )

    headers = criar_headers_operador(
        db_session,
        loja_id=loja.id,
    )

    resposta = client.patch(
        (
            f"/estoques/loja/{loja.id}"
            f"/produto/{produto.id}/minimo"
        ),
        headers=headers,
        json={
            "estoque_minimo": 10,
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso restrito a administradores."
    )


def test_estoque_minimo_negativo_retorna_422(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.patch(
        (
            f"/estoques/loja/{loja.id}"
            f"/produto/{produto.id}/minimo"
        ),
        headers=headers,
        json={
            "estoque_minimo": -1,
        },
    )

    assert resposta.status_code == 422


def test_operador_pode_visualizar_estoque_minimo_da_propria_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
    )

    estoque = criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
    )

    estoque.estoque_minimo = 7
    db_session.commit()

    headers = criar_headers_operador(
        db_session,
        loja_id=loja.id,
    )

    resposta = client.get(
        (
            f"/estoques/loja/{loja.id}"
            f"/produto/{produto.id}"
        ),
        headers=headers,
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["quantidade"] == 20
    assert dados["estoque_minimo"] == 7


def test_novo_estoque_criado_por_entrada_possui_minimo_zero(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta_entrada = client.post(
        "/movimentacoes/entrada",
        headers=headers,
        json={
            "produto_id": produto.id,
            "loja_id": loja.id,
            "quantidade": 10,
        },
    )

    assert resposta_entrada.status_code == 201

    resposta_estoque = client.get(
        (
            f"/estoques/loja/{loja.id}"
            f"/produto/{produto.id}"
        ),
        headers=headers,
    )

    assert resposta_estoque.status_code == 200

    dados = resposta_estoque.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["quantidade"] == 10
    assert dados["estoque_minimo"] == 0