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

### 4. Criar banco de dados

```bash
# Criar database no PostgreSQL
createdb scrapping_db

# Executar migrations
uv run alembic upgrade head
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
- Verifique se o PostgreSQL está rodando
- Confirme a `DATABASE_URL` no `.env`

### Erro ao baixar modelo spaCy
- Certifique-se de ter internet
- Tente: `uv run python -m spacy download pt_core_news_sm --user`

### Erro de importação
- Verifique se todas as dependências foram instaladas: `uv sync`
- Confirme que está no diretório correto

