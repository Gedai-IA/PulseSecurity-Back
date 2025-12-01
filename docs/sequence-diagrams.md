# Diagramas de Sequência

Este documento apresenta os fluxos principais da API através de diagramas de sequência.

---

## 1. Fluxo de Criação de Publicação

### 1.1. Criar Publicação via API

```mermaid
sequenceDiagram
    actor Client as Cliente (Frontend/API)
    participant API as FastAPI Router
    participant Service as Publication Service
    participant NLP as NLP Service
    participant Repo as Publication Repository
    participant DB as PostgreSQL

    Client->>API: POST /api/v1/publications
    Note over Client,API: {publicacao_n, url, description,<br/>date, comments, ...}

    API->>API: Valida schema (Pydantic)
    
    API->>Service: create_publication(publication)
    
    Service->>Repo: get_by_publicacao_n(n)
    Repo->>DB: SELECT * FROM publications WHERE publicacao_n = n
    DB-->>Repo: Resultado
    Repo-->>Service: Publication ou None
    
    alt Publicação já existe
        Service-->>API: Retorna existente
        API-->>Client: 200 OK (publicação existente)
    else Nova publicação
        Service->>Repo: create(publication)
        Repo->>DB: BEGIN TRANSACTION
        Repo->>DB: INSERT INTO publications
        Repo->>DB: INSERT INTO comments
        Repo->>DB: INSERT INTO replies
        Repo->>DB: COMMIT
        DB-->>Repo: Confirmação
        Repo-->>Service: PublicationModel
        Service-->>API: PublicationModel
        API-->>Client: 201 Created
    end
```

### 1.2. Importar Publicações de JSON

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Script as import_json.py
    participant Service as Publication Service
    participant Repo as Publication Repository
    participant DB as PostgreSQL

    User->>Script: python scripts/import_json.py file.json
    Script->>Script: Carrega JSON
    Script->>Script: Parse dados
    
    loop Para cada publicação no JSON
        Script->>Script: Converte para Publication entity
        Script->>Service: create_publication(publication)
        Service->>Repo: create(publication)
        Repo->>DB: INSERT (com transação)
        DB-->>Repo: Confirmação
        Repo-->>Service: PublicationModel
        Service-->>Script: Sucesso
    end
    
    Script->>Script: Commit final
    Script-->>User: Importação concluída
```

---

## 2. Fluxo de Listagem e Filtros

### 2.1. Listar Publicações com Filtros

```mermaid
sequenceDiagram
    actor Client as Cliente
    participant API as FastAPI Router
    participant Service as Publication Service
    participant Repo as Publication Repository
    participant DB as PostgreSQL

    Client->>API: GET /api/v1/publications?start_date=...&end_date=...&tags=...
    
    API->>API: Parse query parameters
    API->>Service: list_publications(start_date, end_date, tags, limit, offset)
    
    Service->>Repo: list(start_date, end_date, tags, limit, offset)
    Repo->>DB: SELECT * FROM publications<br/>WHERE date >= start_date<br/>AND date <= end_date<br/>AND tags @> ARRAY[tags]<br/>ORDER BY date DESC<br/>LIMIT limit OFFSET offset
    DB-->>Repo: Resultados
    Repo->>Repo: Carrega relacionamentos (comments, replies)
    Repo-->>Service: List[PublicationModel]
    
    Service->>Service: count_publications(filters)
    Service->>Repo: count(start_date, end_date, tags)
    Repo->>DB: SELECT COUNT(*) FROM publications WHERE ...
    DB-->>Repo: Total
    Repo-->>Service: Total
    
    Service-->>API: {items, total, limit, offset}
    API-->>Client: 200 OK (JSON)
