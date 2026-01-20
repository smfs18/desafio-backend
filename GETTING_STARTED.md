# GETTING_STARTED.md

## 🎯 Começar em 5 minutos

### Opção 1: Docker (Mais fácil ✨)

```bash
# 1. Clone e entre no diretório
git clone <seu-repo>
cd desafio-backend

# 2. Inicie tudo com um comando
make docker-up

# 3. Pronto! A API está rodando em http://localhost:8000

# 4. Acesse a documentação interativa
open http://localhost:8000/docs
```

### Opção 2: Ambiente Local

```bash
# 1. Certifique-se de ter Python 3.11+ e PostgreSQL 16+
python --version
psql --version

# 2. Clone o repositório
git clone <seu-repo>
cd desafio-backend

# 3. Crie um virtual environment
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 4. Instale as dependências
make install

# 5. Configure o banco de dados
psql -U postgres -c "CREATE DATABASE vlab_fuel;"

# 6. Configure as variáveis de ambiente
cp .env.example .env

# 7. Execute as migrations
make db-upgrade

# 8. Inicie a API
make run

# 9. Acesse em http://localhost:8000/docs
```

---

## 🧪 Teste a API

### Health Check (sem autenticação)

```bash
curl http://localhost:8000/health
```

### Criar um motorista

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

### Criar um abastecimento

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

### Listar abastecimentos com paginação

```bash
curl "http://localhost:8000/api/v1/abastecimentos?page=1&page_size=20" \
  -H "X-API-Key: your-secret-api-key-here"
```

---

## 📚 Estrutura do Projeto

```
desafio-backend/
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── core/                  # Infraestrutura
│   ├── api/v1/                # Routers
│   ├── domain/                # Models, Schemas, Validators
│   ├── services/              # Lógica de negócio
│   ├── repositories/          # Acesso a dados
│   └── tests/                 # Testes
├── alembic/                   # Database migrations
├── docker/                    # Docker files
├── scripts/                   # Scripts utilitários
├── Dockerfile                 # Container build
├── docker-compose.yml         # Orquestração de containers
├── pyproject.toml             # Dependências Python
├── Makefile                   # Comandos úteis
└── README.md                  # Documentação
```

---

## 🏛️ Arquitetura em 30 segundos

```
HTTP Request
   ↓
Router (FastAPI)  ← Recebe HTTP, valida com Pydantic
   ↓
Service           ← Lógica de negócio (anomalia, etc)
   ↓
Repository        ← Acesso ao banco (SQLAlchemy)
   ↓
PostgreSQL        ← Banco de dados
```

---

## 🧪 Rodar Testes

```bash
# Todos os testes
make test

# Testes específicos
pytest app/tests/test_cpf.py -v

# Com cobertura
pytest --cov=app
```

---

## 🔧 Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `make help` | Mostra todos os comandos |
| `make run` | Inicia servidor (reload automático) |
| `make test` | Roda testes |
| `make lint` | Verifica código |
| `make format` | Formata código |
| `make clean` | Remove arquivos temporários |
| `make docker-up` | Inicia containers |
| `make docker-down` | Para containers |
| `make load-data` | Carrega dados iniciais |
| `make db-upgrade` | Aplica migrations |

---

## 🐛 Troubleshooting

### "Connection refused" ao conectar ao PostgreSQL

```bash
# Verifique se o container está rodando
docker ps

# Se não estiver, reinicie
make docker-down
make docker-up

# Aguarde alguns segundos para o PostgreSQL ficar pronto
sleep 10
```

### "ImportError: No module named 'fastapi'"

```bash
# Reinstale as dependências
pip install -e .
```

### "Database 'vlab_fuel' does not exist"

```bash
# Crie o banco (se estiver rodando localmente)
psql -U postgres -c "CREATE DATABASE vlab_fuel;"

# Ou use Docker
make docker-up
```

---

## 📖 Próximos Passos

1. Abra http://localhost:8000/docs para ver a documentação interativa
2. Explore os endpoints com o Swagger UI
3. Leia o [README.md](README.md) para detalhes de arquitetura
4. Leia [CONTRIBUTING.md](CONTRIBUTING.md) para contribute ao projeto
5. Veja o código em `app/` para entender a estrutura

---

## 💡 Exemplos

### Criar motorista e abastecimento

```bash
# 1. Criar motorista
MOTORISTA=$(curl -s -X POST http://localhost:8000/api/v1/motoristas \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "nome": "Maria Silva",
    "cpf": "98765432100",
    "email": "maria@example.com",
    "telefone": "21999999999"
  }')

ID=$(echo $MOTORISTA | jq '.id')

# 2. Criar abastecimento
curl -X POST http://localhost:8000/api/v1/abastecimentos \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d "{
    \"motorista_id\": $ID,
    \"tipo_combustivel\": \"diesel\",
    \"valor\": 300.00,
    \"litros\": 50.0
  }"
```

### Detectar anomalias

```bash
# Abastecimento normal (preço OK)
curl -X POST http://localhost:8000/api/v1/abastecimentos \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "motorista_id": 1,
    "tipo_combustivel": "gasolina",
    "valor": 250.00,
    "litros": 40.0
  }'

# Response: "status": "pendente", "eh_anomalia": false

# Abastecimento suspeito (preço muito alto!)
curl -X POST http://localhost:8000/api/v1/abastecimentos \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "motorista_id": 1,
    "tipo_combustivel": "gasolina",
    "valor": 600.00,
    "litros": 20.0
  }'

# Response: "status": "anomalia", "eh_anomalia": true
```

---

**Dúvidas? Abra uma issue no repositório! 🚀**
