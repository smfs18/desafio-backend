"""Enums for domain models"""

from enum import Enum


class StatusAbastecimento(str, Enum):
    """Status of a fuel refill"""
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    ANOMALIA = "anomalia"


class TipoCombustivel(str, Enum):
    """Types of fuel"""
    GASOLINA = "gasolina"
    DIESEL = "diesel"
    ETANOL = "etanol"
    GNV = "gnv"
