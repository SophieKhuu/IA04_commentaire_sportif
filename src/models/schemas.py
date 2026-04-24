"""
Pydantic data models for volleyball commentary analysis
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class CriteriaScore(BaseModel):
    """Individual criterion score for a player (0-20 scale)"""

    technique: float = Field(..., ge=0, le=20, description="Technical skill 0-20")
    defense: float = Field(..., ge=0, le=20, description="Defensive capability 0-20")
    attitude: float = Field(..., ge=0, le=20, description="Mental attitude 0-20")
    physique: float = Field(..., ge=0, le=20, description="Physical performance 0-20")
    decision_tactique: float = Field(
        ..., ge=0, le=20, description="Tactical decision-making 0-20"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "technique": 15.5,
                "defense": 16.0,
                "attitude": 17.0,
                "physique": 14.5,
                "decision_tactique": 16.5,
            }
        }


class PlayerRating(BaseModel):
    """Complete rating for a single player"""

    name: str = Field(..., description="Player name or identifier")
    number: Optional[str] = Field(None, description="Player jersey number")
    points: int = Field(default=0, description="Points scored")
    aces: int = Field(default=0, description="Aces")
    blocks: int = Field(default=0, description="Blocks")
    errors: int = Field(default=0, description="Errors committed")
    attacks_successful: int = Field(default=0, description="Successful attacks")
    attacks_attempted: int = Field(default=0, description="Attempted attacks")
    scores: CriteriaScore = Field(..., description="Individual criteria scores (0-20)")
    final_score: float = Field(..., ge=0, le=20, description="Average score 0-20")
    notes: str = Field(default="", description="Narrative summary of performance")
    facts: List[str] = Field(default_factory=list, description="Extracted key facts")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dupont",
                "number": "7",
                "points": 15,
                "aces": 2,
                "blocks": 3,
                "errors": 4,
                "attacks_successful": 18,
                "attacks_attempted": 25,
                "scores": {
                    "technique": 15.5,
                    "defense": 16.0,
                    "attitude": 17.0,
                    "physique": 14.5,
                    "decision_tactique": 16.5,
                },
                "final_score": 15.9,
                "notes": "Excellent defenseur avec bonne attitude",
                "facts": ["2 blocks", "10 passes réussies"],
            }
        }

    @validator("final_score")
    def validate_final_score(cls, v):
        """Ensure final score is in valid range"""
        if not (0 <= v <= 20):
            raise ValueError("Final score must be between 0 and 20")
        return v


class AnalysisResult(BaseModel):
    """Complete analysis result for a commentary"""

    commentary: str = Field(..., description="Original commentary text")
    summary: str = Field(..., description="AI-generated summary of key points")
    players: List[PlayerRating] = Field(
        ..., description="List of player ratings extracted"
    )
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis time")
    model_used: str = Field(default="mixtral-8x7b-32768", description="LLM model used")
    source_type: str = Field(
        default="text", description="Source type: 'text', 'audio', etc."
    )
    processing_time_seconds: float = Field(default=0.0, description="Processing duration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "commentary": "Dupont a fait un excellent match...",
                "summary": "Performance exceptionnelle de Dupont avec bon jeu défensif",
                "players": [],
                "timestamp": "2024-04-22T10:30:00",
                "model_used": "mixtral-8x7b-32768",
                "source_type": "text",
                "processing_time_seconds": 3.45,
                "metadata": {},
            }
        }


class ExportResult(BaseModel):
    """Format for exporting results to CSV/JSON"""

    player_name: str
    player_number: Optional[str]
    technique: int
    defense: int
    attitude: int
    physique: int
    decision_tactique: int
    autre: int
    final_score: float
    notes: str
    timestamp: str
