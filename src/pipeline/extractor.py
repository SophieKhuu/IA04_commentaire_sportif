"""
JSON extraction and validation from LLM responses
"""

import logging
from typing import List, Dict, Any, Optional
from pydantic import ValidationError

from src.models.schemas import CriteriaScore, PlayerRating, AnalysisResult
from src.config import SCORING_CRITERIA, MAX_SCORE, MIN_SCORE

logger = logging.getLogger(__name__)


class ExtractionError(Exception):
    """Custom exception for extraction failures"""

    pass


class AnalysisExtractor:
    """Extract and validate structured data from LLM JSON responses"""

    @staticmethod
    def extract_player_ratings(
        llm_response: Dict[str, Any], summary: str, source_type: str = "text"
    ) -> List[PlayerRating]:
        """
        Extract player ratings from LLM JSON response

        Args:
            llm_response: Parsed JSON from LLM
            summary: AI-generated summary
            source_type: Type of source (text, audio, etc.)

        Returns:
            List of PlayerRating objects

        Raises:
            ExtractionError: If data validation fails
        """
        players_data = llm_response.get("players", [])

        if not isinstance(players_data, list):
            raise ExtractionError("Expected 'players' to be a list in LLM response")

        if len(players_data) == 0:
            logger.warning("No players extracted from commentary")
            return []

        player_ratings = []

        for player_data in players_data:
            try:
                # Extract player information
                name = player_data.get("name", "Unknown")
                number = player_data.get("number")
                notes = player_data.get("notes", "")
                facts = player_data.get("facts", [])
                
                # Extract concrete metrics
                points = int(player_data.get("points", 0))
                aces = int(player_data.get("aces", 0))
                blocks = int(player_data.get("blocks", 0))
                errors = int(player_data.get("errors", 0))
                attacks_successful = int(player_data.get("attacks_successful", 0))
                attacks_attempted = int(player_data.get("attacks_attempted", 0))

                # Validate and extract scores (0-20 scale)
                scores = CriteriaScore(
                    technique=AnalysisExtractor._validate_score(
                        player_data.get("scores", {}).get("technique", 10)
                    ),
                    defense=AnalysisExtractor._validate_score(
                        player_data.get("scores", {}).get("defense", 10)
                    ),
                    attitude=AnalysisExtractor._validate_score(
                        player_data.get("scores", {}).get("attitude", 10)
                    ),
                    physique=AnalysisExtractor._validate_score(
                        player_data.get("scores", {}).get("physique", 10)
                    ),
                    decision_tactique=AnalysisExtractor._validate_score(
                        player_data.get("scores", {}).get("decision_tactique", 10)
                    ),
                )

                # Calculate final score
                from src.pipeline.scorer import Scorer

                final_score = Scorer.calculate_final_score(scores)

                # Create PlayerRating
                player_rating = PlayerRating(
                    name=name,
                    number=number,
                    points=points,
                    aces=aces,
                    blocks=blocks,
                    errors=errors,
                    attacks_successful=attacks_successful,
                    attacks_attempted=attacks_attempted,
                    scores=scores,
                    final_score=final_score,
                    notes=notes,
                    facts=facts if isinstance(facts, list) else [],
                )

                player_ratings.append(player_rating)
                logger.info(f"Extracted rating for player: {name} (score: {final_score})")

            except (ValidationError, ValueError, KeyError) as e:
                logger.warning(f"Failed to extract player data: {str(e)}")
                logger.warning(f"Player data: {player_data}")
                continue

        return player_ratings

    @staticmethod
    def _validate_score(score: Any) -> float:
        """
        Validate and normalize score to 0-20 range

        Args:
            score: Score value (int, float, or string)

        Returns:
            Validated score as float

        Raises:
            ValueError: If score cannot be converted
        """
        try:
            # Convert to float first to handle various types
            numeric_score = float(score)

            # Clamp to valid range (0-20)
            if numeric_score < MIN_SCORE:
                logger.warning(
                    f"Score {numeric_score} below minimum {MIN_SCORE}, clamping"
                )
                numeric_score = MIN_SCORE
            elif numeric_score > MAX_SCORE:
                logger.warning(
                    f"Score {numeric_score} above maximum {MAX_SCORE}, clamping"
                )
                numeric_score = MAX_SCORE

            return round(numeric_score, 1)

        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid score value {score}: {str(e)}, using default 10")
            return 10.0

    @staticmethod
    def build_analysis_result(
        commentary: str,
        llm_response: Dict[str, Any],
        player_ratings: List[PlayerRating],
        processing_time: float,
        model_used: str = "mixtral-8x7b-32768",
        source_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AnalysisResult:
        """
        Build complete AnalysisResult from extracted data

        Args:
            commentary: Original commentary text
            llm_response: Parsed LLM response
            player_ratings: Extracted player ratings
            processing_time: Time taken for analysis
            model_used: Name of LLM model used
            source_type: Type of input source
            metadata: Additional metadata

        Returns:
            AnalysisResult object

        Raises:
            ExtractionError: If result validation fails
        """
        try:
            summary = llm_response.get("summary", "")

            if not summary:
                logger.warning("No summary in LLM response")
                summary = "Analysis completed but summary not available"

            result = AnalysisResult(
                commentary=commentary,
                summary=summary,
                players=player_ratings,
                model_used=model_used,
                source_type=source_type,
                processing_time_seconds=processing_time,
                metadata=metadata or {},
            )

            logger.info(
                f"Built AnalysisResult with {len(player_ratings)} players "
                f"in {processing_time:.2f}s"
            )
            return result

        except ValidationError as e:
            raise ExtractionError(f"Failed to validate analysis result: {str(e)}")
