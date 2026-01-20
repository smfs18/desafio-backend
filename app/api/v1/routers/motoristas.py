"""Motorista endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.schemas.motorista import (
    MotoristaCreate,
    MotoristaResponse,
    MotoristaUpdate,
)
from app.domain.validators.cpf import validate_cpf
from app.repositories.motorista_repository import MotoristaRepository

router = APIRouter(prefix="/api/v1/motoristas", tags=["motoristas"])


@router.post(
    "",
    response_model=MotoristaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo motorista",
)
async def create_motorista(
    motorista: MotoristaCreate,
    session: AsyncSession = Depends(get_session),
) -> MotoristaResponse:
    """
    Create a new motorista.

    Args:
        motorista: Motorista data
        session: Database session

    Returns:
        Created motorista

    Raises:
        HTTPException: If CPF is invalid or already exists
    """
    # Validate CPF
    if not validate_cpf(motorista.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido",
        )

    # Check if motorista already exists
    repository = MotoristaRepository(session)
    existing = await repository.get_by_cpf(motorista.cpf)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Motorista com este CPF já existe",
        )

    # Create motorista
    from app.domain.models.motorista import Motorista

    new_motorista = Motorista(
        nome=motorista.nome,
        cpf=motorista.cpf,
        email=motorista.email,
        telefone=motorista.telefone,
    )

    created = await repository.create(new_motorista)
    return MotoristaResponse.model_validate(created)


@router.get(
    "/{motorista_id}",
    response_model=MotoristaResponse,
    summary="Obter motorista por ID",
)
async def get_motorista(
    motorista_id: int,
    session: AsyncSession = Depends(get_session),
) -> MotoristaResponse:
    """
    Get motorista by ID.

    Args:
        motorista_id: Motorista ID
        session: Database session

    Returns:
        Motorista data

    Raises:
        HTTPException: If motorista not found
    """
    repository = MotoristaRepository(session)
    motorista = await repository.get_by_id(motorista_id)

    if not motorista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorista não encontrado",
        )

    return MotoristaResponse.model_validate(motorista)


@router.get(
    "",
    summary="Listar motoristas",
)
async def list_motoristas(
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    List motoristas with pagination.

    Args:
        page: Page number (1-indexed)
        page_size: Items per page
        session: Database session

    Returns:
        Paginated list of motoristas
    """
    repository = MotoristaRepository(session)
    items, total = await repository.get_with_pagination(page, page_size)

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": [MotoristaResponse.model_validate(item) for item in items],
        "total": total,
        "pagina": page,
        "tamanho_pagina": page_size,
        "total_paginas": total_pages,
    }


@router.patch(
    "/{motorista_id}",
    response_model=MotoristaResponse,
    summary="Atualizar motorista",
)
async def update_motorista(
    motorista_id: int,
    motorista_update: MotoristaUpdate,
    session: AsyncSession = Depends(get_session),
) -> MotoristaResponse:
    """
    Update motorista.

    Args:
        motorista_id: Motorista ID
        motorista_update: Update data
        session: Database session

    Returns:
        Updated motorista

    Raises:
        HTTPException: If motorista not found
    """
    repository = MotoristaRepository(session)
    motorista = await repository.get_by_id(motorista_id)

    if not motorista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Motorista não encontrado",
        )

    # Update fields
    update_data = motorista_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(motorista, field, value)

    updated = await repository.update(motorista)
    return MotoristaResponse.model_validate(updated)
