"""FastAPI application factory"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import abastecimentos, health, motoristas
from app.core.config import settings
from app.core.database import dispose_db, init_db
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting up application")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down application")
    await dispose_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="V-Lab Fuel Gateway API - Backend Challenge",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router)
    app.include_router(motoristas.router)
    app.include_router(abastecimentos.router)

    logger.info(f"Application configured - Environment: {settings.environment}")

    return app


app = create_app()