```

### 2.2. Buscar Publicações por Texto

```mermaid
sequenceDiagram
    actor Client as Cliente
    participant API as FastAPI Router
    participant Service as Publication Service
    participant Repo as Publication Repository
    participant DB as PostgreSQL

    Client->>API: GET /api/v1/publications/search?q=violência
    
    API->>Service: search_publications(query="violência", limit=100)
    
    Service->>Repo: search(query="violência", limit=100)
    Repo->>DB: SELECT * FROM publications<br/>WHERE description ILIKE '%violência%'<br/>OR publicacao_n::text ILIKE '%violência%'<br/>LIMIT 100
    DB-->>Repo: Resultados
    Repo->>Repo: Carrega relacionamentos
    Repo-->>Service: List[PublicationModel]
    
    Service-->>API: List[PublicationModel]
    API-->>Client: 200 OK (JSON)
```

---

## 3. Fluxo de Análise NLP

### 3.1. Análise de Sentimento, Emoção e Tópico

```mermaid
sequenceDiagram
    participant Service as NLP Service
    participant Sentiment as Sentiment Analyzer
    participant Emotion as Emotion Classifier
    participant Topic as Topic Classifier
    participant Domain as Domain Entities

    Service->>Service: analyze_publication(publication)
    
    Note over Service: Analisa descrição
    Service->>Sentiment: analyze(description)
    Sentiment->>Sentiment: Verifica keywords
    Sentiment-->>Service: Sentiment (Positivo/Negativo/Neutro)
    
    Service->>Emotion: classify(description)
    Emotion->>Emotion: Verifica keywords
    Emotion-->>Service: Emotion (Alegria/Raiva/...)
    
    Service->>Topic: classify(description)
    Topic->>Topic: Verifica keywords
    Topic-->>Service: Topic (Ameaças/Rivalidade/...)
    
    loop Para cada comentário
        Service->>Service: analyze_comment(comment)
        Service->>Sentiment: analyze(comment.text)
        Service->>Emotion: classify(comment.text)
        Service->>Topic: classify(comment.text)
        
        loop Para cada resposta
            Service->>Service: analyze_comment(reply)
            Service->>Sentiment: analyze(reply.text)
            Service->>Emotion: classify(reply.text)
            Service->>Topic: classify(reply.text)
        end
    end
    
    Service->>Service: Agrega resultados
    Service->>Service: Determina sentimento/emoção/tópico principal
    Service->>Domain: Cria AnalyzedPublication
    Service-->>Service: AnalyzedPublication
```

---

## 4. Fluxo de Dashboard e Estatísticas

### 4.1. Obter Estatísticas do Dashboard

```mermaid
sequenceDiagram
    actor Client as Cliente
    participant API as FastAPI Router
    participant Service as Analysis Service
    participant PubService as Publication Service
    participant NLPService as NLP Service
    participant Repo as Publication Repository
    participant DB as PostgreSQL

    Client->>API: GET /api/v1/dashboard/stats?start_date=...&end_date=...&tags=...
    
    API->>Service: get_dashboard_stats(start_date, end_date, tags)
    
    Service->>PubService: list_publications(filters, limit=10000)
    PubService->>Repo: list(filters, limit=10000)
    Repo->>DB: SELECT * FROM publications WHERE ...
    DB-->>Repo: Todas as publicações
    Repo-->>PubService: List[PublicationModel]
    PubService-->>Service: List[PublicationModel]
    
    loop Para cada publicação
        Service->>Service: Converte Model para Entity
        Service->>NLPService: analyze_publication(publication)
        NLPService->>NLPService: Analisa sentimento, emoção, tópico
        NLPService-->>Service: AnalyzedPublication
        
        Service->>Service: Coleta dados agregados
        Note over Service: - Sentimentos<br/>- Emoções<br/>- Tópicos<br/>- Contagem de ameaças<br/>- Contagem de comentários
    end
    
    Service->>Service: Calcula estatísticas finais
    Note over Service: - Total de publicações<br/>- Total de comentários<br/>- Contagem de ameaças<br/>- % Sentimento negativo<br/>- Distribuições
    Service->>Service: Cria DashboardStats
    Service-->>API: DashboardStats
    API->>API: Converte enums para strings
    API-->>Client: 200 OK (JSON)
