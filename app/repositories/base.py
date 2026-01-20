"""Base repository with common CRUD operations"""

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, session: AsyncSession, model: type[T]):
        """Initialize repository"""
        self.session = session
        self.model = model

    async def create(self, obj: T) -> T:
        """Create a new object"""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, obj_id: int) -> T | None:
        """Get object by ID"""
        return await self.session.get(self.model, obj_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """Get all objects with pagination"""
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, obj: T) -> T:
        """Update an object"""
        await self.session.merge(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        """Delete an object"""
        obj = await self.get_by_id(obj_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False

    async def count(self) -> int:
        """Count all objects"""
        query = select(self.model)
        result = await self.session.execute(query)
        return len(result.scalars().all())
