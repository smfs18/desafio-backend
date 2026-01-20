#!/bin/bash

# 🚀 Script de Inicialização Rápida - V-Lab Backend

set -e

echo "=========================================="
echo "🚀 V-Lab Backend - Quick Start"
echo "=========================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Verificar Docker
echo -e "${BLUE}[1/5]${NC} Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não está instalado!${NC}"
    echo "Instale em: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✅ Docker encontrado${NC}"

# 2. Limpar containers antigos (opcional)
echo -e "${BLUE}[2/5]${NC} Limpando containers antigos (se existirem)..."
docker stop vlab-postgres 2>/dev/null || true
docker rm vlab-postgres 2>/dev/null || true
echo -e "${GREEN}✅ Limpo${NC}"

# 3. Iniciar PostgreSQL
echo -e "${BLUE}[3/5]${NC} Iniciando PostgreSQL..."
docker run --name vlab-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=vlab_fuel \
  -p 5432:5432 \
  -v postgres_vlab_data:/var/lib/postgresql/data \
  -d postgres:16-alpine

echo -e "${GREEN}✅ PostgreSQL iniciado${NC}"

# 4. Aguardar PostgreSQL ficar pronto
echo -e "${BLUE}[4/5]${NC} Aguardando PostgreSQL ficar pronto..."
for i in {1..30}; do
    if docker exec vlab-postgres pg_isready -U postgres &> /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL está pronto!${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# 5. Verificar acesso
echo -e "${BLUE}[5/5]${NC} Verificando conexão..."
docker exec vlab-postgres psql -U postgres -d vlab_fuel -c "SELECT version();" > /dev/null && \
echo -e "${GREEN}✅ Conexão bem-sucedida!${NC}" || \
echo -e "${RED}❌ Erro na conexão${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ PRONTO PARA COMEÇAR!${NC}"
echo "=========================================="
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo ""
echo "1. Instale as dependências Python:"
echo "   pip install -e ."
echo ""
echo "2. Execute as migrations:"
echo "   alembic upgrade head"
echo ""
echo "3. Inicie a API:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Acesse a documentação:"
echo "   http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Ou, para usar Docker Compose (tudo junto):${NC}"
echo "   docker-compose -f docker/docker-compose.yml up"
echo ""
echo "=========================================="
