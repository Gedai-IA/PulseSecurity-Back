#!/bin/bash
# Script para aplicar migrações do banco de dados

set -e

echo "🔄 Aplicando migrações do banco de dados..."

# Muda para o diretório do backend (um nível acima)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BACKEND_DIR"

# Verifica status atual
echo "📋 Verificando status atual das migrações..."
uv run alembic current

echo ""
echo "⬆️  Aplicando todas as migrações pendentes..."
uv run alembic upgrade head

echo ""
echo "✅ Migrações aplicadas com sucesso!"
echo ""
echo "📋 Status final:"
uv run alembic current

echo ""
echo "💡 Para verificar as tabelas criadas, execute:"
echo "   psql -h localhost -U scrapping_user -d scrapping_db -c '\\dt'"

