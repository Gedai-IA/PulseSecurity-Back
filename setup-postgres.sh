#!/bin/bash
# Script para instalar e configurar PostgreSQL

set -e

echo "🐘 Configurando PostgreSQL..."

# Verifica se PostgreSQL está instalado
if ! command -v psql &> /dev/null || ! sudo service postgresql status &> /dev/null; then
    echo "📦 Instalando PostgreSQL..."
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
    echo "✅ PostgreSQL instalado"
else
    echo "✅ PostgreSQL já está instalado"
fi

# Inicia o serviço PostgreSQL
echo "🚀 Iniciando serviço PostgreSQL..."
sudo service postgresql start

# Aguarda o PostgreSQL iniciar
sleep 3

# Verifica se o serviço está rodando
if ! sudo service postgresql status &> /dev/null; then
    echo "❌ Erro: Não foi possível iniciar o PostgreSQL"
    exit 1
fi

echo "✅ PostgreSQL está rodando"

# Obtém a versão do PostgreSQL
PG_VERSION=$(sudo -u postgres psql -tAc "SELECT version();" | head -1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "📋 Versão do PostgreSQL: $PG_VERSION"

# Cria o banco de dados se não existir
DB_NAME="scrapping_db"
DB_USER="scrapping_user"
DB_PASSWORD="scrapping_password"

echo "🔧 Configurando banco de dados..."

# Verifica se o banco já existe
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "ℹ️  Banco de dados '$DB_NAME' já existe"
else
    echo "📦 Criando banco de dados '$DB_NAME'..."
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    echo "✅ Banco de dados criado"
fi

# Verifica se o usuário já existe
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    echo "ℹ️  Usuário '$DB_USER' já existe"
    # Atualiza a senha
    sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
else
    echo "👤 Criando usuário '$DB_USER'..."
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    echo "✅ Usuário criado"
fi

# Concede privilégios
echo "🔐 Concedendo privilégios..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;"
echo "✅ Privilégios concedidos"

# Verifica se o arquivo .env existe
# Muda para o diretório do backend (se o script estiver na raiz)
if [ -d "scrapping-backend" ]; then
    cd scrapping-backend
elif [ ! -f ".env" ] && [ -f "env.example" ]; then
    # Já está no diretório do backend
    :
else
    echo "⚠️  Aviso: Execute este script da raiz do projeto (gedai/) ou do diretório scrapping-backend/"
fi
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Arquivo .env criado a partir de env.example"
    else
        echo "❌ Erro: env.example não encontrado"
        exit 1
    fi
else
    echo "ℹ️  Arquivo .env já existe"
fi

# Atualiza o DATABASE_URL no .env
echo "🔧 Configurando DATABASE_URL no .env..."
DATABASE_URL="postgresql+asyncpg://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"

# Usa sed para atualizar ou adicionar DATABASE_URL
if grep -q "^DATABASE_URL=" .env; then
    # Atualiza linha existente
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^DATABASE_URL=.*|DATABASE_URL=$DATABASE_URL|" .env
    else
        sed -i "s|^DATABASE_URL=.*|DATABASE_URL=$DATABASE_URL|" .env
    fi
else
    # Adiciona nova linha
    echo "DATABASE_URL=$DATABASE_URL" >> .env
fi

echo "✅ DATABASE_URL configurado: postgresql+asyncpg://$DB_USER:***@localhost:5432/$DB_NAME"

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "📋 Informações do banco de dados:"
echo "   Host: localhost"
echo "   Porta: 5432"
echo "   Banco: $DB_NAME"
echo "   Usuário: $DB_USER"
echo "   Senha: $DB_PASSWORD"
echo ""
echo "💡 Próximos passos:"
echo "   1. Execute 'make upgrade' no diretório scrapping-backend para aplicar as migrações"
echo "   2. Ou execute 'make migrate msg=\"nome da migração\"' para criar uma nova migração"
echo ""

