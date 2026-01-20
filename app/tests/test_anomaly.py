"""Tests for anomaly detection"""

import pytest

from app.domain.models.abastecimento import Abastecimento
from app.domain.models.enums import StatusAbastecimento, TipoCombustivel
from app.services.anomaly_service import AnomalyService


class TestAnomalyDetection:
    """Test anomaly detection logic"""

    def test_normal_abastecimento_is_not_anomaly(self):
        """Test that normal fuel refill is not detected as anomaly"""
        abastecimento = Abastecimento(
            motorista_id=1,
            tipo_combustivel=TipoCombustivel.GASOLINA,
            valor=250.00,  # R$ 6.25/liter (normal)
            litros=40.0,
            status=StatusAbastecimento.PENDENTE,
        )

        is_anomaly = AnomalyService.detect_anomaly(abastecimento)
        assert is_anomaly is False

    def test_expensive_abastecimento_is_anomaly(self):
        """Test that expensive fuel refill is detected as anomaly"""
        abastecimento = Abastecimento(
            motorista_id=1,
            tipo_combustivel=TipoCombustivel.GASOLINA,
            valor=600.00,  # R$ 30/liter (way too high - 25% above normal)
            litros=20.0,
            status=StatusAbastecimento.PENDENTE,
        )

        is_anomaly = AnomalyService.detect_anomaly(abastecimento)
        assert is_anomaly is True

    def test_anomaly_score_calculation(self):
        """Test anomaly score calculation"""
        # Normal price
        normal_abastecimento = Abastecimento(
            motorista_id=1,
            tipo_combustivel=TipoCombustivel.DIESEL,
            valor=200.00,
            litros=40.0,
        )

        score_normal = AnomalyService.get_anomaly_score(normal_abastecimento)
        assert 0.0 <= score_normal <= 0.5  # Should be in lower range

        # High price
        high_price_abastecimento = Abastecimento(
            motorista_id=1,
            tipo_combustivel=TipoCombustivel.GASOLINA,
            valor=600.00,
            litros=20.0,
        )

        score_high = AnomalyService.get_anomaly_score(high_price_abastecimento)
        assert 0.5 <= score_high <= 1.0  # Should be in higher range
        assert score_high > score_normal

    def test_zero_liters_no_anomaly(self):
        """Test that zero liters doesn't cause error"""
        abastecimento = Abastecimento(
            motorista_id=1,
            tipo_combustivel=TipoCombustivel.GASOLINA,
            valor=250.00,
            litros=0.0,  # Edge case
        )

        is_anomaly = AnomalyService.detect_anomaly(abastecimento)
        assert is_anomaly is False

        score = AnomalyService.get_anomaly_score(abastecimento)
        assert score == 0.0
