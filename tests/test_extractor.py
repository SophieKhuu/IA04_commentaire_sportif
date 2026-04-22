"""Tests for extraction logic"""

import pytest
from src.pipeline.extractor import AnalysisExtractor


class TestAnalysisExtractor:
    """Test AnalysisExtractor class"""

    def test_validate_score_valid(self):
        """Test score validation with valid values"""
        assert AnalysisExtractor._validate_score(75) == 75
        assert AnalysisExtractor._validate_score(75.5) == 76  # Rounded
        assert AnalysisExtractor._validate_score("80") == 80

    def test_validate_score_boundaries(self):
        """Test score validation at boundaries"""
        assert AnalysisExtractor._validate_score(0) == 0
        assert AnalysisExtractor._validate_score(100) == 100

    def test_validate_score_out_of_range(self):
        """Test score validation with out of range values"""
        assert AnalysisExtractor._validate_score(-10) == 0  # Clamped to min
        assert AnalysisExtractor._validate_score(150) == 100  # Clamped to max

    def test_validate_score_invalid_type(self):
        """Test score validation with invalid types"""
        assert AnalysisExtractor._validate_score("invalid") == 50  # Default
        assert AnalysisExtractor._validate_score(None) == 50  # Default

    def test_extract_player_ratings(self, sample_llm_response):
        """Test player rating extraction from LLM response"""
        ratings = AnalysisExtractor.extract_player_ratings(
            sample_llm_response, "Summary", "text"
        )
        assert len(ratings) > 0
        assert ratings[0].name == "Dupont"
        assert ratings[0].number == "7"

    def test_extract_player_ratings_empty_players(self):
        """Test extraction with no players"""
        response = {"summary": "Summary", "players": []}
        ratings = AnalysisExtractor.extract_player_ratings(response, "Summary", "text")
        assert len(ratings) == 0

    def test_build_analysis_result(self, sample_llm_response, sample_player_rating):
        """Test building analysis result"""
        result = AnalysisExtractor.build_analysis_result(
            commentary="Test commentary",
            llm_response=sample_llm_response,
            player_ratings=[sample_player_rating],
            processing_time=2.5,
        )
        assert result.commentary == "Test commentary"
        assert len(result.players) == 1
        assert result.processing_time_seconds == 2.5
