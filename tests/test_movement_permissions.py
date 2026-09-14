from decimal import Decimal

from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.models.estoque import Estoque
from app.models.loja import Loja
from app.models.movimentacao import Movimentacao
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
        nome="Produto de Movimentação",
        categoria="Teste",
        preco=Decimal("99.90"),
        sku="MOV-PERM-001",
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


def criar_movimentacao_teste(
    db_session,
    produto_id: int,
    loja_id: int,
    tipo: str,
    quantidade: int,
) -> Movimentacao:
    movimentacao = Movimentacao(
        produto_id=produto_id,
        loja_id=loja_id,
        tipo=tipo,
        quantidade=quantidade,
    )

    db_session.add(movimentacao)
    db_session.commit()
    db_session.refresh(movimentacao)

    return movimentacao


def criar_token_usuario(
    usuario,
) -> str:
    return criar_token_acesso(
        usuario_id=usuario.id,
        chave_secreta=settings.jwt_secret,
    )


def test_listar_movimentacoes_sem_autenticacao_retorna_401():
    resposta = client.get(
        "/movimentacoes",
    )

    assert resposta.status_code == 401


def test_registrar_entrada_sem_autenticacao_retorna_401():
    resposta = client.post(
        "/movimentacoes/entrada",
        json={
            "produto_id": 1,
            "loja_id": 1,
            "quantidade": 10,
        },
    )

    assert resposta.status_code == 401


def test_registrar_saida_sem_autenticacao_retorna_401():
    resposta = client.post(
        "/movimentacoes/saida",
        json={
            "produto_id": 1,
            "loja_id": 1,
            "quantidade": 5,
        },
    )

    assert resposta.status_code == 401


def test_operador_nao_pode_registrar_entrada_em_outra_loja(
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

    produto = criar_produto_teste(
        db_session,
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
        "/movimentacoes/entrada",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "produto_id": produto.id,
            "loja_id": outra_loja.id,
            "quantidade": 10,
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )


def test_operador_nao_pode_registrar_saida_em_outra_loja(
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

    produto = criar_produto_teste(
        db_session,
    )

    criar_estoque_teste(
        db_session,
        produto_id=produto.id,
        loja_id=outra_loja.id,
        quantidade=20,
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
        "/movimentacoes/saida",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "produto_id": produto.id,
            "loja_id": outra_loja.id,
            "quantidade": 5,
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )


def test_operador_lista_apenas_movimentacoes_da_propria_loja(
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

    produto = criar_produto_teste(
        db_session,
    )

    movimentacao_operador = criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja_operador.id,
        tipo="entrada",
        quantidade=10,
    )

    criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=outra_loja.id,
        tipo="entrada",
        quantidade=20,
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
        "/movimentacoes",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == movimentacao_operador.id
    assert dados[0]["loja_id"] == loja_operador.id


def test_operador_nao_pode_filtrar_movimentacoes_de_outra_loja(
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
        f"/movimentacoes?loja_id={outra_loja.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == (
        "Acesso não permitido a esta loja."
    )


def test_operador_pode_registrar_entrada_na_propria_loja(
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

    resposta = client.post(
        "/movimentacoes/entrada",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "produto_id": produto.id,
            "loja_id": loja.id,
            "quantidade": 10,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["tipo"] == "entrada"
    assert dados["quantidade"] == 10


def test_operador_pode_registrar_saida_na_propria_loja(
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
        quantidade=20,
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

    resposta = client.post(
        "/movimentacoes/saida",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "produto_id": produto.id,
            "loja_id": loja.id,
            "quantidade": 5,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["tipo"] == "saida"
    assert dados["quantidade"] == 5


def test_admin_pode_consultar_movimentacoes_de_qualquer_loja(
    db_session,
):
    loja_1 = criar_loja_teste(
        db_session,
        nome="Loja 1",
        endereco="Rua Um, 100",
    )

    loja_2 = criar_loja_teste(
        db_session,
        nome="Loja 2",
        endereco="Rua Dois, 200",
    )

    produto = criar_produto_teste(
        db_session,
    )

    criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja_1.id,
        tipo="entrada",
        quantidade=10,
    )

    movimentacao_loja_2 = criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja_2.id,
        tipo="entrada",
        quantidade=20,
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
        f"/movimentacoes?loja_id={loja_2.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == movimentacao_loja_2.id
    assert dados[0]["loja_id"] == loja_2.id


def test_admin_pode_registrar_entrada_em_qualquer_loja(
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
        "/movimentacoes/entrada",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "produto_id": produto.id,
            "loja_id": loja.id,
            "quantidade": 30,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["tipo"] == "entrada"
    assert dados["quantidade"] == 30


def test_admin_pode_registrar_saida_em_qualquer_loja(
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
        quantidade=50,
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

    resposta = client.post(
        "/movimentacoes/saida",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "produto_id": produto.id,
            "loja_id": loja.id,
            "quantidade": 15,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["produto_id"] == produto.id
    assert dados["loja_id"] == loja.id
    assert dados["tipo"] == "saida"
    assert dados["quantidade"] == 15