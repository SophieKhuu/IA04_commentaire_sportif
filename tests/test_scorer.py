"""Tests for scoring logic"""

import pytest
from src.models.schemas import CriteriaScore
from src.pipeline.scorer import Scorer


class TestScorer:
    """Test Scorer class"""

    def test_calculate_final_score_default_weights(self, sample_criteria_score):
        """Test final score calculation with default weights"""
        score = Scorer.calculate_final_score(sample_criteria_score)
        assert 0 <= score <= 100
        assert isinstance(score, float)

    def test_calculate_final_score_custom_weights(self, sample_criteria_score):
        """Test final score calculation with custom weights"""
        weights = {
            "technique": 0.3,
            "defense": 0.3,
            "attitude": 0.2,
            "physique": 0.1,
            "decision_tactique": 0.05,
            "autre": 0.05,
        }
        score = Scorer.calculate_final_score(sample_criteria_score, weights)
        assert 0 <= score <= 100

    def test_calculate_final_score_all_perfect(self):
        """Test final score with all perfect scores"""
        criteria = CriteriaScore(
            technique=100,
            defense=100,
            attitude=100,
            physique=100,
            decision_tactique=100,
            autre=100,
        )
        score = Scorer.calculate_final_score(criteria)
        assert score == 100.0

    def test_calculate_final_score_all_zero(self):
        """Test final score with all zero scores"""
        criteria = CriteriaScore(
            technique=0,
            defense=0,
            attitude=0,
            physique=0,
            decision_tactique=0,
            autre=0,
        )
        score = Scorer.calculate_final_score(criteria)
        assert score == 0.0

    def test_get_rating_category(self):
        """Test rating category classification"""
        assert Scorer.get_rating_category(95) == "Exceptionnel"
        assert Scorer.get_rating_category(85) == "Excellent"
        assert Scorer.get_rating_category(75) == "Bon"
        assert Scorer.get_rating_category(65) == "Satisfaisant"
        assert Scorer.get_rating_category(55) == "Acceptable"
        assert Scorer.get_rating_category(30) == "Faible"

    def test_get_score_color(self):
        """Test score color mapping"""
        color = Scorer.get_score_color(95)
        assert color == "#006400"  # Dark green

        color = Scorer.get_score_color(85)
        assert color == "#228B22"  # Forest green

        color = Scorer.get_score_color(30)
        assert color == "#DC143C"  # Crimson red
