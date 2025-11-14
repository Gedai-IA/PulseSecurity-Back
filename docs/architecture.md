# Arquitetura do Sistema

## Visão Geral

Este documento descreve a arquitetura do backend de análise de sentimento e tópicos em publicações de redes sociais, implementada seguindo os princípios de **Clean Architecture** e **Hexagonal Architecture**.

## Diagrama de Arquitetura

```mermaid
graph TB
    subgraph Frontend["Camada de Apresentação"]
        FE[<strong>Frontend Vue.js</strong><br/>- Dashboard<br/>- Análise de Sentimento<br/>- Visualizações<br/>- Filtros e Busca]
    end

    subgraph API["Camada API - FastAPI"]
        API_GW[API Gateway<br/>FastAPI]
        
        AUTH[Auth Middleware<br/>JWT Validation]
        
        ROUTE[Router<br/>Direcionamento]
        
        CORS[CORS Middleware]
        
        API_GW --> CORS
        CORS --> AUTH
        AUTH --> ROUTE
    end

    subgraph Application["Camada de Aplicação"]
        direction LR
        PUB_SVC[Publication Service<br/>Gerenciamento de Publicações]
        NLP_SVC[NLP Service<br/>Análise de Sentimento<br/>Classificação de Emoções<br/>Classificação de Tópicos]
        ANALYSIS_SVC[Analysis Service<br/>Agregação de Dados<br/>Estatísticas do Dashboard]
    end

    subgraph Domain["Camada de Domínio"]
        direction TB
        ENTITIES[Entities<br/>Publication<br/>Comment<br/>Analysis]
        VO[Value Objects<br/>Sentiment<br/>Emotion<br/>Topic]
    end

    subgraph Infrastructure["Camada de Infraestrutura"]
        direction LR
        REPO[Repository Pattern<br/>Publication Repository]
        NLP_IMPL[NLP Implementations<br/>Sentiment Analyzer<br/>Emotion Classifier<br/>Topic Classifier]
        CACHE_CLIENT[Redis Client<br/>Cache Layer]
    end

    subgraph Data["Camada de Dados"]
        DB[(PostgreSQL<br/><br/>Publications<br/>Comments<br/>Replies<br/>Analyses)]
        CACHE[(Redis<br/><br/>Cache de Queries<br/>Sessions)]
    end

    subgraph External["Serviços Externos"]
        JSON_FILES[Arquivos JSON<br/>Dados de Scraping]
    end

    %% Conexões Frontend -> API
    FE -->|HTTPS/REST| API_GW

    %% Conexões API -> Application
    ROUTE -->|Dependency Injection| PUB_SVC
    ROUTE -->|Dependency Injection| ANALYSIS_SVC
    PUB_SVC -->|Uses| NLP_SVC
    ANALYSIS_SVC -->|Uses| NLP_SVC
    ANALYSIS_SVC -->|Uses| PUB_SVC

    %% Conexões Application -> Domain
    PUB_SVC -->|Uses| ENTITIES
    NLP_SVC -->|Uses| VO
    NLP_SVC -->|Uses| ENTITIES
    ANALYSIS_SVC -->|Uses| ENTITIES
    ANALYSIS_SVC -->|Uses| VO

    %% Conexões Application -> Infrastructure
    PUB_SVC -->|Uses| REPO
    NLP_SVC -->|Uses| NLP_IMPL
    ANALYSIS_SVC -->|Uses| CACHE_CLIENT

    %% Conexões Infrastructure -> Data
    REPO -->|SQL/Async| DB
    CACHE_CLIENT -->|Redis Protocol| CACHE

    %% Conexões Externas
    JSON_FILES -.->|Import Script| REPO

    %% Estilos
    classDef frontend fill:#42b983,stroke:#333,stroke-width:2px,color:#fff
    classDef api fill:#009688,stroke:#333,stroke-width:2px,color:#fff
    classDef application fill:#ff6b6b,stroke:#333,stroke-width:2px,color:#fff
    classDef domain fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#000
    classDef infrastructure fill:#95a5a6,stroke:#333,stroke-width:2px,color:#fff
    classDef database fill:#3498db,stroke:#333,stroke-width:2px,color:#fff
    classDef external fill:#e67e22,stroke:#333,stroke-width:2px,color:#fff
    classDef middleware fill:#f39c12,stroke:#333,stroke-width:2px,color:#000

    class FE frontend
    class API_GW,ROUTE api
    class AUTH,CORS middleware
    class PUB_SVC,NLP_SVC,ANALYSIS_SVC application
    class ENTITIES,VO domain
    class REPO,NLP_IMPL,CACHE_CLIENT infrastructure
    class DB,CACHE database
    class JSON_FILES external
```

## Camadas da Arquitetura

