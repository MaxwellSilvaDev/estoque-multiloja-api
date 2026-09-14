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
    nome: str = "Loja Alertas",
    endereco: str = "Rua dos Alertas, 100",
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
    nome: str,
    sku: str,
) -> Produto:
    produto = Produto(
        nome=nome,
        categoria="Teste",
        preco=Decimal("100.00"),
        sku=sku,
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
    estoque_minimo: int,
) -> Estoque:
    estoque = Estoque(
        produto_id=produto_id,
        loja_id=loja_id,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo,
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


def test_admin_lista_apenas_estoques_baixos_da_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto_baixo = criar_produto_teste(
        db_session,
        nome="Produto Baixo",
        sku="ALERTA-001",
    )

    produto_normal = criar_produto_teste(
        db_session,
        nome="Produto Normal",
        sku="ALERTA-002",
    )

    produto_sem_alerta = criar_produto_teste(
        db_session,
        nome="Produto Sem Alerta",
        sku="ALERTA-003",
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto_baixo.id,
        loja_id=loja.id,
        quantidade=5,
        estoque_minimo=10,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto_normal.id,
        loja_id=loja.id,
        quantidade=15,
        estoque_minimo=10,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto_sem_alerta.id,
        loja_id=loja.id,
        quantidade=0,
        estoque_minimo=0,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        f"/estoques/loja/{loja.id}/alertas/baixo",
        headers=headers,
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["produto_id"] == produto_baixo.id
    assert dados[0]["loja_id"] == loja.id
    assert dados[0]["quantidade"] == 5
    assert dados[0]["estoque_minimo"] == 10


def test_estoque_igual_ao_minimo_aparece_no_alerta(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
        nome="Produto no Limite",
        sku="ALERTA-LIMITE-001",
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        quantidade=10,
        estoque_minimo=10,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        f"/estoques/loja/{loja.id}/alertas/baixo",
        headers=headers,
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["produto_id"] == produto.id
    assert dados[0]["quantidade"] == 10
    assert dados[0]["estoque_minimo"] == 10


def test_operador_pode_consultar_alertas_da_propria_loja(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
        nome="Produto Baixo Operador",
        sku="ALERTA-OPERADOR-001",
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        quantidade=3,
        estoque_minimo=5,
    )

    headers = criar_headers_operador(
        db_session,
        loja_id=loja.id,
    )

    resposta = client.get(
        f"/estoques/loja/{loja.id}/alertas/baixo",
        headers=headers,
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["produto_id"] == produto.id
    assert dados[0]["loja_id"] == loja.id
    assert dados[0]["quantidade"] == 3
    assert dados[0]["estoque_minimo"] == 5


def test_operador_nao_pode_consultar_alertas_de_outra_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja do Operador",
        endereco="Rua do Operador, 100",
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Outra Loja",
        endereco="Rua da Outra Loja, 200",
    )

    headers = criar_headers_operador(
        db_session,
        loja_id=loja_operador.id,
    )

    resposta = client.get(
        f"/estoques/loja/{outra_loja.id}/alertas/baixo",
        headers=headers,
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )


def test_consultar_alertas_sem_autenticacao_retorna_401(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    resposta = client.get(
        f"/estoques/loja/{loja.id}/alertas/baixo",
    )

    assert resposta.status_code == 401