"""Anomaly detection service"""

from app.domain.models.abastecimento import Abastecimento


class AnomalyService:
    """Service for detecting anomalies in fuel refills"""

    ANOMALY_THRESHOLD = 0.25  # 25% threshold for anomaly detection

    @staticmethod
    def detect_anomaly(abastecimento: Abastecimento) -> bool:
        """
        Detect if an abastecimento is anomalous based on price per liter.

        An abastecimento is considered anomalous if the price per liter
        exceeds 25% of the average price for that fuel type.

        Args:
            abastecimento: Abastecimento object to analyze

        Returns:
            True if anomalous, False otherwise
        """
        if abastecimento.litros == 0:
            return False

        price_per_liter = abastecimento.valor / abastecimento.litros

        # For now, we use a simple threshold based on typical fuel prices
        # In a real scenario, this would compare against historical data
        # or use machine learning models

        # Typical threshold: ~R$ 6.50 per liter (adjusted for 25% threshold)
        # This is a placeholder - in production, you'd fetch from database
        normal_price_threshold = 8.12  # ~25% above R$ 6.50

        return price_per_liter > normal_price_threshold

    @staticmethod
    def get_anomaly_score(abastecimento: Abastecimento) -> float:
        """
        Calculate anomaly score for an abastecimento (0.0 to 1.0).

        Args:
            abastecimento: Abastecimento object to analyze

        Returns:
            Anomaly score between 0.0 (normal) and 1.0 (highly anomalous)
        """
        if abastecimento.litros == 0:
            return 0.0

        price_per_liter = abastecimento.valor / abastecimento.litros
        normal_price_threshold = 8.12

        if price_per_liter <= normal_price_threshold:
            score = (price_per_liter / normal_price_threshold) * 0.5
        else:
            score = 0.5 + ((price_per_liter - normal_price_threshold) / normal_price_threshold) * 0.5

        return min(score, 1.0)
