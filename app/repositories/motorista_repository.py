"""Motorista repository for data access"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.motorista import Motorista
from app.repositories.base import BaseRepository


class MotoristaRepository(BaseRepository[Motorista]):
    """Repository for Motorista data access"""

    def __init__(self, session: AsyncSession):
        """Initialize repository"""
        super().__init__(session, Motorista)

    async def get_by_cpf(self, cpf: str) -> Motorista | None:
        """Get motorista by CPF"""
        query = select(self.model).where(self.model.cpf == cpf)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Motorista | None:
        """Get motorista by email"""
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_active(self, skip: int = 0, limit: int = 100) -> list[Motorista]:
        """Get all active motoristas"""
        query = (
            select(self.model)
            .where(self.model.ativo == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_pagination(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[Motorista], int]:
        """Get motoristas with pagination"""
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