```

---

## 5. Fluxo de Cache (Futuro)

### 5.1. Consulta com Cache Redis

```mermaid
sequenceDiagram
    actor Client as Cliente
    participant API as FastAPI Router
    participant Service as Service Layer
    participant Cache as Redis Cache
    participant Repo as Repository
    participant DB as PostgreSQL

    Client->>API: GET /api/v1/dashboard/stats
    
    API->>Service: get_dashboard_stats()
    
    Service->>Cache: get("dashboard:stats:2024-01-01:2024-01-31")
    
    alt Cache Hit
        Cache-->>Service: Dados do cache
        Service-->>API: DashboardStats (do cache)
        API-->>Client: 200 OK
    else Cache Miss
        Cache-->>Service: None
        
        Service->>Repo: list_publications(...)
        Repo->>DB: SELECT ...
        DB-->>Repo: Dados
        Repo-->>Service: List[PublicationModel]
        
        Service->>Service: Processa e agrega
        Service->>Service: Cria DashboardStats
        
        Service->>Cache: set("dashboard:stats:...", stats, expire=3600)
        Cache-->>Service: OK
        
        Service-->>API: DashboardStats
        API-->>Client: 200 OK
    end
```

---

## 6. Fluxo de Autenticação (Futuro)

### 6.1. Login e Geração de Token

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Frontend as Frontend
    participant API as FastAPI Router
    participant Auth as Auth Service
    participant Security as Security Module
    participant DB as PostgreSQL

    User->>Frontend: Insere email e senha
    Frontend->>API: POST /api/v1/auth/login
    Note over Frontend,API: {email, password}

    API->>Auth: login(email, password)
    
    Auth->>DB: SELECT * FROM users WHERE email = email
    DB-->>Auth: User data
    
    Auth->>Security: verify_password(plain, hashed)
    Security-->>Auth: Boolean
    
    alt Senha válida
        Auth->>Security: create_access_token({user_id, email, tipo})
        Security->>Security: Gera JWT
        Security-->>Auth: JWT token
        
        Auth-->>API: {access_token, user}
        API-->>Frontend: 200 OK
        Frontend->>Frontend: Armazena token
        Frontend-->>User: Redireciona para dashboard
    else Senha inválida
        Auth-->>API: Erro
        API-->>Frontend: 401 Unauthorized
        Frontend-->>User: Credenciais inválidas
    end
```

### 6.2. Requisição Autenticada

```mermaid
sequenceDiagram
    actor Client as Cliente
    participant API as FastAPI Router
    participant Middleware as Auth Middleware
    participant Security as Security Module
    participant Service as Service Layer

    Client->>API: GET /api/v1/publications<br/>Authorization: Bearer {token}
    
    API->>Middleware: Valida token
    
    Middleware->>Security: decode_access_token(token)
    Security->>Security: Verifica assinatura e expiração
    Security-->>Middleware: Payload ou None
    
    alt Token válido
        Middleware->>Middleware: Extrai user_id do payload
        Middleware->>API: Continua requisição (user_id no contexto)
        API->>Service: list_publications(...)
        Service-->>API: Dados
        API-->>Client: 200 OK
    else Token inválido/expirado
        Middleware-->>API: Erro de autenticação
        API-->>Client: 401 Unauthorized
    end
```

---

## 7. Fluxo de Análise de Segurança Pública com Drones

