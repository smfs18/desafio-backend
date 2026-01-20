"""Health check endpoint"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health Check")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Status of the API
    """
    return {"status": "healthy"}
