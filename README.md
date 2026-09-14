# 📦 Estoque Multiloja API

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Tests](https://img.shields.io/badge/tests-104%20passing-brightgreen)
![Deploy](https://img.shields.io/badge/deploy-live-brightgreen)

API REST desenvolvida para gerenciamento de estoque de múltiplas lojas.

O projeto permite cadastrar lojas e produtos, controlar o estoque individual de cada unidade, registrar entradas e saídas, consultar movimentações, configurar estoque mínimo e identificar itens com estoque baixo.

A versão **v1.1.0** também adiciona autenticação JWT, usuários, perfis de acesso e restrições por loja.

O objetivo do projeto é aplicar conceitos de desenvolvimento Backend utilizando Python, FastAPI, SQLAlchemy e PostgreSQL, com autenticação, migrations, validações, regras de negócio, tratamento de erros e testes automatizados.

---

## 🌐 Demonstração online

A API está disponível publicamente para demonstração com dados fictícios de lojas, produtos, estoques e movimentações.

### 🔗 Acessos

* 🚀 **[Acessar API](https://estoque-multiloja-api.onrender.com)**
* 📚 **[Abrir documentação Swagger](https://estoque-multiloja-api.onrender.com/docs)**

> O ambiente público funciona em **modo somente leitura**. Operações de consulta estão liberadas, enquanto operações que alteram dados permanecem bloqueadas.

A rota de login é liberada no ambiente de demonstração para permitir autenticação:

```http
POST /auth/login
```

---

## 🆕 Versão atual

```text
v1.1.0
```

Principais evoluções em relação à v1.0.1:

* autenticação com JWT;
* cadastro e gerenciamento de usuários;
* perfis `admin` e `operador`;
* controle de acesso por loja;
* proteção dos endpoints;
* estoque mínimo por produto e loja;
* alertas de estoque baixo;
* filtros de produtos;
* filtro de movimentações por tipo;
* ampliação da suíte automatizada para 104 testes.

---

## 🚀 Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* PyJWT
* bcrypt
* Pytest
* SQLite para testes automatizados
* Docker Compose
* Git e GitHub

---

## ⚙️ Funcionalidades

### 🔐 Autenticação

* Login utilizando e-mail e senha
* Geração de access token JWT
* Token Bearer
* Validade de 60 minutos
* Rejeição de tokens inválidos
* Rejeição de tokens expirados
* Bloqueio de usuários inativos
* Integração com o botão **Authorize** do Swagger

### 👥 Usuários

* Cadastrar usuário
* Listar usuários
* Buscar usuário por ID
* Atualizar usuário
* Ativar e desativar usuários
* E-mail único
* Senha mínima de 8 caracteres
* Senhas armazenadas somente através de hash
* Criação do primeiro administrador por script

### 🛡️ Perfis e permissões

Existem dois perfis:

```text
admin
operador
```

#### Admin

O administrador pode:

* gerenciar usuários;
* cadastrar, editar e excluir lojas;
* cadastrar, editar e excluir produtos;
* consultar estoques de qualquer loja;
* consultar movimentações de qualquer loja;
* registrar movimentações;
* configurar estoque mínimo;
* consultar alertas de estoque baixo de qualquer loja.

#### Operador

O operador é vinculado obrigatoriamente a uma loja.

Pode:

* consultar a própria loja;
* consultar produtos;
* consultar estoque da própria loja;
* consultar movimentações da própria loja;
* registrar entradas e saídas na própria loja;
* consultar alertas de estoque baixo da própria loja.

Não pode:

* gerenciar usuários;
* cadastrar, editar ou excluir lojas;
* cadastrar, editar ou excluir produtos;
* configurar estoque mínimo;
* acessar estoque ou movimentações de outra loja.

Tentativas de acesso a outra loja retornam:

```text
403 Forbidden
```

### 🏪 Lojas

* Cadastrar loja
* Listar lojas
* Buscar loja por ID
* Atualizar loja
* Excluir loja
* Validação dos tipos `matriz` e `filial`
* Proteção contra exclusão de lojas com estoque ou movimentações vinculadas
* Controle de acesso conforme o perfil autenticado

### 📦 Produtos

* Cadastrar produto
* Listar produtos
* Buscar produto por ID
* Atualizar produto
* Excluir produto
* Validação de preço
* SKU único
* Filtro por nome
* Filtro por categoria
* Filtro por SKU
* Combinação de filtros
* Proteção contra exclusão de produtos com estoque ou movimentações vinculadas

### 📊 Estoque

* Consultar estoque de uma loja
* Consultar estoque de um produto em uma loja específica
* Controle independente por loja
* Impedimento de estoque negativo
* Estoque mínimo por produto e loja
* Configuração de estoque mínimo por administrador
* Valor padrão de estoque mínimo igual a `0`
* Consulta de alertas de estoque baixo
* Controle de acesso por loja

### 🔄 Movimentações

* Registrar entrada
* Registrar saída
* Atualização automática do estoque
* Validação de saldo disponível
* Impedimento de saída superior ao saldo
* Histórico de movimentações
* Filtro por loja
* Filtro por produto
* Filtro por tipo
* Combinação de filtros
* Paginação utilizando `limit` e `offset`
* Restrição automática do operador à própria loja

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
│   │   ├── dependencies/
│   │   │   ├── auth.py
│   │   │   └── permissoes.py
│   │   │
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── estoques.py
│   │       ├── lojas.py
│   │       ├── movimentacoes.py
│   │       ├── produtos.py
│   │       └── usuarios.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── crud/
│   │   ├── estoque.py
│   │   ├── loja.py
│   │   ├── movimentacao.py
│   │   ├── produto.py
│   │   └── usuario.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── estoque.py
│   │   ├── loja.py
│   │   ├── movimentacao.py
│   │   ├── produto.py
│   │   └── usuario.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── estoque.py
│   │   ├── loja.py
│   │   ├── movimentacao.py
│   │   ├── produto.py
│   │   └── usuario.py
│   │
│   ├── scripts/
│   │   └── create_admin.py
│   │
│   └── main.py
│
├── docs/
│   └── superpowers/
│       ├── plans/
│       └── specs/
│
├── tests/
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

O sistema trabalha principalmente com cinco entidades.

### Loja

Representa cada unidade da empresa.

Principais campos:

```text
id
nome
endereco
tipo
```

Tipos permitidos:

```text
matriz
filial
```

### Produto

Representa os produtos cadastrados.

```text
id
nome
categoria
preco
sku
```

Cada produto possui um SKU único.

### Estoque

Relaciona um produto a uma loja.

```text
id
produto_id
loja_id
quantidade
estoque_minimo
```

Um mesmo produto pode possuir quantidades e estoques mínimos diferentes em lojas diferentes.

Cada combinação de produto e loja possui apenas um registro de estoque.

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

Os principais tipos utilizados pela API são:

```text
entrada
saida
```

### Usuário

Representa uma conta que pode acessar a API.

```text
id
nome
email
senha_hash
perfil
ativo
loja_id
```

Regras importantes:

* e-mail único;
* senha nunca armazenada em texto puro;
* administrador pode não possuir loja;
* operador deve possuir uma loja vinculada;
* usuário inativo não pode autenticar.

---

## 🔗 Relacionamentos

```text
Loja 1:N Estoque

Produto 1:N Estoque

Loja 1:N Movimentação

Produto 1:N Movimentação

Loja 1:N Usuário
```

---

## 📋 Pré-requisitos

Antes de executar o projeto, tenha instalado:

* Python
* PostgreSQL
* Git

Opcionalmente:

* Docker
* Docker Compose

---

## 📥 Clonando o projeto

```bash
git clone https://github.com/MaxwellSilvaDev/estoque-multiloja-api.git
```

Entre na pasta:

```bash
cd estoque-multiloja-api
```

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

O projeto possui:

```text
.env.example
```

Crie uma cópia chamada:

```text
.env
```

Exemplo de configuração:

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=estoque_multiloja

DATABASE_URL=postgresql+psycopg2://seu_usuario:sua_senha@localhost:5432/estoque_multiloja

JWT_SECRET=gere_uma_chave_secreta_forte
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=60

DEMO_READ_ONLY=false
```

> Nunca envie o arquivo `.env`, senhas, `DATABASE_URL` real ou `JWT_SECRET` para o repositório.

---

## 🐘 Banco de dados com Docker

O projeto possui `docker-compose.yml`, que pode ser utilizado para iniciar o PostgreSQL.

```bash
docker compose up -d
```

Caso utilize PostgreSQL instalado localmente, configure a `DATABASE_URL` para o seu ambiente.

---

## 🗄️ Executando as migrations

Com o banco funcionando:

```bash
alembic upgrade head
```

Para verificar a migration atual:

```bash
alembic current
```

Na v1.1.0, o banco deve alcançar:

```text
b8d7e843d31e (head)
```

---

## 👤 Criando o primeiro administrador

O sistema não possui cadastro público de usuários.

O primeiro administrador pode ser criado através do script:

```bash
python -m app.scripts.create_admin
```

O script solicita os dados necessários de forma interativa.

A senha não é exibida nem armazenada em texto puro.

Após a criação do primeiro administrador, novos usuários podem ser cadastrados pelos endpoints administrativos da API.

---

## ▶️ Executando a API

```bash
uvicorn app.main:app --reload
```

Aplicação:

```text
http://127.0.0.1:8000
```

---

## 📖 Swagger e ReDoc

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Para acessar endpoints protegidos:

1. faça login em `/auth/login`;
2. copie o `access_token`;
3. clique em **Authorize** no Swagger;
4. informe o token Bearer.

---

## 🛣️ Principais endpoints

### Autenticação

```http
POST /auth/login
```

### Usuários

```http
POST /usuarios
GET /usuarios
GET /usuarios/{usuario_id}
PATCH /usuarios/{usuario_id}
```

Endpoints de usuários são administrativos.

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

Consultar os estoques de uma loja:

```http
GET /estoques/loja/{loja_id}
```

Consultar um produto em uma loja:

```http
GET /estoques/loja/{loja_id}/produto/{produto_id}
```

Configurar estoque mínimo:

```http
PATCH /estoques/loja/{loja_id}/produto/{produto_id}/minimo
```

Consultar alertas de estoque baixo:

```http
GET /estoques/loja/{loja_id}/alertas/baixo
```

### Movimentações

Entrada:

```http
POST /movimentacoes/entrada
```

Saída:

```http
POST /movimentacoes/saida
```

Histórico:

```http
GET /movimentacoes
```

---

## 🔐 Exemplo de login

Requisição:

```http
POST /auth/login
```

Body:

```json
{
  "email": "usuario@example.com",
  "senha": "sua_senha"
}
```

Resposta válida:

```json
{
  "access_token": "<token-jwt>",
  "token_type": "bearer"
}
```

O token deve ser enviado nos endpoints protegidos:

```text
Authorization: Bearer <token-jwt>
```

---

## 🔎 Filtros de produtos

O endpoint:

```http
GET /produtos
```

aceita filtros opcionais.

### Nome

Busca parcial e case-insensitive:

```http
GET /produtos?nome=arroz
```

### Categoria

```http
GET /produtos?categoria=Alimentos
```

### SKU

```http
GET /produtos?sku=PROD-001
```

### Combinando filtros

```http
GET /produtos?nome=gamer&categoria=Periféricos&sku=PROD-001
```

---

## 🔎 Filtros de movimentações

### Por loja

```http
GET /movimentacoes?loja_id=1
```

### Por produto

```http
GET /movimentacoes?produto_id=1
```

### Por tipo

```http
GET /movimentacoes?tipo=saida
```

### Combinados

```http
GET /movimentacoes?loja_id=1&produto_id=1&tipo=saida
```

Mesmo utilizando filtros, operadores continuam limitados à própria loja.

---

## 📄 Paginação

O histórico de movimentações possui paginação com `limit` e `offset`.

```http
GET /movimentacoes?limit=20&offset=0
```

Próxima página:

```http
GET /movimentacoes?limit=20&offset=20
```

Com filtros:

```http
GET /movimentacoes?loja_id=1&produto_id=1&tipo=saida&limit=10&offset=0
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

1. verifica se o usuário possui acesso à loja;
2. verifica se o produto existe;
3. verifica se a loja existe;
4. localiza ou cria o estoque;
5. adiciona a quantidade;
6. registra a movimentação.

---

## 📤 Exemplo de saída de estoque

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

A API verifica se existe saldo suficiente.

Caso contrário:

```json
{
  "detail": "Saldo de estoque insuficiente."
}
```

---

## 📉 Estoque mínimo

O estoque mínimo é configurado individualmente para cada combinação de produto e loja.

Endpoint administrativo:

```http
PATCH /estoques/loja/{loja_id}/produto/{produto_id}/minimo
```

Body:

```json
{
  "estoque_minimo": 10
}
```

Regras:

* somente administradores podem alterar;
* operadores podem visualizar;
* valor negativo é inválido;
* novos registros de estoque começam com mínimo `0`.

---

## 🚨 Alertas de estoque baixo

Endpoint:

```http
GET /estoques/loja/{loja_id}/alertas/baixo
```

Um estoque entra no alerta quando:

```text
estoque_minimo > 0
e
quantidade <= estoque_minimo
```

Se `estoque_minimo` for `0`, o item não aparece como alerta configurado.

Administradores podem consultar qualquer loja.

Operadores podem consultar somente a própria loja.

---

## 🧪 Testes automatizados

O projeto utiliza `pytest` e `FastAPI TestClient`.

Durante os testes é utilizado um banco SQLite isolado do PostgreSQL da aplicação.

As foreign keys são ativadas no ambiente de testes para validar as regras de integridade.

Execute:

```bash
python -m pytest -v
```

Ou no Windows:

```bash
venv\Scripts\python.exe -m pytest -v
```

Estado validado da v1.1.0:

```text
104 testes passando
```

Os testes cobrem cenários como:

* autenticação;
* JWT válido, inválido e expirado;
* usuário inativo;
* hash de senha;
* cadastro de usuários;
* e-mail duplicado;
* criação do primeiro administrador;
* permissões de admin;
* permissões de operador;
* bloqueio entre lojas;
* cadastro de lojas;
* cadastro de produtos;
* preço inválido;
* SKU duplicado;
* entrada de estoque;
* saída de estoque;
* saldo insuficiente;
* consultas de estoque;
* estoque mínimo;
* estoque mínimo negativo;
* alertas de estoque baixo;
* filtros de produtos;
* combinação de filtros;
* filtros de movimentações;
* paginação;
* proteção contra exclusão de registros vinculados;
* comportamento do modo de demonstração.

---

## 🔒 Regras de negócio

Algumas regras implementadas:

* senhas nunca são armazenadas em texto puro;
* usuários inativos não podem autenticar;
* somente administradores gerenciam usuários;
* somente administradores alteram lojas e produtos;
* operador pertence obrigatoriamente a uma loja;
* operador não pode acessar dados de outra loja;
* estoque nunca pode possuir quantidade negativa;
* saída não pode ser maior que o saldo;
* SKU deve ser único;
* cada combinação produto + loja possui apenas um estoque;
* quantidades movimentadas devem ser maiores que zero;
* estoque mínimo não pode ser negativo;
* alertas exigem estoque mínimo maior que zero;
* produtos vinculados não podem ser excluídos;
* lojas vinculadas não podem ser excluídas;
* histórico pode ser filtrado e paginado.

---

## 🧰 Migrations

O schema do banco é gerenciado pelo Alembic.

Criar uma migration:

```bash
alembic revision --autogenerate -m "descricao da migration"
```

Aplicar:

```bash
alembic upgrade head
```

Verificar:

```bash
alembic current
```

---

## 📌 Status do projeto

### v1.1.0

```text
✅ Cadastro de lojas
✅ Cadastro de produtos
✅ Controle de estoque por loja
✅ Entrada de produtos
✅ Saída de produtos
✅ Histórico de movimentações
✅ Paginação
✅ Autenticação JWT
✅ Usuários
✅ Hash seguro de senha
✅ Perfis admin e operador
✅ Controle de acesso por loja
✅ Proteção dos endpoints
✅ Ativação e desativação de usuários
✅ Script para primeiro administrador
✅ Estoque mínimo
✅ Alertas de estoque baixo
✅ Filtros de produtos
✅ Filtro de movimentações por tipo
✅ Combinação de filtros
✅ Validações
✅ Tratamento de conflitos
✅ Migrations
✅ 104 testes automatizados
✅ Variáveis de ambiente
✅ Modo público somente leitura
✅ Deploy em ambiente público
✅ CI/CD com GitHub Actions
```

---

## 🔮 Próximas evoluções

Possíveis evoluções futuras:

* dashboard web;
* frontend integrado;
* relatórios de estoque;
* auditoria detalhada;
* logs estruturados;
* monitoramento;
* backups automatizados;
* recuperação de senha;
* refresh token;
* melhorias adicionais de concorrência;
* arquitetura multiempresa.

---

## 🎯 Objetivo

Este projeto foi desenvolvido como parte do meu portfólio de desenvolvimento Backend, com foco na construção de uma API organizada, segura, testável e baseada em regras de negócio reais.

A evolução da v1.0.1 para a v1.1.0 adiciona uma camada completa de autenticação e autorização, além de recursos operacionais de estoque mínimo, alertas e consultas mais flexíveis.

---

## 👨‍💻 Autor

**Maxwell Silva**

Estudante de Engenharia de Software e desenvolvedor em formação, com interesse em desenvolvimento Backend, bancos de dados e APIs REST.

GitHub:

```text
MaxwellSilvaDev
```
