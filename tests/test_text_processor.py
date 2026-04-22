"""Tests for text processing"""

import pytest
from src.pipeline.text_processor import TextProcessor


class TestTextProcessor:
    """Test TextProcessor class"""

    def test_validate_commentary_valid(self):
        """Test validation of valid commentary"""
        text = "This is a valid volleyball commentary with many words about player performance."
        assert TextProcessor.validate_commentary(text) is True

    def test_validate_commentary_empty(self):
        """Test validation of empty commentary"""
        assert TextProcessor.validate_commentary("") is False
        assert TextProcessor.validate_commentary(None) is False

    def test_validate_commentary_too_short(self):
        """Test validation of too short commentary"""
        text = "Short text"  # Less than 10 words
        assert TextProcessor.validate_commentary(text) is False

    def test_clean_text(self):
        """Test text cleaning"""
        text = "  Hello   world  !  "
        cleaned = TextProcessor.clean_text(text)
        assert cleaned == "Hello world !"
        assert "  " not in cleaned

    def test_clean_text_duplicate_punctuation(self):
        """Test removal of duplicate punctuation"""
        text = "Hello!!! World???"
        cleaned = TextProcessor.clean_text(text)
        assert "!!!" not in cleaned
        assert "???" not in cleaned

    def test_normalize_text(self):
        """Test text normalization"""
        text = "  HELLO   WORLD  "
        normalized = TextProcessor.normalize_text(text, lowercase=True)
        assert normalized == "hello world"

    def test_extract_sentences(self):
        """Test sentence extraction"""
        text = "First sentence. Second sentence! Third sentence?"
        sentences = TextProcessor.extract_sentences(text)
        assert len(sentences) == 3
        assert "First sentence" in sentences

    def test_extract_player_names(self):
        """Test player name extraction"""
        text = "Dupont played well. Player 7 had great defense. Martin made good passes."
        names = TextProcessor.extract_player_names(text)
        assert "Dupont" in names or "Martin" in names
        assert "7" in names

    def test_get_text_stats(self):
        """Test text statistics"""
        text = "This is a test. This is another test."
        stats = TextProcessor.get_text_stats(text)
        assert stats["word_count"] > 0
        assert stats["sentence_count"] > 0
        assert stats["character_count"] > 0
        assert stats["avg_word_length"] > 0