### 1. Camada de Apresentação (Frontend)
- **Tecnologia:** Vue.js 3 + TypeScript
- **Responsabilidades:**
  - Interface de usuário
  - Visualizações e gráficos (Chart.js)
  - Filtros e buscas
  - Gerenciamento de estado (Pinia)

### 2. Camada API (FastAPI)
- **Tecnologia:** FastAPI
- **Componentes:**
  - **API Gateway:** Ponto de entrada único
  - **CORS Middleware:** Controle de acesso cross-origin
  - **Auth Middleware:** Validação JWT (futuro)
  - **Router:** Direcionamento de requisições
- **Responsabilidades:**
  - Receber requisições HTTP
  - Validação de entrada (Pydantic)
  - Serialização de saída
  - Tratamento de erros

### 3. Camada de Aplicação
- **Services:**
  - **PublicationService:** Gerenciamento de publicações (CRUD)
  - **NLPService:** Orquestração de análises NLP
  - **AnalysisService:** Agregação e estatísticas
- **Responsabilidades:**
  - Lógica de negócio
  - Orquestração de operações
  - Coordenação entre camadas

### 4. Camada de Domínio
- **Entities:**
  - `Publication`: Publicação com comentários
  - `Comment`: Comentário com respostas
  - `AnalyzedPublication`: Publicação analisada
  - `DashboardStats`: Estatísticas agregadas
- **Value Objects:**
  - `Sentiment`: Positivo, Negativo, Neutro
  - `Emotion`: Alegria, Raiva, Frustração, Ansiedade
  - `Topic`: Ameaças, Rivalidade, Segurança, etc.
- **Responsabilidades:**
  - Regras de negócio puras
  - Entidades imutáveis
  - Sem dependências externas

### 5. Camada de Infraestrutura
- **Database:**
  - Repository Pattern
  - SQLAlchemy Models
  - Queries otimizadas
- **NLP:**
  - Classificadores baseados em keywords
  - Extensível para modelos ML
- **Cache:**
  - Cliente Redis
  - Cache de queries frequentes
- **Responsabilidades:**
  - Implementações técnicas
  - Acesso a dados
  - Integrações externas

### 6. Camada de Dados
- **PostgreSQL:**
  - Armazenamento persistente
  - Relacionamentos complexos
  - Índices para performance
- **Redis:**
  - Cache de queries
  - Sessões (futuro)
  - Filas (futuro com Celery)

## Fluxo de Dados

```
Frontend (Vue.js)
    ↓ HTTP Request
API Layer (FastAPI Routes)
    ↓ Dependency Injection
Application Services
    ↓ Uses
Domain Entities/Value Objects
    ↓ Uses
Infrastructure (Repositories)
    ↓ SQL/Async
Database (PostgreSQL)
```

## Princípios Aplicados

### SOLID
- **Single Responsibility:** Cada classe tem uma responsabilidade única
- **Dependency Inversion:** Dependências apontam para abstrações (Domain)

### Clean Architecture
- **Independência de Frameworks:** Domain não depende de FastAPI/SQLAlchemy
- **Testabilidade:** Camadas isoladas facilitam testes
- **Independência de UI:** API pode ser trocada sem afetar Domain
- **Independência de Banco:** Repository Pattern permite trocar banco

### Padrões de Projeto
- **Repository Pattern:** Abstração de acesso a dados
- **Service Layer:** Lógica de negócio isolada
- **DTO Pattern:** Pydantic schemas para entrada/saída
- **Dependency Injection:** Via FastAPI Depends

## Tecnologias

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| API | FastAPI | >=0.115.0 |
| ORM | SQLAlchemy | >=2.0.0 (async) |
| Banco | PostgreSQL | 14+ |
| Cache | Redis | 7+ |
| Validação | Pydantic | >=2.9.0 |
| Migrations | Alembic | >=1.13.0 |
| NLP | spaCy | >=3.7.0 |
| Testes | pytest | >=8.3.0 |

## Escalabilidade

### Horizontal
- API stateless permite múltiplas instâncias
- Load balancer na frente
- Redis compartilhado para cache

### Vertical
- Async/await para I/O não bloqueante
- Connection pooling no PostgreSQL
- Cache Redis para reduzir carga no banco

### Futuro
- Background tasks com Celery
- Message queue (RabbitMQ/Redis)
- Microserviços se necessário

## Segurança

- **Autenticação:** JWT (implementação futura)
- **Autorização:** Middleware de validação
- **CORS:** Configurável por origem
- **Validação:** Pydantic schemas
- **SQL Injection:** Prevenido por ORM
- **XSS:** Sanitização de entrada

## Monitoramento (Futuro)

- Logging estruturado
- Métricas (Prometheus)
- Tracing distribuído
- Health checks
- Alertas

