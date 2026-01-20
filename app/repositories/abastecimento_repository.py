"""Abastecimento repository for data access"""

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.abastecimento import Abastecimento
from app.domain.models.enums import StatusAbastecimento
from app.repositories.base import BaseRepository


class AbastecimentoRepository(BaseRepository[Abastecimento]):
    """Repository for Abastecimento data access"""

    def __init__(self, session: AsyncSession):
        """Initialize repository"""
        super().__init__(session, Abastecimento)

    async def get_by_motorista_id(
        self, motorista_id: int, skip: int = 0, limit: int = 100
    ) -> list[Abastecimento]:
        """Get all abastecimentos for a specific driver"""
        query = (
            select(self.model)
            .where(self.model.motorista_id == motorista_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_status(
        self, status: StatusAbastecimento, skip: int = 0, limit: int = 100
    ) -> list[Abastecimento]:
        """Get all abastecimentos by status"""
        query = (
            select(self.model)
            .where(self.model.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_anomalies(self, skip: int = 0, limit: int = 100) -> list[Abastecimento]:
        """Get all anomalous abastecimentos"""
        query = (
            select(self.model)
            .where(self.model.eh_anomalia == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count_by_status(self, status: StatusAbastecimento) -> int:
        """Count abastecimentos by status"""
        query = select(func.count()).select_from(self.model).where(self.model.status == status)
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def count_anomalies(self) -> int:
        """Count anomalous abastecimentos"""
        query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.eh_anomalia == True)  # noqa: E712
        )
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_with_pagination(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[Abastecimento], int]:
        """Get abastecimentos with pagination"""
        skip = (page - 1) * page_size

        # Get total count
        count_query = select(func.count()).select_from(self.model)
        count_result = await self.session.execute(count_query)
        total = count_result.scalar() or 0

        # Get paginated results
        query = select(self.model).offset(skip).limit(page_size)
        result = await self.session.execute(query)
        items = result.scalars().all()

        return items, total