### 7.1. Análise de Stream de Drone em Tempo Real

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Frontend as Frontend
    participant API as FastAPI Router
    participant DetectionService as Detection Service
    participant YOLO as YOLO Detector
    participant Camera as Camera/Drone Feed
    participant DB as PostgreSQL

    User->>Frontend: Acessa "Análise de Drones"
    Frontend->>API: GET /api/v1/detections/streams
    Note over Frontend,API: Authorization: Bearer {token}
    
    API->>DetectionService: list_active_streams()
    DetectionService->>DB: SELECT * FROM drone_streams WHERE active = true
    DB-->>DetectionService: List[DroneStream]
    DetectionService-->>API: List[DroneStream]
    API-->>Frontend: 200 OK {streams}
    
    Frontend-->>User: Lista de streams disponíveis
    
    User->>Frontend: Seleciona stream de drone
    Frontend->>API: POST /api/v1/detections/streams/{id}/start
    Note over Frontend,API: Authorization: Bearer {token}
    
    API->>DetectionService: start_detection_stream(stream_id)
    DetectionService->>Camera: connect_to_stream(stream_url)
    Camera-->>DetectionService: Stream connection established
    
    DetectionService->>DetectionService: Inicia thread de processamento
    
    loop Para cada frame do stream
        Camera->>DetectionService: Frame (imagem)
        DetectionService->>YOLO: detect_objects(frame)
        YOLO->>YOLO: Processa com modelo YOLO
        YOLO-->>DetectionService: Detections {boxes, classes, confidences}
        
        alt Objetos detectados (armas)
            DetectionService->>DetectionService: process_detections(detections)
            DetectionService->>DB: INSERT INTO detections
            Note over DetectionService,DB: {stream_id, timestamp,<br/>objects_detected,<br/>location, confidence}
            DB-->>DetectionService: Detection ID
            
            DetectionService->>API: WebSocket: send_alert(detection)
            API->>Frontend: WebSocket: alert {detection}
            Frontend->>Frontend: Exibe alerta em tempo real
            Frontend-->>User: Alerta visual + notificação
        end
        
        DetectionService->>API: WebSocket: send_frame(frame_with_detections)
        API->>Frontend: WebSocket: frame {image, detections}
        Frontend->>Frontend: Atualiza visualização
        Frontend-->>User: Frame com bounding boxes
    end
```

### 7.2. Upload e Análise de Imagem de Drone

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Frontend as Frontend
    participant API as FastAPI Router
    participant DetectionService as Detection Service
    participant YOLO as YOLO Detector
    participant Storage as File Storage
    participant DB as PostgreSQL

    User->>Frontend: Faz upload de imagem de drone
    Frontend->>Frontend: Valida arquivo (tipo, tamanho)
    Frontend->>API: POST /api/v1/detections/analyze
    Note over Frontend,API: Authorization: Bearer {token}<br/>Content-Type: multipart/form-data<br/>file: image.jpg<br/>location: {lat, lng}
    
    API->>API: Valida arquivo e metadados
    API->>Storage: save_uploaded_file(file)
    Storage-->>API: file_path
    
    API->>DetectionService: analyze_image(file_path, location)
    DetectionService->>YOLO: detect_objects(image_path)
    YOLO->>YOLO: Carrega modelo YOLO
    YOLO->>YOLO: Processa imagem
    YOLO-->>DetectionService: Detections {boxes, classes, confidences, names}
    
    DetectionService->>DetectionService: process_detections(detections)
    DetectionService->>DetectionService: generate_annotated_image(image, detections)
    DetectionService->>Storage: save_annotated_image(annotated_image)
    Storage-->>DetectionService: annotated_image_path
    
    DetectionService->>DB: INSERT INTO detections
    Note over DetectionService,DB: {image_path, annotated_path,<br/>location, timestamp,<br/>objects_detected, metadata}
    DB-->>DetectionService: Detection ID
    
    DetectionService-->>API: DetectionResult
    Note over DetectionService,API: {detection_id, objects_detected,<br/>annotated_image_url,<br/>confidence_scores, location}
    
    API-->>Frontend: 200 OK {result}
    Frontend->>Frontend: Renderiza resultado
    Frontend-->>User: Imagem anotada + estatísticas
    Note over User: Visualiza:<br/>- Imagem com bounding boxes<br/>- Contagem de objetos detectados<br/>- Níveis de confiança<br/>- Localização no mapa
```

---

## 8. Fluxo de Dashboard Integrado

