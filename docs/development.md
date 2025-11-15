# Guia de Desenvolvimento

## Pré-requisitos

- Python 3.11 ou superior
- [uv](https://github.com/astral-sh/uv) instalado
- PostgreSQL 14+ instalado e rodando
- Redis 7+ instalado e rodando (opcional para desenvolvimento)

## Setup Inicial

### 1. Clone o Repositório

```bash
git clone <repo-url>
cd scrapping-backend
```

### 2. Instale as Dependências

```bash
uv sync
```

Isso criará um ambiente virtual e instalará todas as dependências listadas no `pyproject.toml`.

### 3. Configure as Variáveis de Ambiente

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/scrapping_db
SECRET_KEY=sua-chave-secreta-aqui
REDIS_URL=redis://localhost:6379/0
```

### 4. Baixe o Modelo spaCy

```bash
uv run python -m spacy download pt_core_news_sm
```

### 5. Configure o Banco de Dados

#### Opção A - Script Automatizado (Recomendado)

**⚠️ IMPORTANTE:** Use o script de configuração automática antes de continuar. Ele instala e configura tudo automaticamente:

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
- Configurar o arquivo `.env` com as credenciais corretas

**Após executar o script, continue com o passo 6 (Executar Migrations) abaixo.**

#### Opção B - Configuração Manual

Se preferir fazer manualmente:

**Instalar PostgreSQL:**
```bash
# Instalar PostgreSQL
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Iniciar serviço
sudo service postgresql start
```

**Criar Banco de Dados e Usuário:**
```bash
# Criar database
sudo -u postgres psql -c "CREATE DATABASE scrapping_db;"

# Criar usuário
sudo -u postgres psql -c "CREATE USER scrapping_user WITH PASSWORD 'scrapping_password';"

# Conceder privilégios
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE scrapping_db TO scrapping_user;"
sudo -u postgres psql -d scrapping_db -c "GRANT ALL ON SCHEMA public TO scrapping_user;"
```

#### Executar Migrations

**Opção A - Usando Alembic (recomendado):**
```bash
# Aplicar todas as migrations
make upgrade
# ou
uv run alembic upgrade head
```

**Opção B - Usando Scripts SQL:**
```bash
# Criar todas as tabelas via SQL
./scripts/apply-all-tables.sh
```

**Verificar tabelas criadas:**
```bash
psql -h localhost -U scrapping_user -d scrapping_db -c "\dt"
```

### 6. Inicie o Servidor

```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000

## Estrutura do Projeto

```
scrapping-backend/
├── app/
│   ├── domain/              # Entidades e regras de negócio
│   │   ├── entities/
│   │   └── value_objects/
│   ├── application/         # Casos de uso e serviços
│   │   └── services/
│   ├── infrastructure/      # Implementações técnicas
│   │   ├── database/
│   │   ├── nlp/
│   │   └── cache/
│   ├── api/                # Rotas e schemas da API
│   │   └── v1/
│   └── core/               # Configurações e utilitários
├── alembic/                # Migrations
├── scripts/                # Scripts utilitários
├── tests/                  # Testes
└── docs/                   # Documentação
```

## Comandos Úteis

### Desenvolvimento

```bash
# Iniciar servidor em modo desenvolvimento
uv run uvicorn app.main:app --reload

# Ou usar o Makefile
make dev
```

### Testes

```bash
# Rodar todos os testes
uv run pytest

# Rodar com coverage
uv run pytest --cov=app --cov-report=html

# Rodar testes específicos
uv run pytest tests/test_publications.py
```

### Formatação e Linting

```bash
# Formatar código
uv run black .

# Verificar linting
uv run ruff check .

# Corrigir problemas automaticamente
uv run ruff check --fix .

# Verificar tipos
uv run mypy app

# Ou usar o Makefile
make format
make lint
```

### Migrations

O projeto usa **Alembic** para gerenciar migrations do banco de dados.

#### Comandos Básicos

```bash
# Criar nova migration
make migrate msg="descrição da migration"
# ou
uv run alembic revision --autogenerate -m "descrição da migration"

# Aplicar migrations
make upgrade
# ou
uv run alembic upgrade head

# Reverter última migration
make downgrade
# ou
uv run alembic downgrade -1

# Ver status atual
uv run alembic current

# Ver histórico de migrations
uv run alembic history
```

#### Scripts SQL Alternativos

Se as migrations do Alembic não funcionarem, você pode usar os scripts SQL na pasta `scripts/`:

```bash
# Criar todas as tabelas via SQL
./scripts/apply-all-tables.sh

# Criar apenas a tabela users via SQL
./scripts/apply-sql-migration.sh

# Aplicar migrations do Alembic (script wrapper)
./scripts/apply-migrations.sh
```

#### Fluxo de Trabalho com Migrations

1. **Fazer alterações nos models** em `app/infrastructure/database/models.py`

2. **Gerar migration:**
   ```bash
   make migrate msg="adiciona campo novo"
   ```

3. **Revisar o arquivo gerado** em `alembic/versions/` e ajustar se necessário

4. **Aplicar a migration:**
   ```bash
   make upgrade
   ```

5. **Verificar se funcionou:**
   ```bash
   psql -h localhost -U scrapping_user -d scrapping_db -c "\d nome_da_tabela"
   ```

#### Sincronizar Alembic Após Criar Tabelas Manualmente

Se você criou tabelas manualmente via SQL e quer sincronizar o Alembic:

```bash
# Marca a migration como aplicada sem executá-la
uv run alembic stamp head

# Ou marca uma migration específica
uv run alembic stamp <revision_id>
```

### Importar Dados

```bash
# Importar arquivo JSON
uv run python scripts/import_json.py path/to/file.json
```

## Convenções de Código

### Nomenclatura

- **Classes:** PascalCase (`PublicationService`)
- **Funções/Métodos:** snake_case (`get_publication`)
- **Variáveis:** snake_case (`publication_id`)
- **Constantes:** UPPER_SNAKE_CASE (`MAX_LIMIT`)
- **Arquivos:** snake_case (`publication_service.py`)

### Type Hints

Sempre use type hints:

```python
async def get_publication(
    publication_id: int,
    db: AsyncSession = Depends(get_db),
) -> Optional[PublicationModel]:
    ...
```

### Docstrings

Use docstrings no formato Google:

```python
def analyze_sentiment(text: str) -> Sentiment:
    """Analisa o sentimento de um texto.
    
    Args:
        text: Texto a ser analisado
        
    Returns:
        Sentiment: Sentimento detectado (Positivo, Negativo ou Neutro)
    """
    ...
```

### Imports

Organize imports nesta ordem:
1. Standard library
2. Third-party
3. Local application

```python
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.publication import Publication
from app.application.services.publication_service import PublicationService
```

## Padrões de Desenvolvimento

### Adicionar Nova Rota

1. Crie o schema Pydantic em `app/api/v1/schemas/`
2. Crie a rota em `app/api/v1/routes/`
3. Use o service correspondente
4. Adicione a rota em `app/main.py`

Exemplo:

```python
# app/api/v1/routes/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.application.services.example_service import ExampleService

router = APIRouter()

@router.get("/example")
async def get_example(db: AsyncSession = Depends(get_db)):
    service = ExampleService(db)
    return await service.get_example()
```

### Adicionar Novo Service

1. Crie o service em `app/application/services/`
2. Use o repository correspondente
3. Mantenha a lógica de negócio no service

Exemplo:

```python
# app/application/services/example_service.py
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repositories.example_repository import ExampleRepository

class ExampleService:
    def __init__(self, session: AsyncSession):
        self.repository = ExampleRepository(session)
    
    async def get_example(self):
        return await self.repository.get_all()
```

### Adicionar Nova Migration

1. **Faça alterações nos models** em `app/infrastructure/database/models.py`

2. **Gere a migration:**
   ```bash
   make migrate msg="adiciona campo novo"
   # ou
   uv run alembic revision --autogenerate -m "adiciona campo novo"
   ```

3. **Revise o arquivo gerado** em `alembic/versions/` e ajuste se necessário

4. **Aplique a migration:**
   ```bash
   make upgrade
   # ou
   uv run alembic upgrade head
   ```

5. **Verifique se funcionou:**
   ```bash
   psql -h localhost -U scrapping_user -d scrapping_db -c "\d nome_da_tabela"
   ```

**Nota:** Se a migration gerada estiver vazia (só tem `pass`), você pode precisar preenchê-la manualmente ou usar os scripts SQL alternativos em `scripts/`.

## Testes

### Estrutura de Testes

```
tests/
├── conftest.py          # Fixtures compartilhadas
├── test_publications.py
├── test_services.py
└── test_api.py
```

### Escrevendo Testes

```python
import pytest
from app.application.services.publication_service import PublicationService

@pytest.mark.asyncio
async def test_create_publication(db_session):
    service = PublicationService(db_session)
    # ... seu teste
```

### Rodar Testes

```bash
# Todos os testes
pytest

# Com verbose
pytest -v

# Com coverage
pytest --cov=app

# Teste específico
pytest tests/test_publications.py::test_create_publication
```

## Debugging

### Logs

O FastAPI usa logging padrão do Python. Configure no código:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Mensagem de info")
logger.error("Mensagem de erro")
```

### Debug Mode

No `.env`:
```env
DEBUG=true
```

Isso ativa:
- SQLAlchemy echo (queries SQL no console)
- Stack traces detalhados
- Validações extras

### VS Code Debugging

Crie `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": false
        }
    ]
}
```

## Performance

### Otimizações de Query

- Use `selectinload` para eager loading
- Adicione índices no banco
- Use paginação para listas grandes
- Implemente cache Redis para queries frequentes

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Seu código aqui

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

## Troubleshooting

### Erro de Conexão com Banco

- Verifique se PostgreSQL está rodando: `pg_isready`
- Confirme a `DATABASE_URL` no `.env`
- Verifique permissões do usuário

### Erro ao Baixar Modelo spaCy

```bash
# Tente com --user
uv run python -m spacy download pt_core_news_sm --user

