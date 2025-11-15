# Pasta JSON

Esta pasta contém os arquivos JSON com os dados das publicações que serão importados para o banco de dados através das migrations do Alembic.

## Estrutura Esperada

Os arquivos JSON devem seguir o formato:

```json
[
  {
    "publicacao_n": 1,
    "url": "https://...",
    "views": "42.6K",
    "likes": "3864",
    "comments_count": 0,
    "shares": "38",
    "bookmarks": "277",
    "description": "...",
    "musicTitle": "...",
    "date": "2024-4-23",
    "tags": ["#tag1", "#tag2"],
    "comments": [
      {
        "username": "user",
        "text": "comment text",
        "likes": "10",
        "replies": [
          {
            "username": "user2",
            "text": "reply text",
            "likes": "5"
          }
        ]
      }
    ]
  }
]
```

## Como Funciona

Quando você executa `alembic upgrade head`, a migration `populate_json_data` irá:

1. Ler todos os arquivos `*.json` desta pasta
2. Processar os dados em memória (sem armazenar em arquivos intermediários)
3. Inserir os dados diretamente no banco de dados

## Importante

- Os dados são processados **diretamente** durante a migration, sem armazenamento intermediário
- A migration remove duplicatas automaticamente (mantendo a publicação com mais comentários)
- Comentários com username/text "N/A" são ignorados
- O caminho é relativo ao projeto, tornando o código portável entre diferentes máquinas

## Segurança

⚠️ **Nota sobre dados sensíveis**: Se os arquivos JSON contêm dados sensíveis, considere:
- Adicionar `json/` ao `.gitignore` para não versionar os dados
- Usar variáveis de ambiente ou secrets para caminhos alternativos
- Processar os dados em um ambiente seguro antes de fazer commit

