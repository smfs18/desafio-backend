"""Abastecimento schemas for API requests and responses"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.models.enums import StatusAbastecimento, TipoCombustivel


class AbastecimentoBase(BaseModel):
    """Base schema for Abastecimento"""

    motorista_id: int = Field(..., description="ID do motorista")
    tipo_combustivel: TipoCombustivel = Field(..., description="Tipo de combustível")
    valor: float = Field(..., gt=0, description="Valor do abastecimento")
    litros: float = Field(..., gt=0, description="Litros abastecidos")


class AbastecimentoCreate(AbastecimentoBase):
    """Schema for creating a new Abastecimento"""

    pass


class AbastecimentoResponse(AbastecimentoBase):
    """Schema for Abastecimento response"""

    id: int
    status: StatusAbastecimento
    motivo_recusa: str | None
    eh_anomalia: bool
    data_abastecimento: datetime
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


class AbastecimentoListResponse(BaseModel):
    """Schema for paginated Abastecimento list"""

    items: list[AbastecimentoResponse]
    total: int
    pagina: int
    tamanho_pagina: int
    total_paginas: int
