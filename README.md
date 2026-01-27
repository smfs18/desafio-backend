# V-Lab Fuel Gateway API 🚗⛽

> Backend challenge - RESTful API for fuel refill management with anomaly detection

**Status**: ✅ Production-Ready Architecture | 🏗️ Built with Clean Architecture Principles

---

## 📋 Visão Geral

A **V-Lab Fuel Gateway API** é uma aplicação backend em FastAPI que gerencia abastecimentos de combustível para frotas de motoristas, com detecção automática de anomalias.

### Características Principais

✅ **Arquitetura em Camadas** - Clean Architecture  
✅ **Detecção de Anomalias** - Identifica abastecimentos suspeitos (>25% do preço normal)  
✅ **Validação de CPF** - Regras de negócio reutilizáveis e testáveis  
✅ **Paginação** - Suporte completo para listagem com filtros  
✅ **Async/Await** - Operações não-bloqueantes com SQLAlchemy async  
✅ **API Versionada** - `/api/v1` preparada para futuras versões  
✅ **Docker-Ready** - Container multi-stage otimizado para produção  
✅ **Migrations** - Alembic integrado para versionamento de banco  

---

## 🏛️ Arquitetura

### Visão Geral de uma Requisição 

```
HTTP Request
   ↓
Router (FastAPI)
   ↓
Service (Regras de negócio)
   ↓
Repository (Banco de dados)
   ↓
PostgreSQL
```

### Estrutura de Pastas

```
app/
├── main.py                          # Entrada da aplicação
├── core/                            # Infraestrutura
│   ├── config.py                    # Configurações do Pydantic Settings
│   ├── database.py                  # SQLAlchemy Engine + Session
│   ├── security.py                  # Validação de API Key
│   └── logging.py                   # Configuração de logs
├── api/v1/                          # Routers versionados
│   └── routers/
│       ├── health.py                # Health check
│       ├── motoristas.py            # Endpoints de motoristas
│       └── abastecimentos.py        # Endpoints de abastecimentos
├── domain/                          # Modelos de negócio
│   ├── models/
│   │   ├── motorista.py             # ORM do motorista
│   │   ├── abastecimento.py         # ORM do abastecimento
│   │   └── enums.py                 # Enums compartilhados
│   ├── schemas/
│   │   ├── motorista.py             # Pydantic schemas
│   │   └── abastecimento.py         # Pydantic schemas
│   └── validators/
│       └── cpf.py                   # Validação de CPF
├── services/                        # Lógica de negócio
│   ├── abastecimento_service.py     # Orquestração
│   └── anomaly_service.py           # Detecção de anomalias
├── repositories/                    # Acesso a dados
│   ├── base.py                      # CRUD genérico
│   ├── abastecimento_repository.py  # Queries específicas
│   └── motorista_repository.py      # Queries específicas
└── tests/                           # Testes unitários
    ├── conftest.py                  # Fixtures do pytest
    └── test_cpf.py                  # Testes de validação
```

### Responsabilidade de Cada Camada

#### 🔌 `api/routers/`
- ✅ Recebe e valida requests (Pydantic)
- ✅ Chama services
- ✅ Retorna responses HTTP
- ❌ SEM regra de negócio
- ❌ SEM SQL direto

#### 💼 `services/`
- ✅ Lógica de negócio (anomalia, orquestração)
- ✅ Independente de FastAPI
- ✅ Fácil de testar e reutilizar
- ✅ Orquestra repositories

#### 🗄️ `repositories/`
- ✅ Queries SQLAlchemy isoladas
- ✅ Fácil de mockar em testes
- ✅ Operações CRUD genéricas

