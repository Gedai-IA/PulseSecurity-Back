# Quick Start Guide

## Setup Rápido

### 1. Instalar dependências

```bash
uv sync
```

### 2. Configurar variáveis de ambiente

```bash
cp env.example .env
# Edite o .env com suas configurações
```

**Importante:** Configure pelo menos:
- `DATABASE_URL`: URL do PostgreSQL
- `SECRET_KEY`: Chave secreta para JWT (gere uma aleatória)

### 3. Baixar modelo spaCy

```bash
uv run python -m spacy download pt_core_news_sm
```

### 4. Configurar Banco de Dados

**⚠️ IMPORTANTE:** Use o script de configuração automática para configurar o PostgreSQL:

```bash
# Execute da raiz do projeto (gedai/) ou do diretório scrapping-backend
./setup-postgres.sh

# Ou se estiver no diretório scrapping-backend:
cd scrapping-backend
./setup-postgres.sh
```

Este script irá:
- Instalar PostgreSQL (se necessário)
- Iniciar o serviço PostgreSQL
- Criar o banco de dados `scrapping_db`
- Criar o usuário `scrapping_user`
- Configurar o arquivo `.env` automaticamente

**Alternativa - Configuração Manual:**

Se preferir fazer manualmente:

```bash
# Instalar PostgreSQL
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Iniciar serviço
sudo service postgresql start

# Criar banco e usuário
sudo -u postgres psql -c "CREATE DATABASE scrapping_db;"
sudo -u postgres psql -c "CREATE USER scrapping_user WITH PASSWORD 'scrapping_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE scrapping_db TO scrapping_user;"
sudo -u postgres psql -d scrapping_db -c "GRANT ALL ON SCHEMA public TO scrapping_user;"
```

#### 4.2. Executar Migrations

**Opção A - Usando Alembic (recomendado):**
```bash
# Aplicar todas as migrations
make upgrade
# ou
uv run alembic upgrade head
```

**Opção B - Usando Scripts SQL (se migrations não funcionarem):**
```bash
# Criar todas as tabelas
./scripts/apply-all-tables.sh

# Ou criar apenas a tabela users
./scripts/apply-sql-migration.sh
```

**Verificar se as tabelas foram criadas:**
```bash
psql -h localhost -U scrapping_user -d scrapping_db -c "\dt"
```

### 5. Importar dados JSON (opcional)

```bash
uv run python scripts/import_json.py <caminho_para_arquivo.json>
```

### 6. Iniciar servidor

```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000

## Endpoints Principais

- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Exemplos de Uso

#### Listar publicações
```bash
curl http://localhost:8000/api/v1/publications
```

#### Obter estatísticas do dashboard
```bash
curl http://localhost:8000/api/v1/dashboard/stats
```

#### Buscar publicações
```bash
curl "http://localhost:8000/api/v1/publications/search?q=violência"
```

## Comandos Úteis

```bash
# Rodar testes
uv run pytest

# Formatar código
make format

# Criar nova migration
make migrate msg="descrição da migration"

# Aplicar migrations
make upgrade
```

## Troubleshooting

### Erro de conexão com banco
- Verifique se o PostgreSQL está rodando: `sudo service postgresql status`
- Confirme a `DATABASE_URL` no `.env`
- Teste a conexão: `psql -h localhost -U scrapping_user -d scrapping_db`

### Erro: "relation does not exist"
- As tabelas não foram criadas. Execute:
  ```bash
  ./scripts/apply-all-tables.sh
  ```

### Erro: "Target database is not up to date"
- Aplique as migrations pendentes:
  ```bash
  make upgrade
  ```

### Erro ao baixar modelo spaCy
- Certifique-se de ter internet
- Tente: `uv run python -m spacy download pt_core_news_sm --user`

### Erro de importação
- Verifique se todas as dependências foram instaladas: `uv sync`
- Confirme que está no diretório correto

