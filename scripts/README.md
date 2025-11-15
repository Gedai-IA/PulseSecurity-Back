# Scripts de Banco de Dados

Esta pasta contém scripts auxiliares para gerenciar o banco de dados.

## Scripts Disponíveis

### `apply-all-tables.sh`
Cria todas as tabelas do banco de dados diretamente via SQL.

**Uso:**
```bash
cd scrapping-backend
./scripts/apply-all-tables.sh
```

### `apply-sql-migration.sh`
Cria apenas a tabela `users` diretamente via SQL.

**Uso:**
```bash
cd scrapping-backend
./scripts/apply-sql-migration.sh
```

### `apply-migrations.sh`
Aplica as migrações do Alembic.

**Uso:**
```bash
cd scrapping-backend
./scripts/apply-migrations.sh
```

## Arquivos SQL

### `create_all_tables.sql`
Script SQL para criar todas as tabelas:
- publications
- comments
- replies
- publication_analyses
- comment_analyses

### `create_users_table.sql`
Script SQL para criar apenas a tabela `users`.

## Notas

- Todos os scripts devem ser executados a partir do diretório `scrapping-backend`
- Os scripts automaticamente detectam o diretório correto e encontram o arquivo `.env`
- Certifique-se de que o PostgreSQL está rodando antes de executar os scripts

