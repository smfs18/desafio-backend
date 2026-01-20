"""Pytest configuration and fixtures"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_session
from app.domain.models import Abastecimento, Motorista  # noqa: F401
from app.main import app


@pytest.fixture
async def test_db():
    """Create a test database"""
    # Use in-memory SQLite for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def test_session(test_db):
    """Create a test session"""
    async_session_maker = sessionmaker(
        test_db,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with async_session_maker() as session:
        yield session


@pytest.fixture
def test_client(test_session):
    """Create a test client with test session"""
    def override_get_session():
        return test_session

    app.dependency_overrides[get_session] = override_get_session
    
    from fastapi.testclient import TestClient
    return TestClient(app)
