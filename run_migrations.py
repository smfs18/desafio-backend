#!/usr/bin/env python3
"""Script para rodar migrations manualmente"""

import asyncio
from app.core.database import init_db


async def main():
    """Inicializar banco de dados"""
    print("🔄 Criando tabelas...")
    await init_db()
    print("✅ Tabelas criadas com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
