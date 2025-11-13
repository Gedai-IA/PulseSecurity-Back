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
cp .env.example .env
# Edite o .env com suas configurações
```

4. Baixe o modelo spaCy:
```bash
uv run python -m spacy download pt_core_news_sm
```

5. Execute as migrations:
```bash
uv run alembic upgrade head
```

6. Inicie o servidor:
```bash
uv run uvicorn app.main:app --reload
```

## Estrutura do Projeto

```
app/
├── domain/          # Entidades e value objects
├── application/     # Casos de uso e serviços
├── infrastructure/  # Implementações técnicas
├── api/            # Rotas e schemas da API
└── core/           # Configurações e utilitários
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

### Criar migration:
```bash
uv run alembic revision --autogenerate -m "description"
```

## API Documentation

Após iniciar o servidor, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

