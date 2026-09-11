# 📦 Estoque Multiloja API

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![Tests](https://img.shields.io/badge/tests-16%20passing-brightgreen)
![Deploy](https://img.shields.io/badge/deploy-live-brightgreen)

API REST desenvolvida para gerenciamento de estoque de múltiplas lojas.

O projeto permite cadastrar lojas e produtos, controlar o estoque individual de cada unidade, registrar entradas e saídas de produtos e consultar o histórico de movimentações.

O objetivo do projeto é aplicar conceitos de desenvolvimento Backend utilizando Python, FastAPI, SQLAlchemy e PostgreSQL, com migrations, validações, tratamento de erros e testes automatizados.

---

## 🌐 Demonstração online

A API está disponível publicamente para demonstração com dados fictícios de lojas, produtos, estoques e movimentações.

### 🔗 Acessos

- 🚀 **[Acessar API](https://estoque-multiloja-api.onrender.com)**
- 📚 **[Abrir documentação Swagger](https://estoque-multiloja-api.onrender.com/docs)**

> O ambiente público funciona em **modo somente leitura**. Operações de consulta estão liberadas, enquanto operações de escrita são bloqueadas para proteger os dados da demonstração.

---

## 🚀 Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest
- SQLite para testes automatizados
- Docker Compose
- Git e GitHub

---

## ⚙️ Funcionalidades

A API possui atualmente as seguintes funcionalidades:

### 🏪 Lojas

- Cadastrar loja
- Listar lojas
- Buscar loja por ID
- Atualizar loja
- Excluir loja
- Validação dos tipos `matriz` e `filial`
- Proteção contra exclusão de lojas que possuem estoque ou movimentações vinculadas

### 📦 Produtos

- Cadastrar produto
- Listar produtos
- Buscar produto por ID
- Atualizar produto
- Excluir produto
- Validação de preço
- SKU único para cada produto
- Proteção contra exclusão de produtos que possuem estoque ou movimentações vinculadas

### 📊 Estoque

- Consultar estoque de uma loja
- Consultar estoque de um produto em uma loja específica
- Controle independente de quantidade para cada loja
- Impedimento de estoque negativo

### 🔄 Movimentações

- Registrar entrada de produtos
- Registrar saída de produtos
- Atualização automática do estoque
- Validação de saldo disponível
- Impedimento de saída superior ao estoque disponível
- Histórico de movimentações
- Filtro por loja
- Filtro por produto
- Paginação utilizando `limit` e `offset`

---

## 🏗️ Estrutura do projeto

```text
estoque-multiloja-api/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── estoques.py
│   │       ├── lojas.py
│   │       ├── movimentacoes.py
│   │       └── produtos.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── crud/
│   │   ├── estoque.py
│   │   ├── loja.py
│   │   ├── movimentacao.py
│   │   └── produto.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── estoque.py
│   │   ├── loja.py
│   │   ├── movimentacao.py
│   │   └── produto.py
│   │
│   ├── schemas/
│   │   ├── estoque.py
│   │   ├── loja.py
│   │   ├── movimentacao.py
│   │   └── produto.py
│   │
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_estoques.py
│   ├── test_lojas.py
│   ├── test_movimentacoes.py
│   └── test_produtos.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🗃️ Modelo de dados

O sistema trabalha com quatro entidades principais:

### Loja

Representa cada unidade da empresa.

Principais campos:

```text
id
nome
endereco
tipo
```

O tipo da loja pode ser:

```text
matriz
filial
```

### Produto

Representa os produtos cadastrados no sistema.

Principais campos:

```text
id
nome
categoria
preco
sku
```

Cada produto possui um SKU único.

### Estoque

Relaciona um produto a uma loja e armazena sua quantidade disponível.

```text
id
produto_id
loja_id
quantidade
```

Um mesmo produto pode possuir quantidades diferentes em lojas diferentes.

### Movimentação

Registra alterações realizadas no estoque.

```text
id
produto_id
loja_id
tipo
quantidade
data
```

Os principais tipos de movimentação utilizados atualmente são:

```text
entrada
saida
```

---

## 🔗 Relacionamentos

```text
Loja 1:N Estoque

Produto 1:N Estoque

Loja 1:N Movimentação

Produto 1:N Movimentação
```

Cada combinação de produto e loja possui apenas um registro de estoque.

---

## 📋 Pré-requisitos

Antes de executar o projeto, tenha instalado:

- Python
- PostgreSQL
- Git

Opcionalmente:

- Docker
- Docker Compose

---

## 📥 Clonando o projeto

```bash
git clone https://github.com/MaxwellSilvaDev/estoque-multiloja-api.git
```

Entre na pasta:

```bash
cd estoque-multiloja-api
```

> Caso o repositório esteja privado, é necessário possuir permissão de acesso no GitHub.

---

## 🐍 Criando o ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

---

## 📦 Instalando as dependências

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração das variáveis de ambiente

O projeto possui um arquivo:

```text
.env.example
```

Crie uma cópia chamada:

```text
.env
```

Exemplo:

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=estoque_multiloja
DATABASE_URL=postgresql+psycopg2://seu_usuario:sua_senha@localhost:5432/estoque_multiloja
```

O arquivo `.env` contém informações sensíveis e não deve ser enviado para o GitHub.

---

## 🐘 Banco de dados com Docker

O projeto possui um arquivo `docker-compose.yml` que pode ser utilizado para iniciar o PostgreSQL.

Execute:

```bash
docker compose up -d
```

Isso iniciará o banco PostgreSQL configurado para o projeto.

Caso utilize uma instalação local do PostgreSQL, ajuste a variável `DATABASE_URL` conforme a porta e as credenciais do seu ambiente.

---

## 🗄️ Executando as migrations

Com o banco de dados funcionando, execute:

```bash
alembic upgrade head
```

Esse comando cria e atualiza as tabelas necessárias no banco de dados.

Para verificar a migration atual:

```bash
alembic current
```

---

## ▶️ Executando a API

Inicie o servidor utilizando:

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

---

## 📖 Documentação Swagger

O FastAPI gera automaticamente uma interface para visualizar e testar os endpoints.

Acesse:

```text
http://127.0.0.1:8000/docs
```

Também é possível acessar a documentação ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 🛣️ Principais endpoints

### Lojas

```http
POST /lojas
GET /lojas
GET /lojas/{loja_id}
PATCH /lojas/{loja_id}
DELETE /lojas/{loja_id}
```

### Produtos

```http
POST /produtos
GET /produtos
GET /produtos/{produto_id}
PATCH /produtos/{produto_id}
DELETE /produtos/{produto_id}
```

### Estoques

Consultar todos os estoques de uma loja:

```http
GET /estoques/loja/{loja_id}
```

Consultar um produto específico dentro de uma loja:

```http
GET /estoques/loja/{loja_id}/produto/{produto_id}
```

### Movimentações

Registrar entrada:

```http
POST /movimentacoes/entrada
```

Registrar saída:

```http
POST /movimentacoes/saida
```

Consultar histórico:

```http
GET /movimentacoes
```

---

## 🔎 Filtros de movimentações

O histórico permite filtros opcionais.

Por loja:

```http
GET /movimentacoes?loja_id=1
```

Por produto:

```http
GET /movimentacoes?produto_id=1
```

Com os dois filtros:

```http
GET /movimentacoes?loja_id=1&produto_id=1
```

---

## 📄 Paginação

O endpoint de movimentações possui paginação utilizando `limit` e `offset`.

Exemplo:

```http
GET /movimentacoes?limit=20&offset=0
```

Próxima página:

```http
GET /movimentacoes?limit=20&offset=20
```

Também é possível combinar paginação e filtros:

```http
GET /movimentacoes?loja_id=1&produto_id=1&limit=10&offset=0
```

O valor máximo permitido para `limit` é:

```text
100
```

---

## 📥 Exemplo de entrada de estoque

Requisição:

```http
POST /movimentacoes/entrada
```

Body:

```json
{
  "produto_id": 1,
  "loja_id": 1,
  "quantidade": 10
}
```

A API:

1. verifica se o produto existe;
2. verifica se a loja existe;
3. localiza ou cria o estoque;
4. adiciona a quantidade;
5. registra a movimentação.

---

## 📤 Exemplo de saída de estoque

Requisição:

```http
POST /movimentacoes/saida
```

Body:

```json
{
  "produto_id": 1,
  "loja_id": 1,
  "quantidade": 3
}
```

Antes de realizar a saída, a API verifica se existe saldo suficiente.

Caso não exista:

```json
{
  "detail": "Saldo de estoque insuficiente."
}
```

---

## 🧪 Testes automatizados

O projeto possui testes automatizados utilizando `pytest` e `FastAPI TestClient`.

Durante os testes é utilizado um banco SQLite em memória, separado do PostgreSQL utilizado pela aplicação.

As foreign keys são ativadas no ambiente de testes para validar corretamente as regras de integridade.

Execute todos os testes com:

```bash
python -m pytest -v
```

No Windows também é possível utilizar diretamente o Python do ambiente virtual:

```bash
venv\Scripts\python.exe -m pytest -v
```

Estado atual:

```text
16 testes passando
```

Os testes cobrem cenários como:

- cadastro de lojas;
- validação do tipo de loja;
- cadastro de produtos;
- validação de preço;
- SKU duplicado;
- entrada de estoque;
- saída de estoque;
- saldo insuficiente;
- consultas de estoque;
- filtros de movimentações;
- paginação;
- proteção contra exclusão de produtos vinculados;
- proteção contra exclusão de lojas vinculadas.

---

## 🔒 Regras de negócio

Algumas regras implementadas:

- O estoque nunca pode possuir quantidade negativa.
- Uma saída não pode ser maior que o saldo disponível.
- O SKU de um produto deve ser único.
- Cada combinação de produto e loja possui apenas um estoque.
- Quantidades movimentadas devem ser maiores que zero.
- Produtos vinculados a estoque ou movimentações não podem ser excluídos.
- Lojas vinculadas a estoque ou movimentações não podem ser excluídas.
- O histórico de movimentações pode ser filtrado e paginado.

---

## 🧰 Migrations

O gerenciamento do schema do banco é realizado com Alembic.

Criar uma nova migration:

```bash
alembic revision --autogenerate -m "descricao da migration"
```

Aplicar migrations:

```bash
alembic upgrade head
```

---

## 📌 Status do projeto

### MVP

Principais funcionalidades do Backend implementadas.

```text
✅ Cadastro de lojas
✅ Cadastro de produtos
✅ Controle de estoque por loja
✅ Entrada de produtos
✅ Saída de produtos
✅ Histórico de movimentações
✅ Filtros
✅ Paginação
✅ Validações
✅ Tratamento de conflitos
✅ Migrations
✅ Testes automatizados
✅ Variáveis de ambiente
✅ Deploy em ambiente público
✅ CI/CD com GitHub Actions
```

---

## 🔮 Próximas evoluções

Uma futura versão do sistema poderá incluir:

- autenticação com JWT;
- cadastro de usuários;
- perfis e permissões;
- controle de acesso por loja;
- dashboard web;
- frontend integrado à API;
- relatórios de estoque;
- estoque mínimo e alertas;
- auditoria;
- logs;
- monitoramento;
- backups;
- melhorias para concorrência de movimentações;
- arquitetura preparada para múltiplas empresas.

---

## 🎯 Objetivo

Este projeto foi desenvolvido como parte do meu portfólio de desenvolvimento Backend, com foco na construção de uma API organizada, testável e baseada em regras de negócio reais.

Ele também serve como base para futuras evoluções até uma aplicação completa de gerenciamento de estoque.

---

## 👨‍💻 Autor

**Maxwell Silva**

Estudante de Engenharia de Software e desenvolvedor em formação, com interesse em desenvolvimento Backend, bancos de dados e APIs REST.

GitHub:

```text
MaxwellSilvaDev
```