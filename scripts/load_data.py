"""Script to load initial data into the database"""

import asyncio
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.domain.models.abastecimento import Abastecimento
from app.domain.models.enums import StatusAbastecimento, TipoCombustivel
from app.domain.models.motorista import Motorista


async def load_data() -> None:
    """Load initial data into the database"""
    # Create engine
    engine = create_async_engine(settings.database_url, echo=True)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    async with async_session() as session:
        # Create motoristas
        motoristas = [
            Motorista(
                nome="João Silva",
                cpf="12345678909",
                email="joao.silva@example.com",
                telefone="11999999999",
            ),
            Motorista(
                nome="Maria Santos",
                cpf="98765432100",
                email="maria.santos@example.com",
                telefone="21999999999",
            ),
            Motorista(
                nome="Pedro Oliveira",
                cpf="55555555555",
                email="pedro.oliveira@example.com",
                telefone="31999999999",
            ),
        ]

        for motorista in motoristas:
            session.add(motorista)

        await session.commit()

        print(f"✅ Created {len(motoristas)} motoristas")

        # Create abastecimentos
        now = datetime.utcnow()
        abastecimentos = [
            Abastecimento(
                motorista_id=1,
                tipo_combustivel=TipoCombustivel.GASOLINA,
                valor=250.00,
                litros=40.0,
                status=StatusAbastecimento.APROVADO,
                data_abastecimento=now - timedelta(days=5),
            ),
            Abastecimento(
                motorista_id=1,
                tipo_combustivel=TipoCombustivel.DIESEL,
                valor=450.00,
                litros=50.0,
                status=StatusAbastecimento.APROVADO,
                data_abastecimento=now - timedelta(days=3),
            ),
            Abastecimento(
                motorista_id=2,
                tipo_combustivel=TipoCombustivel.GASOLINA,
                valor=600.00,
                litros=20.0,  # High price per liter - anomaly
                status=StatusAbastecimento.ANOMALIA,
                eh_anomalia=True,
                data_abastecimento=now - timedelta(days=1),
            ),
            Abastecimento(
                motorista_id=3,
                tipo_combustivel=TipoCombustivel.ETANOL,
                valor=200.00,
                litros=35.0,
                status=StatusAbastecimento.APROVADO,
                data_abastecimento=now,
            ),
        ]

        for abastecimento in abastecimentos:
            session.add(abastecimento)

        await session.commit()

        print(f"✅ Created {len(abastecimentos)} abastecimentos")

    await engine.dispose()
    print("✅ Database loaded successfully!")


if __name__ == "__main__":
    asyncio.run(load_data())
