# Arquitetura do Projeto

## Visão Geral

Este projeto implementa uma arquitetura **Clean Architecture** / **Hexagonal Architecture**, organizando o código em camadas bem definidas com responsabilidades claras.

## Estrutura de Camadas

### 1. Domain (Domínio)
**Localização:** `app/domain/`

Camada mais interna, contém as regras de negócio puras, sem dependências externas.

- **Entities** (`entities/`): Entidades de negócio
  - `publication.py`: Entidade de publicação
  - `comment.py`: Entidade de comentário
  - `analysis.py`: Entidade de análise agregada

- **Value Objects** (`value_objects/`): Objetos de valor imutáveis
  - `sentiment.py`: Sentimento (Positivo, Negativo, Neutro)
  - `emotion.py`: Emoção (Alegria, Raiva, Frustração, Ansiedade)
  - `topic.py`: Tópico (Ameaças, Rivalidade, Segurança, etc.)

### 2. Application (Aplicação)
**Localização:** `app/application/`

Contém a lógica de aplicação e casos de uso.

- **Services** (`services/`):
  - `publication_service.py`: Gerenciamento de publicações
  - `nlp_service.py`: Processamento de NLP (sentimento, emoção, tópico)
  - `analysis_service.py`: Agregação e análise de dados

### 3. Infrastructure (Infraestrutura)
**Localização:** `app/infrastructure/`

Implementações técnicas e detalhes de frameworks.

- **Database** (`database/`):
  - `models.py`: Models SQLAlchemy
  - `session.py`: Configuração de sessão
  - `repositories/`: Implementação do padrão Repository
    - `publication_repository.py`: Acesso a dados de publicações

- **NLP** (`nlp/`):
  - `sentiment_analyzer.py`: Análise de sentimento
  - `emotion_classifier.py`: Classificação de emoções
  - `topic_classifier.py`: Classificação de tópicos

- **Cache** (`cache/`):
  - `redis_client.py`: Cliente Redis para cache

### 4. API (Apresentação)
**Localização:** `app/api/`

Camada de apresentação, endpoints REST.

- **Routes** (`v1/routes/`):
  - `publications.py`: CRUD de publicações
  - `dashboard.py`: Estatísticas do dashboard
  - `analysis.py`: Endpoints de análise
  - `auth.py`: Autenticação (placeholder)

- **Schemas** (`v1/schemas/`):
  - `publication_schemas.py`: Schemas Pydantic para publicações
  - `dashboard_schemas.py`: Schemas para dashboard

## Fluxo de Dados

```
Frontend (Vue.js)
    ↓ HTTP Request
API Layer (FastAPI Routes)
    ↓
Application Services
    ↓
Domain Entities/Value Objects
    ↓
Infrastructure (Repositories → Database)
```

## Padrões de Projeto Utilizados

1. **Repository Pattern**: Abstração de acesso a dados
2. **Service Layer**: Lógica de negócio isolada
3. **DTO Pattern**: Pydantic schemas para entrada/saída
4. **Dependency Injection**: Via FastAPI Depends

## Princípios Aplicados

- **SOLID**: Especialmente Single Responsibility e Dependency Inversion
- **DRY**: Reutilização de código via services
- **Separation of Concerns**: Cada camada tem responsabilidade única
- **Clean Code**: Código legível e manutenível

## Tecnologias

- **FastAPI**: Framework web assíncrono
- **SQLAlchemy 2.0**: ORM assíncrono
- **PostgreSQL**: Banco de dados
- **Redis**: Cache
- **Pydantic**: Validação de dados
- **Alembic**: Migrations

## Próximos Passos

1. Implementar autenticação JWT completa
2. Adicionar testes unitários e de integração
3. Implementar cache Redis nas queries frequentes
4. Adicionar background tasks com Celery para processamento assíncrono
5. Melhorar NLP com modelos de ML mais sofisticados

