"""Abastecimento model"""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.domain.models.enums import StatusAbastecimento, TipoCombustivel


class Abastecimento(Base):
    """Abastecimento (Fuel Refill) model"""

    __tablename__ = "abastecimentos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    motorista_id: Mapped[int] = mapped_column(
        ForeignKey("motoristas.id"), nullable=False, index=True
    )
    tipo_combustivel: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    litros: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=StatusAbastecimento.PENDENTE,
        index=True,
    )
    motivo_recusa: Mapped[str | None] = mapped_column(String(500), nullable=True)
    eh_anomalia: Mapped[bool] = mapped_column(default=False, index=True)
    data_abastecimento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"<Abastecimento(id={self.id}, motorista_id={self.motorista_id}, status={self.status})>"
