"""
Text preprocessing and validation
"""

import logging
import re
from typing import Optional

from src.config import MIN_COMMENTARY_LENGTH, MAX_COMMENTARY_LENGTH

logger = logging.getLogger(__name__)


class TextProcessor:
    """Text cleaning, validation, and preprocessing"""

    @staticmethod
    def validate_commentary(text: str) -> bool:
        """
        Validate commentary length and basic structure

        Args:
            text: Commentary text to validate

        Returns:
            True if valid, False otherwise
        """
        if not text or not isinstance(text, str):
            logger.warning("Commentary is empty or not a string")
            return False

        # Count words
        word_count = len(text.split())

        if word_count < MIN_COMMENTARY_LENGTH:
            logger.warning(
                f"Commentary too short: {word_count} words "
                f"(minimum: {MIN_COMMENTARY_LENGTH})"
            )
            return False

        if word_count > MAX_COMMENTARY_LENGTH:
            logger.warning(
                f"Commentary too long: {word_count} words "
                f"(maximum: {MAX_COMMENTARY_LENGTH})"
            )
            return False

        return True

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Strip leading/trailing whitespace
        text = text.strip()

        # Remove duplicate punctuation
        text = re.sub(r"([.!?,;:])\1+", r"\1", text)

        logger.debug(f"Text cleaned: {len(text)} characters")
        return text

    @staticmethod
    def normalize_text(text: str, lowercase: bool = False) -> str:
        """
        Normalize text for processing

        Args:
            text: Text to normalize
            lowercase: Whether to convert to lowercase

        Returns:
            Normalized text
        """
        text = TextProcessor.clean_text(text)

        if lowercase:
            text = text.lower()

        return text

    @staticmethod
    def extract_sentences(text: str) -> list:
        """
        Extract sentences from text

        Args:
            text: Text to process

        Returns:
            List of sentences
        """
        # Simple sentence splitting on . ! ?
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    @staticmethod
    def extract_player_names(text: str) -> list:
        """
        Extract potential player names/numbers from text

        Simple heuristic: capitalized words or numbers

        Args:
            text: Text to search

        Returns:
            List of potential player identifiers
        """
        # Look for patterns like "Dupont", "Player 7", "numéro 10", etc.
        patterns = [
            r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?",  # Capitalized names
            r"(?:joueur|player|numéro|n°)\s+(\d+)",  # Player numbers
            r"(?:n°|#)(\d+)",  # Jersey numbers
        ]

        names = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            names.update(matches)

        return list(names)

    @staticmethod
    def get_text_stats(text: str) -> dict:
        """
        Get statistics about text

        Args:
            text: Text to analyze

        Returns:
            Dictionary with text statistics
        """
        words = text.split()
        sentences = TextProcessor.extract_sentences(text)

        return {
            "word_count": len(words),
            "character_count": len(text),
            "sentence_count": len(sentences),
            "avg_word_length": (
                sum(len(w) for w in words) / len(words) if words else 0
            ),
            "avg_sentence_length": (
                sum(len(s.split()) for s in sentences) / len(sentences)
                if sentences
                else 0
            ),
        }
