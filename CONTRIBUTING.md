# CONTRIBUTING.md

Guia para contribuir e trabalhar com este projeto.

## 📌 Estrutura do Projeto

```
app/
├── main.py              # FastAPI app factory
├── core/                # Infraestrutura (config, DB, security)
├── api/v1/              # Routers HTTP
├── domain/              # Models, Schemas, Validators
├── services/            # Lógica de negócio
├── repositories/        # Acesso a dados
└── tests/               # Testes unitários
```

## 🛠️ Setup Inicial

```bash
# 1. Instale as dependências
make install
make dev

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env conforme necessário

# 3. Inicie com Docker (recomendado)
make docker-up

# 4. Ou execute localmente
make run
```

## 📝 Workflow de Desenvolvimento

### 1. Criar uma Nova Feature

```bash
# Crie uma branch
git checkout -b feature/nome-da-feature

# Faça as mudanças
# ...

# Rode testes antes de commitar
make test

# Formate o código
make format

# Rode linter
make lint
```

### 2. Exemplo: Adicionar um Novo Endpoint

#### Passo 1: Criar o Schema (Input/Output)

```python
# app/domain/schemas/exemplo.py
from pydantic import BaseModel

class ExemploCreate(BaseModel):
    name: str
    value: int

class ExemploResponse(ExemploCreate):
    id: int
    class Config:
        from_attributes = True
```

#### Passo 2: Criar o Model (Banco de Dados)

```python
# app/domain/models/exemplo.py
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Exemplo(Base):
    __tablename__ = "exemplos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int] = mapped_column()
```

#### Passo 3: Criar o Repository

```python
# app/repositories/exemplo_repository.py
from app.repositories.base import BaseRepository
from app.domain.models.exemplo import Exemplo

class ExemploRepository(BaseRepository[Exemplo]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Exemplo)
```

#### Passo 4: Criar o Service (Lógica de Negócio)

```python
# app/services/exemplo_service.py
from app.repositories.exemplo_repository import ExemploRepository

class ExemploService:
    def __init__(self, session: AsyncSession):
        self.repository = ExemploRepository(session)
    
    async def create(self, name: str, value: int) -> Exemplo:
        exemplo = Exemplo(name=name, value=value)
        return await self.repository.create(exemplo)
```

#### Passo 5: Criar o Router

```python
# app/api/v1/routers/exemplo.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session

router = APIRouter(prefix="/api/v1/exemplos", tags=["exemplos"])

@router.post("", response_model=ExemploResponse)
async def create_exemplo(
    exemplo: ExemploCreate,
    session: AsyncSession = Depends(get_session)
):
    service = ExemploService(session)
    return await service.create(exemplo.name, exemplo.value)
```

#### Passo 6: Incluir o Router no Main

```python
# app/main.py
from app.api.v1.routers import exemplo

app.include_router(exemplo.router)
```

#### Passo 7: Criar Migration

```bash
# Gere uma migration automática
alembic revision --autogenerate -m "Add exemplo table"

# Verifique a migration em alembic/versions/
# Faça ajustes se necessário
```

## 🧪 Escrevendo Testes

```python
# app/tests/test_exemplo.py
import pytest

class TestExemploService:
    async def test_create_exemplo(self, test_session):
        service = ExemploService(test_session)
        resultado = await service.create("test", 42)
        assert resultado.name == "test"
        assert resultado.value == 42
```

## 🔍 Code Quality

### Lint

```bash
make lint
```

### Format

```bash
make format
```

### Testes com Cobertura

```bash
pytest --cov=app --cov-report=html
# Abra htmlcov/index.html
```

## 📦 Dependências

### Adicionar nova dependência

```bash
# Edite pyproject.toml
# [project]
# dependencies = [
#     "nova-lib==1.0.0",
# ]

# Reinstale
pip install -e ".[dev]"

# Ou adicione diretamente com pip
pip install nova-lib
```

## 🐳 Docker

```bash
# Build
docker build -f Dockerfile -t vlab-api:latest .

# Run
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@localhost/vlab_fuel \
  vlab-api:latest

# Ou com docker-compose
docker-compose -f docker/docker-compose.yml up
```

## 🔄 Migrations

```bash
# Criar migration automática
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrations
make db-upgrade

# Reverter última migration
make db-downgrade
```

## 🔐 Segurança

- Nunca commite `.env` (já está no .gitignore)
- Use `API_KEY` forte em produção
- Valide todas as inputs com Pydantic
- Use HTTPS em produção

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Alembic](https://alembic.sqlalchemy.org/)

## ❓ FAQ

### P: Como debugar?

```python
# Use breakpoints no VSCode
import pdb; pdb.set_trace()

# Ou use o debugger do pytest
pytest -vv --pdb
```

### P: Como ver logs?

```bash
# Aumente o LOG_LEVEL em .env
LOG_LEVEL=DEBUG

# Ou por container
docker-compose -f docker/docker-compose.yml logs -f api
```

### P: Como resetar o banco?

```bash
# Com docker
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up

# Ou manualmente
dropdb vlab_fuel
createdb vlab_fuel
alembic upgrade head
```

---

**Happy coding! 🚀**
