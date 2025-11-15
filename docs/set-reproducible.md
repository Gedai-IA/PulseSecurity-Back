# Guia de Reprodução do Projeto

Este documento explica o fluxo completo para reproduzir o projeto em outro computador.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+**
- **uv** (gerenciador de pacotes Python) - [Instalação](https://github.com/astral-sh/uv)
- **PostgreSQL 14+**
- **Redis 7+** (opcional, para cache)

## 🔄 Fluxo Completo de Setup

### 1. Clonar/Obter o Código

```bash
# Se usando Git
git clone <url-do-repositorio>
cd scrapping-backend

# Ou copie a pasta do projeto para o novo computador
```

### 2. Estrutura de Arquivos Necessária

O projeto precisa da seguinte estrutura:

```
scrapping-backend/
├── json/                          # ⚠️ IMPORTANTE: Pasta com dados JSON
│   ├── *.json                     # Arquivos JSON com publicações
│   └── README.md
├── alembic/
│   ├── helpers.py                 # Processa JSONs
│   └── versions/
│       ├── create_publications_tables.py
│       └── populate_json_data.py  # Migration que importa dados
├── app/                           # Código da aplicação
├── .env                           # Variáveis de ambiente (criar)
├── pyproject.toml                 # Dependências
└── ...
```

**⚠️ IMPORTANTE:** A pasta `json/` com os arquivos JSON **deve existir** antes de executar as migrations!

### 3. Instalar Dependências

```bash
cd scrapping-backend

# Instalar todas as dependências do projeto
uv sync
```

Isso irá:
- Criar um ambiente virtual (`.venv`)
- Instalar todas as dependências listadas em `pyproject.toml`

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar o arquivo .env com suas configurações
nano .env  # ou use seu editor preferido
```

**Configurações mínimas necessárias no `.env`:**

```env
# Banco de Dados
DATABASE_URL=postgresql+asyncpg://scrapping_user:scrapping_password@localhost:5432/scrapping_db

# Segurança
SECRET_KEY=sua-chave-secreta-aqui-gerar-uma-aleatoria

# Opcional: Redis (se usar cache)
REDIS_URL=redis://localhost:6379/0
```

**Gerar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Configurar PostgreSQL

#### Opção A: Script Automático (Recomendado)

```bash
# Na raiz do projeto (gedai/) ou no diretório scrapping-backend
./setup-postgres.sh
```

Este script irá:
- Instalar PostgreSQL (se necessário)
- Criar o banco de dados `scrapping_db`
- Criar o usuário `scrapping_user`
- Configurar permissões

#### Opção B: Manual

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

### 6. Baixar Modelo spaCy (para NLP)

```bash
uv run python -m spacy download pt_core_news_sm
```

### 7. Preparar Dados JSON

**⚠️ CRÍTICO:** Antes de executar as migrations, você precisa:

1. **Criar a pasta `json/`** dentro de `scrapping-backend/`:
   ```bash
   mkdir -p scrapping-backend/json
   ```

2. **Copiar os arquivos JSON** para essa pasta:
   ```bash
   # Exemplo: copiar arquivos JSON para a pasta
   cp /caminho/para/arquivos/*.json scrapping-backend/json/
   ```

3. **Verificar que os arquivos estão lá:**
   ```bash
   ls scrapping-backend/json/
   # Deve mostrar os arquivos .json
   ```

### 8. Executar Migrations

```bash
cd scrapping-backend

# Verificar status atual
uv run alembic current

# Aplicar todas as migrations
uv run alembic upgrade head
```

**O que acontece durante as migrations:**

1. **Migration 1** (`b587c504012b_version_01`): Migration inicial (vazia)
2. **Migration 2** (`9eaec19212fd_add_users_table`): Cria tabela `users`
3. **Migration 3** (`create_pub_tables`): 
   - Cria tabelas: `publications`, `comments`, `replies`, `publication_analyses`, `comment_analyses`
   - Verifica se as tabelas já existem (idempotente)
4. **Migration 4** (`populate_json_data`): 
   - **Lê todos os arquivos `*.json` da pasta `json/`**
   - **Processa os dados em memória** (sem armazenar em arquivos)
   - **Insere no banco de dados:**
     - Publicações
     - Comentários
     - Respostas

**Fluxo de processamento dos JSONs:**

```
json/*.json
    ↓
helpers.py::load_all_publications()
    ↓ (lê arquivos, processa em memória)
    ↓
populate_json_data.py::upgrade()
    ↓ (insere diretamente no banco)
    ↓
PostgreSQL
```

### 9. Verificar se Funcionou

```bash
# Verificar quantas publicações foram inseridas
psql -h localhost -U scrapping_user -d scrapping_db -c "SELECT COUNT(*) FROM publications;"

# Verificar comentários
psql -h localhost -U scrapping_user -d scrapping_db -c "SELECT COUNT(*) FROM comments;"

# Verificar respostas
psql -h localhost -U scrapping_user -d scrapping_db -c "SELECT COUNT(*) FROM replies;"
```

### 10. Iniciar a Aplicação

```bash
cd scrapping-backend

# Usando Makefile
make dev

# Ou diretamente
uv run uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Verificação de Problemas

### Erro: "Diretório de JSONs não encontrado"

**Causa:** A pasta `json/` não existe ou está no lugar errado.

**Solução:**
```bash
# Verificar se a pasta existe
ls -la scrapping-backend/json/

# Se não existir, criar e copiar arquivos
mkdir -p scrapping-backend/json
cp /caminho/para/arquivos/*.json scrapping-backend/json/
```

### Erro: "relation already exists"

**Causa:** As tabelas já existem no banco.

**Solução:** A migration `create_pub_tables` é idempotente e verifica se as tabelas existem antes de criar. Se ainda assim der erro, você pode:

```bash
# Verificar status das migrations
uv run alembic current

# Se necessário, marcar migration como aplicada
uv run alembic stamp head
```

### Erro: "Nenhuma publicação encontrada"

**Causa:** Não há arquivos JSON na pasta `json/` ou estão vazios.

**Solução:**
```bash
# Verificar arquivos JSON
ls -lh scrapping-backend/json/*.json

# Verificar se não estão vazios
wc -l scrapping-backend/json/*.json
```

## 📦 Checklist de Reprodução

Use este checklist ao configurar em um novo computador:

- [ ] Código do projeto copiado/clonado
- [ ] `uv` instalado
- [ ] PostgreSQL instalado e rodando
- [ ] Dependências instaladas (`uv sync`)
- [ ] Arquivo `.env` configurado
- [ ] Banco de dados criado
- [ ] Pasta `json/` criada em `scrapping-backend/json/`
- [ ] Arquivos JSON copiados para `scrapping-backend/json/`
- [ ] Modelo spaCy baixado
- [ ] Migrations executadas (`alembic upgrade head`)
- [ ] Dados verificados no banco
- [ ] Aplicação iniciada e funcionando

## 🔐 Segurança e Dados Sensíveis

### Se os dados JSON são sensíveis:

1. **Não versionar a pasta `json/` no Git:**
   ```bash
   # Adicionar ao .gitignore
   echo "json/*.json" >> .gitignore
   ```

2. **Compartilhar dados de forma segura:**
   - Usar serviços de compartilhamento seguro
   - Criptografar antes de enviar
   - Usar variáveis de ambiente para caminhos alternativos

3. **Processamento seguro:**
   - Os dados são processados **diretamente em memória** durante a migration
   - **Não são armazenados** em arquivos Python intermediários
   - São inseridos diretamente no banco de dados

## 🎯 Resumo do Fluxo

```
1. Código → 2. Dependências → 3. Config (.env) → 4. PostgreSQL
                                                          ↓
8. Aplicação ← 7. Verificar ← 6. Migrations ← 5. JSONs
```

**Pontos-chave:**
- ✅ Tudo usa **caminhos relativos** (portável)
- ✅ Dados processados **em memória** (seguro)
- ✅ Migrations **idempotentes** (podem rodar múltiplas vezes)
- ✅ Estrutura **reproduzível** em qualquer máquina

## 📚 Documentação Adicional

- [README.md](../README.md) - Documentação principal
- [quickstart.md](./quickstart.md) - Guia rápido
- [database-setup.md](./database-setup.md) - Setup detalhado do banco
- [json/README.md](../json/README.md) - Sobre a pasta JSON

