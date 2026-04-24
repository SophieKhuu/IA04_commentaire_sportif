"""
Scoring logic and calculations
"""

import logging
from typing import Dict

from src.models.schemas import CriteriaScore
from src.config import SCORING_CRITERIA

logger = logging.getLogger(__name__)


class Scorer:
    """Calculate player scores based on criteria"""

    @staticmethod
    def calculate_final_score(criteria: CriteriaScore, weights: Dict[str, float] = None) -> float:
        """
        Calculate average final score from individual criteria (0-20 scale)

        Args:
            criteria: CriteriaScore object with individual scores (0-20)
            weights: Optional - not used in new system (kept for backward compatibility)

        Returns:
            Average final score (0-20)
        """
        # Calculate simple average of 5 criteria
        final_score = (
            criteria.technique
            + criteria.defense
            + criteria.attitude
            + criteria.physique
            + criteria.decision_tactique
        ) / 5

        # Round to 1 decimal
        final_score = round(final_score, 1)

        logger.debug(
            f"Calculated final score: {final_score} "
            f"from T:{criteria.technique} D:{criteria.defense} "
            f"A:{criteria.attitude} P:{criteria.physique} "
            f"DT:{criteria.decision_tactique}"
        )

        return final_score

    @staticmethod
    def get_rating_category(score: float) -> str:
        """
        Categorize player performance based on final score (0-20 scale)

        Args:
            score: Final score (0-20)

        Returns:
            Performance category string
        """
        if score >= 18:
            return "Exceptionnel"
        elif score >= 16:
            return "Excellent"
        elif score >= 14:
            return "Bon"
        elif score >= 12:
            return "Satisfaisant"
        elif score >= 10:
            return "Acceptable"
        else:
            return "Faible"

    @staticmethod
    def get_score_color(score: float) -> str:
        """
        Get color code for visualization based on score (0-20 scale)

        Args:
            score: Final score (0-20)

        Returns:
            Color code (hex)
        """
        if score >= 18:
            return "#006400"  # Dark green
        elif score >= 16:
            return "#228B22"  # Forest green
        elif score >= 14:
            return "#FFD700"  # Gold
        elif score >= 12:
            return "#FF8C00"  # Orange
        else:
            return "#DC143C"  # Crimson red
