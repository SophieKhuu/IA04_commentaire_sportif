"""Test configuration and fixtures"""

import pytest
from src.pipeline.llm_client import GroqLLMClient
from src.models.schemas import CriteriaScore, PlayerRating


@pytest.fixture
def sample_criteria_score():
    """Sample criteria score for testing"""
    return CriteriaScore(
        technique=75,
        defense=80,
        attitude=85,
        physique=78,
        decision_tactique=72,
        autre=70,
    )


@pytest.fixture
def sample_player_rating(sample_criteria_score):
    """Sample player rating for testing"""
    return PlayerRating(
        name="Dupont",
        number="7",
        scores=sample_criteria_score,
        final_score=76.5,
        notes="Good performance",
        facts=["2 blocks", "10 passes"],
    )


@pytest.fixture
def sample_llm_response():
    """Sample LLM response for testing"""
    return {
        "summary": "Excellent performance by the team",
        "players": [
            {
                "name": "Dupont",
                "number": "7",
                "technique": 75,
                "defense": 80,
                "attitude": 85,
                "physique": 78,
                "decision_tactique": 72,
                "autre": 70,
                "notes": "Excellent player",
                "facts": ["2 blocks", "10 passes"],
            }
        ],
    }
