# Configuração do Banco de Dados

Este guia detalha como configurar e gerenciar o banco de dados PostgreSQL para o projeto.

## Pré-requisitos

- PostgreSQL 14+ instalado
- Acesso de administrador ao PostgreSQL (para criar banco e usuário)

## Instalação do PostgreSQL

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo service postgresql start
```

### Verificar Instalação

```bash
# Verificar se está rodando
sudo service postgresql status

# Verificar versão
psql --version
```

## Configuração Inicial

### Opção A - Script Automatizado (Recomendado)

**⚠️ IMPORTANTE:** Use o script de configuração automática que faz tudo por você:

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

**Após executar o script, pule para a seção [Migrations](#migrations) abaixo.**

### Opção B - Configuração Manual

Se preferir fazer manualmente:

#### 1. Criar Banco de Dados

```bash
sudo -u postgres psql -c "CREATE DATABASE scrapping_db;"
```

#### 2. Criar Usuário

```bash
sudo -u postgres psql -c "CREATE USER scrapping_user WITH PASSWORD 'scrapping_password';"
```

#### 3. Conceder Privilégios

```bash
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE scrapping_db TO scrapping_user;"
sudo -u postgres psql -d scrapping_db -c "GRANT ALL ON SCHEMA public TO scrapping_user;"
```

#### 4. Configurar Variáveis de Ambiente

No arquivo `.env` do backend:

```env
DATABASE_URL=postgresql+asyncpg://scrapping_user:scrapping_password@localhost:5432/scrapping_db
```

## Migrations

### Usando Alembic (Recomendado)

O projeto usa **Alembic** para gerenciar o schema do banco de dados.

#### Aplicar Migrations

```bash
# Aplicar todas as migrations pendentes
make upgrade

# Ou diretamente
uv run alembic upgrade head
```

#### Criar Nova Migration

1. Faça alterações nos models em `app/infrastructure/database/models.py`

2. Gere a migration:
   ```bash
   make migrate msg="descrição da alteração"
   ```

3. Revise o arquivo gerado em `alembic/versions/`

4. Aplique a migration:
   ```bash
   make upgrade
   ```

#### Verificar Status

```bash
# Ver migration atual aplicada
uv run alembic current

# Ver histórico de migrations
uv run alembic history

# Ver SQL que será executado (sem aplicar)
uv run alembic upgrade head --sql
```

### Usando Scripts SQL (Alternativa)

Se as migrations do Alembic não funcionarem, você pode usar os scripts SQL diretos.

#### Criar Todas as Tabelas

```bash
./scripts/apply-all-tables.sh
```

Este script cria:
- `publications` - Publicações principais
- `comments` - Comentários
- `replies` - Respostas
- `publication_analyses` - Análises de publicações
- `comment_analyses` - Análises de comentários

#### Criar Apenas Tabela Users

```bash
./scripts/apply-sql-migration.sh
```

#### Sincronizar Alembic Após Criar Tabelas Manualmente

Se você criou tabelas via SQL e quer sincronizar o Alembic:

```bash
# Marca a migration atual como aplicada
uv run alembic stamp head

# Ou marca uma migration específica
uv run alembic stamp <revision_id>
```

## Verificação

### Listar Tabelas

```bash
psql -h localhost -U scrapping_user -d scrapping_db -c "\dt"
```

### Ver Estrutura de uma Tabela

```bash
psql -h localhost -U scrapping_user -d scrapping_db -c "\d users"
psql -h localhost -U scrapping_user -d scrapping_db -c "\d publications"
```

### Testar Conexão

```bash
psql -h localhost -U scrapping_user -d scrapping_db -c "SELECT version();"
```

## Troubleshooting

### Erro: "relation does not exist"

As tabelas não foram criadas. Execute:

```bash
./scripts/apply-all-tables.sh
```

### Erro: "Target database is not up to date"

Aplique as migrations pendentes:

```bash
make upgrade
```

### Erro: "password authentication failed"

Verifique:
- Usuário e senha no `.env`
- Permissões do usuário no PostgreSQL

### Erro: "could not connect to server"

Verifique:
- PostgreSQL está rodando: `sudo service postgresql status`
- Porta correta (padrão: 5432)
- Firewall não está bloqueando

### Resetar Banco de Dados

⚠️ **ATENÇÃO:** Isso apagará todos os dados!

```bash
# Conectar como postgres
sudo -u postgres psql

# No prompt do PostgreSQL:
DROP DATABASE scrapping_db;
CREATE DATABASE scrapping_db;
GRANT ALL PRIVILEGES ON DATABASE scrapping_db TO scrapping_user;
\q

# Recriar todas as tabelas
./scripts/apply-all-tables.sh
```

## Estrutura das Tabelas

### Tabelas Principais

- **users** - Usuários do sistema
- **publications** - Publicações de redes sociais
- **comments** - Comentários das publicações
- **replies** - Respostas aos comentários
- **publication_analyses** - Análises de sentimento/emoção/tópico das publicações
- **comment_analyses** - Análises de sentimento/emoção/tópico dos comentários

### Relacionamentos

- `comments.publication_id` → `publications.id`
- `replies.comment_id` → `comments.id`
- `publication_analyses.publication_id` → `publications.id`
- `comment_analyses.comment_id` → `comments.id`

## Backup e Restore

### Backup

```bash
pg_dump -h localhost -U scrapping_user -d scrapping_db > backup.sql
```

### Restore

```bash
psql -h localhost -U scrapping_user -d scrapping_db < backup.sql
```

## Recursos Adicionais

- [Documentação do PostgreSQL](https://www.postgresql.org/docs/)
- [Documentação do Alembic](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)

