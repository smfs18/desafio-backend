"""Abastecimento service with business logic"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.abastecimento import Abastecimento
from app.domain.models.enums import StatusAbastecimento
from app.repositories.abastecimento_repository import AbastecimentoRepository
from app.services.anomaly_service import AnomalyService


class AbastecimentoService:
    """Service for managing abastecimentos with business rules"""

    def __init__(self, session: AsyncSession):
        """Initialize service with database session"""
        self.session = session
        self.repository = AbastecimentoRepository(session)
        self.anomaly_service = AnomalyService()

    async def create_abastecimento(
        self,
        motorista_id: int,
        tipo_combustivel: str,
        valor: float,
        litros: float,
    ) -> Abastecimento:
        """
        Create a new abastecimento with anomaly detection.

        Business logic:
        - If anomaly detected: status = ANOMALIA
        - Otherwise: status = PENDENTE

        Args:
            motorista_id: ID of the driver
            tipo_combustivel: Type of fuel
            valor: Value of refill
            litros: Liters refilled

        Returns:
            Created Abastecimento object
        """
        # Create abastecimento with pending status
        abastecimento = Abastecimento(
            motorista_id=motorista_id,
            tipo_combustivel=tipo_combustivel,
            valor=valor,
            litros=litros,
            status=StatusAbastecimento.PENDENTE,
        )

        # Check for anomalies
        is_anomaly = self.anomaly_service.detect_anomaly(abastecimento)
        if is_anomaly:
            abastecimento.status = StatusAbastecimento.ANOMALIA
            abastecimento.eh_anomalia = True

        # Save to database
        return await self.repository.create(abastecimento)

    async def approve_abastecimento(self, abastecimento_id: int) -> Abastecimento | None:
        """Approve an abastecimento"""
        abastecimento = await self.repository.get_by_id(abastecimento_id)
        if not abastecimento:
            return None

        abastecimento.status = StatusAbastecimento.APROVADO
        return await self.repository.update(abastecimento)

    async def reject_abastecimento(
        self, abastecimento_id: int, motivo: str
    ) -> Abastecimento | None:
        """Reject an abastecimento"""
        abastecimento = await self.repository.get_by_id(abastecimento_id)
        if not abastecimento:
            return None

        abastecimento.status = StatusAbastecimento.RECUSADO
        abastecimento.motivo_recusa = motivo
        return await self.repository.update(abastecimento)
