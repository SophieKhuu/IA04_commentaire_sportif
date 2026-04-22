"""Tests for Pydantic models"""

import pytest
from datetime import datetime
from src.models.schemas import (
    CriteriaScore,
    PlayerRating,
    AnalysisResult,
    ExportResult,
)


class TestCriteriaScore:
    """Test CriteriaScore model"""

    def test_valid_criteria_score(self, sample_criteria_score):
        """Test creating valid criteria score"""
        assert sample_criteria_score.technique == 75
        assert sample_criteria_score.defense == 80
        assert sample_criteria_score.attitude == 85

    def test_criteria_score_boundaries(self):
        """Test score boundaries (0-100)"""
        # Valid: boundary values
        score = CriteriaScore(
            technique=0,
            defense=100,
            attitude=50,
            physique=50,
            decision_tactique=50,
            autre=50,
        )
        assert score.technique == 0
        assert score.defense == 100

        # Invalid: out of range
        with pytest.raises(ValueError):
            CriteriaScore(
                technique=101,
                defense=50,
                attitude=50,
                physique=50,
                decision_tactique=50,
                autre=50,
            )

    def test_criteria_score_json(self, sample_criteria_score):
        """Test JSON serialization"""
        json_data = sample_criteria_score.model_dump_json()
        assert "technique" in json_data
        assert "defense" in json_data


class TestPlayerRating:
    """Test PlayerRating model"""

    def test_valid_player_rating(self, sample_player_rating):
        """Test creating valid player rating"""
        assert sample_player_rating.name == "Dupont"
        assert sample_player_rating.number == "7"
        assert sample_player_rating.final_score == 76.5

    def test_player_rating_final_score_validation(self, sample_criteria_score):
        """Test final score validation"""
        # Valid
        rating = PlayerRating(
            name="Test",
            scores=sample_criteria_score,
            final_score=75.5,
        )
        assert rating.final_score == 75.5

        # Invalid
        with pytest.raises(ValueError):
            PlayerRating(
                name="Test",
                scores=sample_criteria_score,
                final_score=150,  # Out of range
            )

    def test_player_rating_optional_fields(self, sample_criteria_score):
        """Test optional fields"""
        rating = PlayerRating(
            name="Test",
            scores=sample_criteria_score,
            final_score=75.0,
        )
        assert rating.number is None
        assert rating.notes == ""
        assert rating.facts == []


class TestAnalysisResult:
    """Test AnalysisResult model"""

    def test_valid_analysis_result(self, sample_player_rating):
        """Test creating valid analysis result"""
        result = AnalysisResult(
            commentary="Test commentary",
            summary="Test summary",
            players=[sample_player_rating],
        )
        assert result.commentary == "Test commentary"
        assert len(result.players) == 1
        assert isinstance(result.timestamp, datetime)

    def test_analysis_result_empty_players(self):
        """Test analysis result with no players"""
        result = AnalysisResult(
            commentary="Test",
            summary="Summary",
            players=[],
        )
        assert len(result.players) == 0
