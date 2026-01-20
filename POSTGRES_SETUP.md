# 🐘 Guia de Instalação PostgreSQL

## Opção 1: Com Docker 

```bash
# 1. Inicie o PostgreSQL em um container
docker run --name vlab-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=vlab_fuel \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:16-alpine

# 2. Verifique se está rodando
docker ps

# 3. Pronto! O banco está acessível em localhost:5432
```

---

## Opção 2: Instalação Nativa no Ubuntu/Debian

### Passo 1: Instalar PostgreSQL

```bash
# Atualize os pacotes
sudo apt update

# Instale PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Verifique a versão
psql --version
```

### Passo 2: Iniciar o Serviço

```bash
# Inicie o PostgreSQL
sudo systemctl start postgresql

# Verifique o status
sudo systemctl status postgresql

# (Opcional) Para iniciar automaticamente na boot
sudo systemctl enable postgresql
```

### Passo 3: Acessar o PostgreSQL

```bash
# Acesse o psql (terminal do PostgreSQL)
sudo -u postgres psql

# Você verá o prompt: postgres=#
```

### Passo 4: Criar o Banco e o Usuário

```sql
-- Dentro do psql, execute:

-- Criar banco de dados
CREATE DATABASE vlab_fuel;

-- Criar usuário (se quiser usar um diferente)
CREATE USER vlab_user WITH PASSWORD 'your_password';

-- Dar permissões
ALTER ROLE vlab_user SET client_encoding TO 'utf8';
ALTER ROLE vlab_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE vlab_user SET default_transaction_deferrable TO on;
ALTER ROLE vlab_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE vlab_fuel TO vlab_user;

-- Sair
\q
```

### Passo 5: Testar Conexão

```bash
# Conecte ao banco
psql -U postgres -d vlab_fuel -h localhost

# Se conseguir, está funcionando! 🎉
# Saia com:
\q
```

---

## Opção 3: Instalação com Docker Compose 

Já temos um `docker-compose.yml` pronto no projeto! Basta usar:

```bash
# 1. Navigate para a pasta do projeto
cd /home/smfs/Documentos/desafio-backend

# 2. Inicie tudo
docker-compose -f docker/docker-compose.yml up -d

# 3. Aguarde o PostgreSQL ficar pronto
sleep 10

# 4. Verifique
docker-compose -f docker/docker-compose.yml ps
```

---

## 🔧 Configurar a Connection String

### Para Docker
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/vlab_fuel
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:password@localhost:5432/vlab_fuel
```

### Para Usuário Local
```
DATABASE_URL=postgresql://vlab_user:your_password@localhost:5432/vlab_fuel
DATABASE_URL_ASYNC=postgresql+asyncpg://vlab_user:your_password@localhost:5432/vlab_fuel
```

### Atualizar no `.env`
```bash
# Edite o arquivo .env
nano .env

# Ou use seu editor favorito
code .env
```

---

## ✅ Verificar Conexão

### Com psql (Cliente do PostgreSQL)

```bash
# Conexão local
psql -U postgres -d vlab_fuel -h localhost

# Ou se criou usuário diferente
psql -U vlab_user -d vlab_fuel -h localhost

# Dentro do psql, verifique as tabelas (depois das migrations)
\dt

# Ou liste os bancos
\l

# Saia
\q
```

### Com Python

```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="vlab_fuel",
        user="postgres",
        password="password"
    )
    print("✅ Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"❌ Erro: {e}")
```

### Com SQLAlchemy

```python
from sqlalchemy import create_engine, inspect

DATABASE_URL = "postgresql://postgres:password@localhost:5432/vlab_fuel"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        inspector = inspect(conn)
        print("✅ Conexão bem-sucedida!")
        print(f"Tabelas: {inspector.get_table_names()}")
except Exception as e:
    print(f"❌ Erro: {e}")
```

---

## 🐛 Troubleshooting

### Erro: "could not connect to server"

```bash
# Verifique se PostgreSQL está rodando
docker ps | grep postgres

# Ou (para instalação nativa)
sudo systemctl status postgresql

# Se não estiver rodando, inicie:
sudo systemctl start postgresql

# Ou com Docker:
docker-compose -f docker/docker-compose.yml up -d postgres
```

### Erro: "permission denied for user"

```bash
# Verifique a senha está correta no .env
# Default: password

# Se esqueceu, resete no Docker:
docker exec -it vlab-postgres psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'newpassword';"
```

### Erro: "database does not exist"

```bash
# Crie o banco
psql -U postgres -c "CREATE DATABASE vlab_fuel;"

# Ou use as migrations do projeto (automático)
make db-upgrade
```

### Erro: "Port 5432 already in use"

```bash
# Se usar Docker, mude a porta:
docker run --name vlab-postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5433:5432 \
  -d postgres:16-alpine

# E atualize no .env:
DATABASE_URL=postgresql://postgres:password@localhost:5433/vlab_fuel
```

---

## 📊 Próximos Passos

Depois de ter o PostgreSQL rodando:

### 1. Instale as dependências Python

```bash
cd /home/smfs/Documentos/desafio-backend
pip install -e .
```

### 2. Execute as Migrations

```bash
# Cria as tabelas automaticamente
alembic upgrade head

# Ou se usar o Makefile
make db-upgrade
```

### 3. Carregue dados iniciais (opcional)

```bash
python scripts/load_data.py
# Ou
make load-data
```

### 4. Inicie a API

```bash
make run
# Ou
uvicorn app.main:app --reload
```

### 5. Acesse a documentação

Abra: http://localhost:8000/docs

---

## 🎯 Resumo Rápido (5 minutos)

```bash
# 1. Inicie PostgreSQL com Docker
docker run --name vlab-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=vlab_fuel \
  -p 5432:5432 \
  -d postgres:16-alpine

# 2. Aguarde 5 segundos
sleep 5

# 3. Clone o projeto (se não tiver)
cd /home/smfs/Documentos/desafio-backend

# 4. Instale Python deps
pip install -e .

# 5. Execute migrations
alembic upgrade head

# 6. Inicie a API
uvicorn app.main:app --reload

# 7. Acesse
open http://localhost:8000/docs
```

---

**Dúvidas? Me avisa! 🚀**
