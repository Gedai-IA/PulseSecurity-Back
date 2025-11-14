# Documentação da API

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticação

> **Nota:** Autenticação será implementada em versão futura. Por enquanto, os endpoints estão abertos.

Futuramente, as requisições autenticadas devem incluir o header:

```
Authorization: Bearer {token}
```

## Endpoints

### Publicações

#### Criar Publicação

```http
POST /publications
Content-Type: application/json
```

**Request Body:**

```json
{
  "publicacao_n": 1,
  "url": "https://example.com/post/1",
  "description": "Descrição da publicação",
  "date": "2024-01-15T10:00:00",
  "views": "10.5K",
  "likes": "1.2K",
  "comments_count": 50,
  "shares": "500",
  "bookmarks": "100",
  "music_title": "Música de fundo",
  "tags": ["#tag1", "#tag2"],
  "comments": [
    {
      "username": "user1",
      "text": "Comentário exemplo",
      "likes": 10,
      "replies": [
        {
          "username": "user2",
          "text": "Resposta exemplo",
          "likes": 5
        }
      ]
    }
  ]
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "publicacao_n": 1,
  "url": "https://example.com/post/1",
  "description": "Descrição da publicação",
  "date": "2024-01-15T10:00:00",
  "views": "10.5K",
  "likes": "1.2K",
  "comments_count": 50,
  "shares": "500",
  "bookmarks": "100",
  "music_title": "Música de fundo",
  "tags": ["#tag1", "#tag2"],
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

#### Listar Publicações

```http
GET /publications?start_date=2024-01-01&end_date=2024-01-31&tags=tag1&limit=100&offset=0
```

**Query Parameters:**

| Parâmetro | Tipo | Descrição | Obrigatório |
|-----------|------|-----------|-------------|
| `start_date` | datetime | Data inicial (ISO format) | Não |
| `end_date` | datetime | Data final (ISO format) | Não |
| `tags` | array[string] | Lista de tags para filtrar | Não |
| `limit` | integer | Número máximo de resultados (1-1000) | Não (padrão: 100) |
| `offset` | integer | Número de resultados para pular | Não (padrão: 0) |

**Response:** `200 OK`

```json
{
  "items": [
    {
      "id": 1,
      "publicacao_n": 1,
      "url": "https://example.com/post/1",
      "description": "Descrição",
      "date": "2024-01-15T10:00:00",
      ...
    }
  ],
  "total": 150,
  "limit": 100,
  "offset": 0
}
```

#### Obter Publicação por ID

```http
GET /publications/{id}
```

**Path Parameters:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | integer | ID da publicação |

**Response:** `200 OK`

```json
{
  "id": 1,
  "publicacao_n": 1,
  "url": "https://example.com/post/1",
  "description": "Descrição da publicação",
  ...
}
```

**Erros:**

- `404 Not Found`: Publicação não encontrada

#### Buscar Publicações

```http
GET /publications/search?q=violência&limit=100
```

**Query Parameters:**

| Parâmetro | Tipo | Descrição | Obrigatório |
|-----------|------|-----------|-------------|
| `q` | string | Termo de busca (mínimo 1 caractere) | Sim |
| `limit` | integer | Número máximo de resultados (1-1000) | Não (padrão: 100) |

**Response:** `200 OK`

```json
{
  "items": [...],
  "total": 25,
  "limit": 100,
  "offset": 0
}
```

### Dashboard

#### Obter Estatísticas

```http
GET /dashboard/stats?start_date=2024-01-01&end_date=2024-01-31&tags=tag1
```

**Query Parameters:**

| Parâmetro | Tipo | Descrição | Obrigatório |
|-----------|------|-----------|-------------|
| `start_date` | datetime | Data inicial (ISO format) | Não |
| `end_date` | datetime | Data final (ISO format) | Não |
| `tags` | array[string] | Lista de tags para filtrar | Não |

**Response:** `200 OK`

```json
{
  "total_publications": 150,
  "total_comments": 5000,
  "threat_count": 25,
  "negative_sentiment_percent": 35.5,
  "sentiment_distribution": {
    "Positivo": 2000,
    "Negativo": 2500,
    "Neutro": 500
  },
  "emotion_distribution": {
    "Alegria": 1500,
    "Raiva": 2000,
    "Frustração": 800,
    "Ansiedade": 700,
    "Geral": 0
  },
  "topic_distribution": {
    "Ameaças e Riscos": 25,
    "Rivalidade Esportiva": 50,
    "Segurança (Policial)": 30,
    "Apoio e União": 40,
    "Organização e Eventos": 35,
    "Política e Gestão": 20,
    "Geral": 0
  },
  "date_range": [
    "2024-01-01T00:00:00",
    "2024-01-31T23:59:59"
  ]
}
```

### Análise

#### Health Check

```http
GET /analysis/health
```

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "service": "analysis"
}
```

