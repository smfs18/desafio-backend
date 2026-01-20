# 🎯 QUICK REFERENCE - Comandos Essenciais

## 🚀 Inicialização Rápida

```bash
# 1. Inicie PostgreSQL
docker run --name vlab-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=vlab_fuel \
  -p 5433:5432 \
  -d postgres:16-alpine

# 2. Setup Python
cd /home/smfs/Documentos/desafio-backend
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install email-validator

# 3. Database
python run_migrations.py
python scripts/load_data.py

# 4. Run API
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Endpoints

### Health Check ✅
```bash
curl http://localhost:8000/health
```

### Listar Abastecimentos 📋
```bash
curl http://localhost:8000/api/v1/abastecimentos \
  -H "X-API-Key: your-secret-api-key-here"
```

### Criar Abastecimento ➕
```bash
curl -X POST http://localhost:8000/api/v1/abastecimentos \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "motorista_id": 1,
    "tipo_combustivel": "gasolina",
    "valor": 250.00,
    "litros": 40.0
  }'
```

### Criar Motorista 👤
```bash
curl -X POST http://localhost:8000/api/v1/motoristas \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678909",
    "email": "joao@example.com",
    "telefone": "11999999999"
  }'
```

### Listar Motoristas 👥
```bash
curl http://localhost:8000/api/v1/motoristas \
  -H "X-API-Key: your-secret-api-key-here"
```

### Paginação 📖
```bash
curl "http://localhost:8000/api/v1/abastecimentos?page=1&page_size=20" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Filtrar por Status 🔍
```bash
curl "http://localhost:8000/api/v1/abastecimentos?status=anomalia" \
  -H "X-API-Key: your-secret-api-key-here"
```

---

## 🧪 Testes

```bash
# Todos os testes
pytest app/tests/ -v

# CPF validation tests
pytest app/tests/test_cpf.py -v

# Anomaly detection tests
pytest app/tests/test_anomaly.py -v

# Com cobertura
pytest --cov=app --cov-report=html
```

---

## 🔧 Makefile Commands

```bash
# Help
make help

# Development
make run              # Inicia servidor
make test             # Roda testes
make lint             # Verifica código
make format           # Formata código
make clean            # Limpa cache

# Database
make db-upgrade       # Aplica migrations
make db-downgrade     # Desfaz última migration
make load-data        # Carrega dados iniciais

# Docker
make docker-up        # Inicia containers
make docker-down      # Para containers
make docker-logs      # Mostra logs
```

---

## 📚 Documentação

```bash
# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc

# Files
cat README.md                    # Documentação completa
cat REQUIREMENTS_CHECKLIST.md    # Verificação de requisitos
cat ARCHITECTURE.md              # Diagramas de arquitetura
cat TEST_RESULTS.md              # Resultados dos testes
cat POSTGRES_SETUP.md            # Guia PostgreSQL
cat GETTING_STARTED.md           # Quick start
cat CONTRIBUTING.md              # Guia de contribuição
cat SUMMARY.md                   # Resumo executivo
```

---

## 🔑 Variáveis de Ambiente

```bash
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5433/vlab_fuel
ENVIRONMENT=development
API_KEY=your-secret-api-key-here
LOG_LEVEL=INFO
```

---

## 🐛 Troubleshooting

### PostgreSQL já está rodando
```bash
# Listar containers
docker ps

# Remover container antigo
docker rm -f vlab-postgres

# Recomeçar
docker run --name vlab-postgres ...
```

### Porta 5433 em uso
```bash
# Mude para 5434
-p 5434:5432

# Atualize .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5434/vlab_fuel
```

### ModuleNotFoundError
```bash
# Reinstale dependências
pip install -e .
pip install email-validator
```

### Banco de dados não criado
```bash
# Execute migrations
python run_migrations.py

# Carregue dados
python scripts/load_data.py
```

---

## 📊 Status Commands

```bash
# Verificar API
curl -s http://localhost:8000/health | jq .

# Verificar banco
docker exec vlab-postgres psql -U postgres -d vlab_fuel -c "SELECT COUNT(*) FROM motoristas;"

# Ver logs da API
tail -f /tmp/api.log

# Ver containers rodando
docker ps

# Ver status das dependências
pip show fastapi sqlalchemy pydantic
```

---

## 🎯 Exemplos de Requests com jq

```bash
# Listar com jq (parse JSON)
curl -s http://localhost:8000/api/v1/abastecimentos \
  -H "X-API-Key: your-secret-api-key-here" | jq '.items[0]'

# Pretty print
curl -s http://localhost:8000/api/v1/abastecimentos \
  -H "X-API-Key: your-secret-api-key-here" | jq '.'

# Contar registros
curl -s http://localhost:8000/api/v1/abastecimentos \
  -H "X-API-Key: your-secret-api-key-here" | jq '.total'

# Filtrar anomalias
curl -s "http://localhost:8000/api/v1/abastecimentos?status=anomalia" \
  -H "X-API-Key: your-secret-api-key-here" | jq '.items[].eh_anomalia'
```

---

## 💾 Database Queries

```bash
# Conectar ao PostgreSQL
docker exec -it vlab-postgres psql -U postgres -d vlab_fuel

# Inside psql:
\dt                                    # List tables
\d motoristas                          # Describe table
SELECT * FROM motoristas;              # See drivers
SELECT * FROM abastecimentos;          # See refills
SELECT COUNT(*) FROM abastecimentos;   # Count refills
SELECT * FROM abastecimentos WHERE eh_anomalia = true;  # Anomalies
\q                                     # Exit
```

---

## 🚀 Production Ready

```bash
# Build production image
docker build -f Dockerfile -t vlab-api:latest .

# Run with Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# Check status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f api
```

---

## 📝 Common CPF Values for Testing

**Valid CPFs:**
- 12345678909
- 98765432100
- 55555555555
- 11144477735

**Invalid CPFs:**
- 111.111.111-11 (all same digits)
- 12345678901 (wrong check digit)
- 123.456.789 (too short)

---

## 🎉 Success Indicators

✅ Health check retorna `{"status":"healthy"}`  
✅ Abastecimentos listam com paginação  
✅ Anomalias são detectadas (eh_anomalia=true)  
✅ CPF inválido é rejeitado  
✅ API Key obrigatória funciona  
✅ Banco tem motoristas e abastecimentos  
✅ Testes passam sem erros  

---

**Tudo pronto para production! 🚀**
