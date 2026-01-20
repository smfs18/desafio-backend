"""Abastecimento endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.models.enums import StatusAbastecimento
from app.domain.schemas.abastecimento import (
    AbastecimentoCreate,
    AbastecimentoListResponse,
    AbastecimentoResponse,
)
from app.repositories.abastecimento_repository import AbastecimentoRepository
from app.repositories.motorista_repository import MotoristaRepository
from app.services.abastecimento_service import AbastecimentoService

router = APIRouter(prefix="/api/v1/abastecimentos", tags=["abastecimentos"])


@router.post(
    "",
    response_model=AbastecimentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo abastecimento",
)
async def create_abastecimento(
    abastecimento: AbastecimentoCreate,
    session: AsyncSession = Depends(get_session),
) -> AbastecimentoResponse:
    """
    Create a new abastecimento with anomaly detection.

    Args:
        abastecimento: Abastecimento data
        session: Database session

    Returns:
        Created abastecimento

    Raises:
        HTTPException: If motorista not found or data is invalid
    """
    # Verify motorista exists
    motorista_repo = MotoristaRepository(session)
    motorista = await motorista_repo.get_by_id(abastecimento.motorista_id)
    if not motorista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorista não encontrado",
        )

    # Create abastecimento with business logic
    service = AbastecimentoService(session)
    created = await service.create_abastecimento(
        motorista_id=abastecimento.motorista_id,
        tipo_combustivel=abastecimento.tipo_combustivel,
        valor=abastecimento.valor,
        litros=abastecimento.litros,
    )

    return AbastecimentoResponse.model_validate(created)


@router.get(
    "/{abastecimento_id}",
    response_model=AbastecimentoResponse,
    summary="Obter abastecimento por ID",
)
async def get_abastecimento(
    abastecimento_id: int,
    session: AsyncSession = Depends(get_session),
) -> AbastecimentoResponse:
    """
    Get abastecimento by ID.

    Args:
        abastecimento_id: Abastecimento ID
        session: Database session

    Returns:
        Abastecimento data

    Raises:
        HTTPException: If abastecimento not found
    """
    repository = AbastecimentoRepository(session)
    abastecimento = await repository.get_by_id(abastecimento_id)

    if not abastecimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abastecimento não encontrado",
        )

    return AbastecimentoResponse.model_validate(abastecimento)


@router.get(
    "",
    response_model=AbastecimentoListResponse,
    summary="Listar abastecimentos",
)
async def list_abastecimentos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: StatusAbastecimento | None = Query(None),
    motorista_id: int | None = Query(None),
    session: AsyncSession = Depends(get_session),
) -> AbastecimentoListResponse:
    """
    List abastecimentos with pagination and filters.

    Args:
        page: Page number (1-indexed)
        page_size: Items per page
        status_filter: Filter by status
        motorista_id: Filter by motorista ID
        session: Database session

    Returns:
        Paginated list of abastecimentos
    """
    repository = AbastecimentoRepository(session)

    if motorista_id:
        # Get abastecimentos for specific motorista
        items = await repository.get_by_motorista_id(motorista_id)
        total = len(items)
    elif status_filter:
        # Get abastecimentos by status
        items = await repository.get_by_status(status_filter)
        total = len(items)
    else:
        # Get all abastecimentos with pagination
        items, total = await repository.get_with_pagination(page, page_size)

    total_pages = (total + page_size - 1) // page_size

    return AbastecimentoListResponse(
        items=[AbastecimentoResponse.model_validate(item) for item in items],
        total=total,
        pagina=page,
        tamanho_pagina=page_size,
        total_paginas=total_pages,
    )


@router.post(
    "/{abastecimento_id}/approve",
    response_model=AbastecimentoResponse,
    summary="Aprovar abastecimento",
)
async def approve_abastecimento(
    abastecimento_id: int,
    session: AsyncSession = Depends(get_session),
) -> AbastecimentoResponse:
    """
    Approve an abastecimento.

    Args:
        abastecimento_id: Abastecimento ID
        session: Database session

    Returns:
        Updated abastecimento

    Raises:
        HTTPException: If abastecimento not found
    """
    service = AbastecimentoService(session)
    updated = await service.approve_abastecimento(abastecimento_id)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abastecimento não encontrado",
        )

    return AbastecimentoResponse.model_validate(updated)


@router.post(
    "/{abastecimento_id}/reject",
    response_model=AbastecimentoResponse,
    summary="Rejeitar abastecimento",
)
async def reject_abastecimento(
    abastecimento_id: int,
    motivo: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_session),
) -> AbastecimentoResponse:
    """
    Reject an abastecimento.

    Args:
        abastecimento_id: Abastecimento ID
        motivo: Reason for rejection
        session: Database session

    Returns:
        Updated abastecimento

    Raises:
        HTTPException: If abastecimento not found
    """
    service = AbastecimentoService(session)
    updated = await service.reject_abastecimento(abastecimento_id, motivo)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abastecimento não encontrado",
        )

    return AbastecimentoResponse.model_validate(updated)
