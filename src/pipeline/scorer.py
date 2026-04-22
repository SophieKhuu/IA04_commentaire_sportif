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
        Calculate weighted final score from individual criteria

        Args:
            criteria: CriteriaScore object with individual scores
            weights: Optional custom weights dict. If None, uses config defaults.

        Returns:
            Weighted final score (0-100)
        """
        if weights is None:
            weights = {
                "technique": SCORING_CRITERIA["technique"]["weight"],
                "defense": SCORING_CRITERIA["defense"]["weight"],
                "attitude": SCORING_CRITERIA["attitude"]["weight"],
                "physique": SCORING_CRITERIA["physique"]["weight"],
                "decision_tactique": SCORING_CRITERIA["decision_tactique"]["weight"],
                "autre": SCORING_CRITERIA["autre"]["weight"],
            }

        # Verify weights sum to approximately 1.0
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            logger.warning(
                f"Weights don't sum to 1.0 (sum={total_weight}), normalizing"
            )
            # Normalize weights
            weights = {k: v / total_weight for k, v in weights.items()}

        # Calculate weighted score
        final_score = (
            criteria.technique * weights.get("technique", 0)
            + criteria.defense * weights.get("defense", 0)
            + criteria.attitude * weights.get("attitude", 0)
            + criteria.physique * weights.get("physique", 0)
            + criteria.decision_tactique * weights.get("decision_tactique", 0)
            + criteria.autre * weights.get("autre", 0)
        )

        # Round to 1 decimal
        final_score = round(final_score, 1)

        logger.debug(
            f"Calculated final score: {final_score} "
            f"from T:{criteria.technique} D:{criteria.defense} "
            f"A:{criteria.attitude} P:{criteria.physique} "
            f"DT:{criteria.decision_tactique} O:{criteria.autre}"
        )

        return final_score

    @staticmethod
    def get_rating_category(score: float) -> str:
        """
        Categorize player performance based on final score

        Args:
            score: Final score (0-100)

        Returns:
            Performance category string
        """
        if score >= 90:
            return "Exceptionnel"
        elif score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Bon"
        elif score >= 60:
            return "Satisfaisant"
        elif score >= 50:
            return "Acceptable"
        else:
            return "Faible"

    @staticmethod
    def get_score_color(score: float) -> str:
        """
        Get color code for visualization based on score

        Args:
            score: Final score (0-100)

        Returns:
            Color code (hex or rgb)
        """
        if score >= 90:
            return "#006400"  # Dark green
        elif score >= 80:
            return "#228B22"  # Forest green
        elif score >= 70:
            return "#FFD700"  # Gold
        elif score >= 60:
            return "#FF8C00"  # Orange
        else:
            return "#DC143C"  # Crimson red
