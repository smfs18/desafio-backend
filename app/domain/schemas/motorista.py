"""Motorista schemas for API requests and responses"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class MotoristaBase(BaseModel):
    """Base schema for Motorista"""

    nome: str = Field(..., min_length=1, max_length=255, description="Nome do motorista")
    cpf: str = Field(..., min_length=11, max_length=11, description="CPF do motorista")
    email: EmailStr = Field(..., description="Email do motorista")
    telefone: str | None = Field(None, max_length=20, description="Telefone do motorista")


class MotoristaCreate(MotoristaBase):
    """Schema for creating a new Motorista"""

    pass


class MotoristaUpdate(BaseModel):
    """Schema for updating a Motorista"""

    nome: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = Field(None)
    telefone: str | None = Field(None, max_length=20)
    ativo: bool | None = Field(None)


class MotoristaResponse(MotoristaBase):
    """Schema for Motorista response"""

    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