### Autenticação (Placeholder)

#### Login

```http
POST /auth/login
Content-Type: application/json
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "senha123"
}
```

**Response:** `200 OK` (futuro)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nome": "Usuário"
  }
}
```

#### Registro

```http
POST /auth/register
Content-Type: application/json
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "senha123",
  "nome": "Usuário",
  "tipo": "medico"
}
```

**Response:** `201 Created` (futuro)

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| `200` | OK - Requisição bem-sucedida |
| `201` | Created - Recurso criado com sucesso |
| `400` | Bad Request - Requisição inválida |
| `401` | Unauthorized - Não autenticado |
| `403` | Forbidden - Sem permissão |
| `404` | Not Found - Recurso não encontrado |
| `422` | Unprocessable Entity - Erro de validação |
| `500` | Internal Server Error - Erro no servidor |

## Tratamento de Erros

### Formato de Erro

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Exemplos

**404 Not Found:**

```json
{
  "detail": "Publicação 123 não encontrada"
}
```

**422 Validation Error:**

```json
{
  "detail": [
    {
      "loc": ["body", "publicacao_n"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

> **Nota:** Rate limiting será implementado em versão futura.

## Paginação

Endpoints que retornam listas suportam paginação via query parameters:

- `limit`: Número de itens por página (padrão: 100, máximo: 1000)
- `offset`: Número de itens para pular (padrão: 0)

**Exemplo:**

```http
GET /publications?limit=50&offset=100
```

Retorna itens 101-150.

## Filtros

### Filtro por Data

Use `start_date` e `end_date` para filtrar por intervalo:

```http
GET /publications?start_date=2024-01-01T00:00:00&end_date=2024-01-31T23:59:59
```

### Filtro por Tags

Use `tags` para filtrar por uma ou mais tags:

```http
GET /publications?tags=tag1&tags=tag2
```

## Documentação Interativa

Acesse a documentação interativa:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Exemplos de Uso

### cURL

```bash
# Listar publicações
curl http://localhost:8000/api/v1/publications

# Criar publicação
curl -X POST http://localhost:8000/api/v1/publications \
  -H "Content-Type: application/json" \
  -d '{
    "publicacao_n": 1,
    "url": "https://example.com/post/1",
    "description": "Descrição",
    "date": "2024-01-15T10:00:00"
  }'

# Obter estatísticas
curl "http://localhost:8000/api/v1/dashboard/stats?start_date=2024-01-01&end_date=2024-01-31"
```

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    # Listar publicações
    response = await client.get("http://localhost:8000/api/v1/publications")
    data = response.json()
    
    # Criar publicação
    publication = {
        "publicacao_n": 1,
        "url": "https://example.com/post/1",
        "description": "Descrição",
        "date": "2024-01-15T10:00:00"
    }
    response = await client.post(
        "http://localhost:8000/api/v1/publications",
        json=publication
    )
```

### JavaScript/TypeScript

```typescript
// Listar publicações
const response = await fetch('http://localhost:8000/api/v1/publications');
const data = await response.json();

// Criar publicação
const publication = {
  publicacao_n: 1,
  url: 'https://example.com/post/1',
  description: 'Descrição',
  date: '2024-01-15T10:00:00'
};

const response = await fetch('http://localhost:8000/api/v1/publications', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(publication)
});
```