# Ou instale manualmente
pip install https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-3.7.0/pt_core_news_sm-3.7.0-py3-none-any.whl
```

### Erro de Importação

- Verifique se todas as dependências foram instaladas: `uv sync`
- Confirme que está no diretório correto
- Verifique o `PYTHONPATH`

### Migration não aplica

**Erro: "Target database is not up to date"**
```bash
# Aplique as migrations pendentes primeiro
make upgrade
```

**Erro: "relation does not exist"**
```bash
# Use o script SQL para criar as tabelas
./scripts/apply-all-tables.sh

# Depois sincronize o Alembic
uv run alembic stamp head
```

**Verificar status:**
```bash
# Ver migration atual
uv run alembic current

# Ver histórico
uv run alembic history

# Ver SQL que será executado (sem aplicar)
uv run alembic upgrade head --sql
```

**Forçar aplicação:**
```bash
# Aplicar todas as migrations
uv run alembic upgrade head
```

## Contribuindo

1. Crie uma branch: `git checkout -b feature/nova-feature`
2. Faça suas alterações
3. Execute testes: `pytest`
4. Formate código: `make format`
5. Commit: `git commit -m "feat: adiciona nova feature"`
6. Push: `git push origin feature/nova-feature`
7. Abra um Pull Request

### Commit Messages

Use o padrão Conventional Commits:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Tarefas de manutenção

## Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