### 8.1. Dashboard Integrado com Alertas em Tempo Real

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Frontend as Frontend
    participant API as FastAPI Router
    participant DashboardService as Dashboard Service
    participant PubService as Publication Service
    participant DetectionService as Detection Service
    participant DB as PostgreSQL
    participant WS as WebSocket

    User->>Frontend: Acessa dashboard principal
    Frontend->>API: GET /api/v1/dashboard/stats
    Frontend->>WS: connect_websocket()
    
    API->>DashboardService: get_dashboard_stats()
    
    par Análise de Redes Sociais
        DashboardService->>PubService: get_publication_stats()
        PubService->>DB: SELECT COUNT(*), sentiment, emotion, topic<br/>FROM publications<br/>WHERE date > NOW() - INTERVAL '24 hours'<br/>GROUP BY sentiment, emotion, topic
        DB-->>PubService: Aggregated stats
        PubService-->>DashboardService: SocialMediaStats
    and Análise de Drones
        DashboardService->>DetectionService: get_detection_stats()
        DetectionService->>DB: SELECT COUNT(*), class, confidence<br/>FROM detections<br/>WHERE timestamp > NOW() - INTERVAL '24 hours'<br/>GROUP BY class
        DB-->>DetectionService: Aggregated stats
        DetectionService-->>DashboardService: DetectionStats
    end
    
    DashboardService->>DashboardService: merge_stats(social_stats, detection_stats)
    DashboardService->>DashboardService: calculate_risk_indicators()
    DashboardService-->>API: IntegratedDashboardStats
    
    API-->>Frontend: 200 OK {stats}
    Frontend->>Frontend: Renderiza dashboard
    
    loop WebSocket: Alertas em Tempo Real
        DetectionService->>WS: send_alert(detection)
        WS->>Frontend: {type: "detection_alert", data: {...}}
        Frontend->>Frontend: Exibe notificação
        Frontend->>Frontend: Atualiza contadores
        Frontend-->>User: Alerta visual + som
    end
```

### 8.2. Visualização Integrada no Mapa

```mermaid
sequenceDiagram
    actor User as Usuário
    participant Frontend as Frontend
    participant API as FastAPI Router
    participant AnalysisService as Analysis Service
    participant DB as PostgreSQL

    User->>Frontend: Acessa "Mapa de Eventos"
    Frontend->>API: GET /api/v1/map/events?bounds={north,south,east,west}
    Note over Frontend,API: Authorization: Bearer {token}
    
    API->>AnalysisService: get_map_events(bounds, filters)
    
    AnalysisService->>DB: SELECT * FROM detections<br/>WHERE location && bounds<br/>AND timestamp > NOW() - INTERVAL '24 hours'
    DB-->>AnalysisService: List[Detection]
    
    AnalysisService->>DB: SELECT * FROM publications<br/>WHERE has_location = true<br/>AND location && bounds<br/>AND date > NOW() - INTERVAL '24 hours'
    DB-->>AnalysisService: List[Publication]
    
    AnalysisService->>AnalysisService: aggregate_events(detections, publications)
    AnalysisService->>AnalysisService: calculate_risk_levels()
    AnalysisService-->>API: MapEvents {events, risk_zones}
    
    API-->>Frontend: 200 OK {events, risk_zones}
    
    Frontend->>Frontend: Renderiza mapa
    Frontend->>Frontend: Adiciona marcadores de eventos
    Frontend->>Frontend: Desenha zonas de risco
    Frontend-->>User: Mapa interativo
    Note over User: Visualiza:<br/>- Marcadores de detecções de drones<br/>- Marcadores de publicações relevantes<br/>- Zonas de risco calculadas<br/>- Heatmap de atividade
```

---

## Notas Técnicas

### Validação de Dados
- Todas as requisições são validadas por schemas Pydantic
- Erros de validação retornam 422 Unprocessable Entity

### Tratamento de Erros
- Exceções customizadas (NotFoundError, ValidationError, etc.)
- Logging de erros para debugging
- Mensagens de erro amigáveis para o cliente

### Performance
- Queries otimizadas com índices
- Eager loading de relacionamentos (selectinload)
- Cache Redis para queries frequentes (futuro)
- Paginação para listas grandes

### Transações
- Operações de escrita usam transações
- Rollback automático em caso de erro
- Commit explícito após sucesso

