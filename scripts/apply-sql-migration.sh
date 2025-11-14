#!/bin/bash
# Script para aplicar a criação da tabela users via SQL direto

set -e

echo "🔧 Criando tabela users diretamente no banco de dados..."

# Muda para o diretório do backend (um nível acima)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BACKEND_DIR"

# Verifica se o arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Erro: Arquivo .env não encontrado"
    exit 1
fi

# Extrai informações do DATABASE_URL do .env
DB_URL=$(grep "^DATABASE_URL=" .env | cut -d '=' -f2-)

# Extrai componentes da URL
# Formato: postgresql+asyncpg://user:password@host:port/database
DB_USER=$(echo $DB_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
DB_PASS=$(echo $DB_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
DB_HOST=$(echo $DB_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DB_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
DB_NAME=$(echo $DB_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')

echo "📋 Conectando ao banco: $DB_NAME em $DB_HOST:$DB_PORT"
echo "👤 Usuário: $DB_USER"
echo ""

# Aplica o script SQL (usa caminho absoluto do script)
PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$SCRIPT_DIR/create_users_table.sql"

echo ""
echo "✅ Tabela users criada com sucesso!"
echo ""
echo "💡 Para verificar, execute:"
echo "   psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\\d users'"

