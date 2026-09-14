from decimal import Decimal

from app.core.config import settings
from app.core.security import criar_token_acesso
from app.crud.usuario import criar_usuario
from app.models.loja import Loja
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.schemas.usuario import UsuarioCreate
from tests.conftest import client


def criar_produto_teste(
    db_session,
    nome: str,
    categoria: str,
    sku: str,
) -> Produto:
    produto = Produto(
        nome=nome,
        categoria=categoria,
        preco=Decimal("100.00"),
        sku=sku,
    )

    db_session.add(produto)
    db_session.commit()
    db_session.refresh(produto)

    return produto


def criar_loja_teste(
    db_session,
    nome: str = "Loja Filtros",
    endereco: str = "Rua dos Filtros, 100",
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


def test_filtrar_produtos_por_nome_parcial(
    db_session,
):
    produto_arroz = criar_produto_teste(
        db_session,
        nome="Arroz Integral",
        categoria="Alimentos",
        sku="FILTRO-001",
    )

    criar_produto_teste(
        db_session,
        nome="Feijão Carioca",
        categoria="Alimentos",
        sku="FILTRO-002",
    )

    criar_produto_teste(
        db_session,
        nome="Macarrão",
        categoria="Alimentos",
        sku="FILTRO-003",
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/produtos",
        headers=headers,
        params={
            "nome": "ARROZ",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == produto_arroz.id
    assert dados[0]["nome"] == "Arroz Integral"


def test_filtrar_produtos_por_categoria(
    db_session,
):
    produto_teclado = criar_produto_teste(
        db_session,
        nome="Teclado Mecânico",
        categoria="Periféricos",
        sku="FILTRO-CAT-001",
    )

    criar_produto_teste(
        db_session,
        nome="Mouse Gamer",
        categoria="Periféricos",
        sku="FILTRO-CAT-002",
    )

    criar_produto_teste(
        db_session,
        nome="Notebook",
        categoria="Computadores",
        sku="FILTRO-CAT-003",
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/produtos",
        headers=headers,
        params={
            "categoria": "Computadores",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["nome"] == "Notebook"
    assert dados[0]["categoria"] == "Computadores"
    assert all(
        item["id"] != produto_teclado.id
        for item in dados
    )


def test_filtrar_produtos_por_sku(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
        nome="Monitor",
        categoria="Periféricos",
        sku="SKU-EXATO-001",
    )

    criar_produto_teste(
        db_session,
        nome="Webcam",
        categoria="Periféricos",
        sku="SKU-EXATO-002",
    )

    criar_produto_teste(
        db_session,
        nome="Headset",
        categoria="Periféricos",
        sku="SKU-EXATO-003",
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/produtos",
        headers=headers,
        params={
            "sku": "SKU-EXATO-001",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == produto.id
    assert dados[0]["nome"] == "Monitor"
    assert dados[0]["sku"] == "SKU-EXATO-001"


def test_combinar_filtros_de_produtos(
    db_session,
):
    produto = criar_produto_teste(
        db_session,
        nome="Mouse Gamer Pro",
        categoria="Periféricos",
        sku="COMBO-001",
    )

    criar_produto_teste(
        db_session,
        nome="Mouse Office",
        categoria="Periféricos",
        sku="COMBO-002",
    )

    criar_produto_teste(
        db_session,
        nome="Mouse Gamer Pro",
        categoria="Acessórios",
        sku="COMBO-003",
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/produtos",
        headers=headers,
        params={
            "nome": "gamer",
            "categoria": "Periféricos",
            "sku": "COMBO-001",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == produto.id
    assert dados[0]["nome"] == "Mouse Gamer Pro"
    assert dados[0]["categoria"] == "Periféricos"
    assert dados[0]["sku"] == "COMBO-001"


def test_filtrar_movimentacoes_por_tipo(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    produto = criar_produto_teste(
        db_session,
        nome="Produto Movimentação",
        categoria="Teste",
        sku="MOV-TIPO-001",
    )

    criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        tipo="entrada",
        quantidade=10,
    )

    movimentacao_saida = criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        tipo="saida",
        quantidade=3,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/movimentacoes",
        headers=headers,
        params={
            "tipo": "saida",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == movimentacao_saida.id
    assert dados[0]["tipo"] == "saida"
    assert dados[0]["quantidade"] == 3


def test_combinar_filtros_de_movimentacoes(
    db_session,
):
    loja = criar_loja_teste(
        db_session,
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Outra Loja Filtros",
        endereco="Rua Secundária, 200",
    )

    produto = criar_produto_teste(
        db_session,
        nome="Produto Principal",
        categoria="Teste",
        sku="MOV-COMBO-001",
    )

    outro_produto = criar_produto_teste(
        db_session,
        nome="Outro Produto",
        categoria="Teste",
        sku="MOV-COMBO-002",
    )

    movimentacao_esperada = criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        tipo="saida",
        quantidade=2,
    )

    criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja.id,
        tipo="entrada",
        quantidade=10,
    )

    criar_movimentacao_teste(
        db_session,
        produto_id=outro_produto.id,
        loja_id=loja.id,
        tipo="saida",
        quantidade=4,
    )

    criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=outra_loja.id,
        tipo="saida",
        quantidade=5,
    )

    headers = criar_headers_admin(
        db_session,
    )

    resposta = client.get(
        "/movimentacoes",
        headers=headers,
        params={
            "loja_id": loja.id,
            "produto_id": produto.id,
            "tipo": "saida",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == movimentacao_esperada.id
    assert dados[0]["loja_id"] == loja.id
    assert dados[0]["produto_id"] == produto.id
    assert dados[0]["tipo"] == "saida"


def test_operador_filtra_tipo_apenas_na_propria_loja(
    db_session,
):
    loja_operador = criar_loja_teste(
        db_session,
        nome="Loja Operador Filtros",
        endereco="Rua Operador, 100",
    )

    outra_loja = criar_loja_teste(
        db_session,
        nome="Loja Externa Filtros",
        endereco="Rua Externa, 200",
    )

    produto = criar_produto_teste(
        db_session,
        nome="Produto do Operador",
        categoria="Teste",
        sku="MOV-OPERADOR-001",
    )

    movimentacao_esperada = criar_movimentacao_teste(
        db_session,
        produto_id=produto.id,
        loja_id=loja_operador.id,
        tipo="saida",
        quantidade=2,
    )

    criar_movimentacao_teste(
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
        tipo="saida",
        quantidade=7,
    )

    headers = criar_headers_operador(
        db_session,
        loja_id=loja_operador.id,
    )

    resposta = client.get(
        "/movimentacoes",
        headers=headers,
        params={
            "tipo": "saida",
        },
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert len(dados) == 1
    assert dados[0]["id"] == movimentacao_esperada.id
    assert dados[0]["loja_id"] == loja_operador.id
    assert dados[0]["tipo"] == "saida"