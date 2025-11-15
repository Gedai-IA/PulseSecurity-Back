# Scrapping Backend

Backend API para análise de sentimento, emoções e tópicos em publicações de redes sociais.

## Arquitetura

Este projeto segue os princípios de **Clean Architecture** e **Hexagonal Architecture**, organizado em camadas:

- **Domain**: Entidades e regras de negócio puras
- **Application**: Casos de uso e serviços de aplicação
- **Infrastructure**: Implementações técnicas (banco de dados, NLP, cache)
- **API**: Camada de apresentação (FastAPI)

## Tecnologias

- **FastAPI**: Framework web assíncrono
- **SQLAlchemy 2.0**: ORM assíncrono
- **PostgreSQL**: Banco de dados relacional
- **Redis**: Cache e message broker
- **Celery**: Tarefas assíncronas
- **spaCy + Transformers**: Processamento de linguagem natural
- **Pydantic**: Validação de dados
- **Alembic**: Migrations

## Instalação

### Pré-requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) instalado
- PostgreSQL 14+
- Redis 7+

### Setup

1. Clone o repositório:
```bash
git clone <repo-url>
cd scrapping-backend
```

2. Instale as dependências com uv:
```bash
uv sync
```

3. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o .env com suas configurações
```

**Importante:** Configure pelo menos:
- `DATABASE_URL`: URL do PostgreSQL (ex: `postgresql+asyncpg://user:password@localhost:5432/scrapping_db`)
- `SECRET_KEY`: Chave secreta para JWT (gere uma aleatória)

4. Configure o PostgreSQL:

Se o PostgreSQL não estiver instalado ou configurado, veja a seção [Configuração do Banco de Dados](#configuração-do-banco-de-dados) abaixo.

5. Baixe o modelo spaCy:
```bash
uv run python -m spacy download pt_core_news_sm
```

6. Execute as migrations:

**Opção A - Usando Alembic (recomendado):**
```bash
make upgrade
# ou
uv run alembic upgrade head
```

**Opção B - Usando scripts SQL (se as migrações não funcionarem):**
```bash
# Criar todas as tabelas
./scripts/apply-all-tables.sh

# Ou criar apenas a tabela users
./scripts/apply-sql-migration.sh
```

7. Inicie o servidor:
```bash
make dev
# ou
uv run uvicorn app.main:app --reload
```

## Configuração do Banco de Dados

### Instalar e Configurar PostgreSQL

Se o PostgreSQL não estiver instalado, você pode usar o script de configuração automática:

```bash
# Na raiz do projeto (gedai/)
./setup-postgres.sh
```

Ou configure manualmente:

1. **Instalar PostgreSQL:**
```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
```

2. **Iniciar o serviço:**
```bash
sudo service postgresql start
```

3. **Criar banco de dados e usuário:**
```bash
sudo -u postgres psql -c "CREATE DATABASE scrapping_db;"
sudo -u postgres psql -c "CREATE USER scrapping_user WITH PASSWORD 'scrapping_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE scrapping_db TO scrapping_user;"
```

4. **Configurar o `.env`:**
```env
DATABASE_URL=postgresql+asyncpg://scrapping_user:scrapping_password@localhost:5432/scrapping_db
```

### Migrations

O projeto usa **Alembic** para gerenciar migrations do banco de dados.

#### Estrutura de Dados

Os dados iniciais são carregados automaticamente através das migrations. Os arquivos JSON devem estar na pasta `json/` dentro do diretório do backend:

```
scrapping-backend/
├── json/                    # Arquivos JSON com dados das publicações
│   ├── *.json
│   └── README.md
├── alembic/
│   └── helpers.py          # Funções para processar JSONs
└── ...
```

A migration `populate_json_data` lê todos os arquivos `*.json` da pasta `json/` e os importa diretamente para o banco de dados, processando os dados em memória sem armazenar arquivos intermediários.

#### Aplicar Migrations

```bash
# Usando Makefile (recomendado)
make upgrade

# Ou diretamente
uv run alembic upgrade head
```

**Nota:** Certifique-se de que a pasta `json/` existe e contém os arquivos JSON antes de executar as migrations.

#### Criar Nova Migration

```bash
# Usando Makefile
make migrate msg="descrição da migration"

# Ou diretamente
uv run alembic revision --autogenerate -m "descrição da migration"
```

#### Verificar Status das Migrations

```bash
# Ver migration atual
uv run alembic current

# Ver histórico
uv run alembic history
```

#### Scripts SQL Alternativos

Se as migrations do Alembic não funcionarem, você pode usar os scripts SQL diretos na pasta `scripts/`:

- `./scripts/apply-all-tables.sh` - Cria todas as tabelas
- `./scripts/apply-sql-migration.sh` - Cria apenas a tabela users
- `./scripts/apply-migrations.sh` - Aplica migrations do Alembic

Veja mais detalhes em [`scripts/README.md`](./scripts/README.md).

#### Troubleshooting de Migrations

**Erro: "Target database is not up to date"**
```bash
# Aplique as migrations pendentes primeiro
make upgrade
```

**Erro: "relation does not exist"**
```bash
# Use o script SQL para criar as tabelas
./scripts/apply-all-tables.sh
```

**Sincronizar Alembic após criar tabelas manualmente:**
```bash
# Marca a migration como aplicada sem executá-la
uv run alembic stamp head
```

## Estrutura do Projeto

```
scrapping-backend/
├── app/
│   ├── domain/          # Entidades e value objects
│   ├── application/     # Casos de uso e serviços
│   ├── infrastructure/  # Implementações técnicas
│   ├── api/            # Rotas e schemas da API
│   └── core/           # Configurações e utilitários
├── alembic/            # Migrations do banco de dados
│   └── versions/       # Arquivos de migration
├── scripts/            # Scripts utilitários
│   ├── apply-all-tables.sh      # Cria todas as tabelas via SQL
│   ├── apply-sql-migration.sh   # Cria tabela users via SQL
│   ├── apply-migrations.sh      # Aplica migrations do Alembic
│   ├── create_all_tables.sql    # SQL para criar todas as tabelas
│   └── create_users_table.sql   # SQL para criar tabela users
├── tests/              # Testes automatizados
└── docs/               # Documentação
```

## Desenvolvimento

### Rodar testes:
```bash
uv run pytest
```

### Formatação:
```bash
uv run black .
uv run ruff check --fix .
```

### Migrations:

```bash
# Criar nova migration
make migrate msg="descrição da migration"

# Aplicar migrations
make upgrade

# Reverter última migration
make downgrade

# Ver status atual
uv run alembic current
```

### Scripts de Banco de Dados:

```bash
# Criar todas as tabelas via SQL
./scripts/apply-all-tables.sh

# Criar apenas tabela users via SQL
./scripts/apply-sql-migration.sh

# Aplicar migrations do Alembic
./scripts/apply-migrations.sh
```

## Documentação

Documentação completa disponível em [`docs/`](./docs/):
- [Quick Start](./docs/quickstart.md) - Guia rápido para começar
- [Configuração do Banco de Dados](./docs/database-setup.md) - Setup completo do PostgreSQL e migrations
- [Arquitetura](./docs/architecture.md) - Diagrama de arquitetura e visão geral
- [Diagramas de Sequência](./docs/sequence-diagrams.md) - Fluxos principais
- [Guia de Desenvolvimento](./docs/development.md) - Setup e convenções
- [Documentação da API](./docs/api.md) - Referência completa dos endpoints

Documentação interativa da API (após iniciar o servidor):
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