#### 📦 `domain/`
- ✅ **models/** - Mapeamento ORM (banco de dados)
- ✅ **schemas/** - Contrato da API (entrada/saída)
- ✅ **validators/** - Regras reutilizáveis

#### ⚙️ `core/`
- ✅ Database connection
- ✅ Configuração
- ✅ Segurança
- ✅ Logging

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- PostgreSQL 16+ (ou use Docker)
- pip

### 1️⃣ Instalação

```bash
# Clone o repositório
git clone <seu-repo>
cd desafio-backend

# Instale as dependências
make install

# (Opcional) Instale dependências de desenvolvimento
make dev
```

### 2️⃣ Configuração

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite .env com suas configurações
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

### 3️⃣ Execute com Docker (Recomendado)

```bash
# Inicie os containers
make docker-up

# Aguarde o PostgreSQL ficar pronto
docker-compose -f docker/docker-compose.yml ps

# Acesse a API
curl http://localhost:8000/health
```

### 4️⃣ Ou Execute Localmente

```bash
# Certifique-se de que o PostgreSQL está rodando
psql -U postgres -c "CREATE DATABASE vlab_fuel;"

# Execute as migrations
make db-upgrade

# Inicie o servidor
make run

# A API estará disponível em http://localhost:8000
```

### 5️⃣ (Opcional) Carregue dados iniciais

```bash
make load-data
```

---

## 📚 Exemplos de Uso

### Health Check

```bash
curl http://localhost:8000/health

# Response:
# {"status": "healthy"}
```

### Criar Motorista

```bash
curl -X POST http://localhost:8000/api/v1/motoristas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678909",
    "email": "joao@example.com",
    "telefone": "11999999999"
  }'
```

### Criar Abastecimento (com Detecção de Anomalia)

```bash
curl -X POST http://localhost:8000/api/v1/abastecimentos \
  -H "Content-Type: application/json" \
  -d '{
    "motorista_id": 1,
    "tipo_combustivel": "gasolina",
    "valor": 250.00,
    "litros": 40.0
  }'

# Response (NORMAL):
# {
#   "id": 1,
#   "motorista_id": 1,
#   "tipo_combustivel": "gasolina",
#   "valor": 250.00,
#   "litros": 40.0,
#   "status": "pendente",
#   "eh_anomalia": false,
#   ...
# }

# Response (ANOMALIA - preço por litro > 25% acima do normal):
# {
#   "id": 2,
#   "motorista_id": 1,
#   "tipo_combustivel": "gasolina",
#   "valor": 600.00,
#   "litros": 20.0,      # 30/litro - anomalia!
#   "status": "anomalia",
#   "eh_anomalia": true,
#   ...
# }
```

### Listar Abastecimentos com Paginação

```bash
curl "http://localhost:8000/api/v1/abastecimentos?page=1&page_size=20"

# Response:
# {
#   "items": [...],
#   "total": 45,
#   "pagina": 1,
#   "tamanho_pagina": 20,
#   "total_paginas": 3
# }
```

### Filtrar por Status

```bash
curl "http://localhost:8000/api/v1/abastecimentos?status=anomalia"
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
make test

# Testes específicos
pytest app/tests/test_cpf.py -v

# Com cobertura
pytest --cov=app
```

### Exemplo: Validação de CPF

```python
# app/tests/test_cpf.py
def test_valid_cpf():
    assert validate_cpf("123.456.789-09") is True

def test_invalid_cpf_all_same_digits():
    assert validate_cpf("111.111.111-11") is False
```

---

## 🔧 Comandos Úteis

```bash
# Development
make run              # Inicia servidor com reload automático
make lint             # Roda linters (ruff, mypy)
make format           # Formata código (black, isort)
make clean            # Remove arquivos temporários

# Docker
make docker-up        # Inicia containers
make docker-down      # Para containers
make docker-logs      # Mostra logs da API

# Database
make db-upgrade       # Aplica migrations
make db-downgrade     # Desfaz última migration
make load-data        # Carrega dados iniciais
```

---

## 🎯 Decisões de Arquitetura

### Por que Clean Architecture?

1. **Separação de Responsabilidades** - Cada camada tem um propósito claro
2. **Testabilidade** - Fácil isolar e testar cada componente
3. **Escalabilidade** - Pronto para times maiores
4. **Profissionalismo** 

### Por que SQLAlchemy Async?

- Non-blocking I/O
- Melhor performance em alta concorrência
- Preparado para escala

### Por que Pydantic v2?

- Validação automática
- Serialização JSON nativa
- Type hints robustos
- Performance melhorada

### Por que Alembic?

- Versionamento de banco de dados
- Rollback seguro
- Documentação automática de changes

---

## 🔒 Segurança

### API Key

Todos os endpoints (exceto `/health`) exigem API Key:

```bash
curl -X GET http://localhost:8000/api/v1/motoristas \
  -H "X-API-Key: your-secret-api-key-here"
```

Configure a API Key no `.env`:

```
API_KEY=seu-secret-key-super-seguro-aqui
```

### Validação de Entrada

- Pydantic valida todos os payloads automaticamente
- Regras customizadas em `validators/`
- Type hints previnem erros de tipo

---

## 📖 Documentação

### Swagger UI

Abra `http://localhost:8000/docs` para acessar a documentação interativa.

### ReDoc

Abra `http://localhost:8000/redoc` para documentação alternativa.

---

## 🚀 Deployment

### Com Docker

```bash
# Build image
docker build -f Dockerfile -t vlab-api:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/vlab_fuel \
  vlab-api:latest
```

### Com Docker Compose (Recomendado)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

---

## 📊 Monitoramento

### Health Check

```bash
curl http://localhost:8000/health
```

O endpoint `/health` é usado por orquestradores (K8s, Nomad, etc.) para verificar se a aplicação está pronta.

---

## 🐛 Troubleshooting

### Erro: "Connection refused"

```bash
# Verifique se o PostgreSQL está rodando
docker ps | grep postgres

# Se não estiver, inicie com Docker
docker-compose -f docker/docker-compose.yml up -d postgres
```

### Erro: "ImportError"

```bash
# Reinstale as dependências
pip install -e .
```

### Erro: "No module named 'app'"

```bash
# Certifique-se de estar na raiz do projeto
pwd  # Deve terminar com /desafio-backend
```

---

## 📝 Próximos Passos (Roadmap)

- [ ] Autenticação com JWT
- [ ] Rate limiting
- [ ] Cache com Redis
- [ ] Documentação OpenAPI completa
- [ ] Testes de integração
- [ ] CI/CD com GitHub Actions
- [ ] Observability (Prometheus, Jaeger)
- [ ] GraphQL (opcional)

---

## 👨‍💻 Stack Tecnológico

| Componente | Tecnologia |
|-----------|-----------|
| **Framework Web** | FastAPI 0.104+ |
| **Servidor ASGI** | Uvicorn 0.24+ |
| **ORM** | SQLAlchemy 2.0+ |
| **Banco de Dados** | PostgreSQL 16+ |
| **Validação** | Pydantic v2 |
| **Migrations** | Alembic |
| **Async Driver** | asyncpg |
| **Testes** | pytest |
| **Linting** | ruff |
| **Formatação** | black |
| **Containerização** | Docker |

---

## 📄 Licença

MIT License - Ver LICENSE para detalhes

---

## ✨ Diferenciais

✅ API versionada (`/api/v1`)  
✅ Alembic rodando automaticamente  
✅ Script de carga isolado  
✅ Testes focados em regra (CPF + anomalia)  
✅ `.env.example`  
✅ README explicando decisões  
✅ Clean Architecture   
✅ Async/Await nativo  
✅ Dockerfile multi-stage  
✅ Docker Compose completo  
✅ Makefile para comandos comuns  
✅ Health check para orquestradores  

---

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido por Silas Manoel** 🚀
