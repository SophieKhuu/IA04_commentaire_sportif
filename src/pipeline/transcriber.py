"""
Whisper-based audio transcription
"""

import logging
import os
from pathlib import Path
from typing import Optional

import whisper

# from src.config import WHISPER_MODEL, WHISPER_DEVICE

WHISPER_MODEL="base"
WHISPER_DEVICE="cpu"

logger = logging.getLogger(__name__)


class WhisperTranscriber:
    """Whisper audio transcription with model caching"""

    _model_cache = {}  # Class-level cache for models

    def __init__(
        self,
        model_name: str = WHISPER_MODEL,
        device: str = WHISPER_DEVICE,
    ):
        """
        Initialize Whisper transcriber

        Args:
            model_name: Whisper model (tiny, base, small, medium, large)
            device: Device to use (cpu, cuda, etc.)
        """
        self.model_name = model_name
        self.device = device
        self.model = self._load_model(model_name, device)

        logger.info(f"Initialized Whisper transcriber with model: {model_name}")

    @classmethod
    def _load_model(cls, model_name: str, device: str):
        """
        Load Whisper model with caching

        Args:
            model_name: Model name
            device: Device to use

        Returns:
            Loaded model
        """
        cache_key = f"{model_name}_{device}"

        if cache_key not in cls._model_cache:
            logger.info(f"Loading Whisper model: {model_name} on {device}")
            model = whisper.load_model(model_name, device=device)
            cls._model_cache[cache_key] = model
            logger.info(f"Model loaded and cached")
        else:
            logger.info(f"Using cached Whisper model: {model_name}")

        return cls._model_cache[cache_key]

    @staticmethod
    def _validate_audio_file(audio_path: str) -> Path:
        """
        Validate audio file exists and is readable

        Args:
            audio_path: Path to audio file

        Returns:
            Path object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format not supported
        """
        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {audio_path}")

        supported_formats = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
        if path.suffix.lower() not in supported_formats:
            raise ValueError(
                f"Unsupported audio format: {path.suffix}. "
                f"Supported: {supported_formats}"
            )

        return path

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text

        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'fr', 'en'). If None, auto-detect.

        Returns:
            Transcribed text

        Raises:
            FileNotFoundError: If audio file not found
            ValueError: If transcription fails
        """
        try:
            path = self._validate_audio_file(audio_path)
            # path = Path(audio_path)
            logger.info(f"Transcribing audio: {audio_path}")

            # Transcribe
            result = self.model.transcribe(
                str(path),
                language=language,
                verbose=False,
            )

            transcribed_text = result.get("text", "").strip()

            if not transcribed_text:
                logger.warning(f"Transcription produced empty result")
                raise ValueError("Transcription produced empty result")

            logger.info(
                f"Transcription completed: {len(transcribed_text)} characters"
            )
            return transcribed_text

        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise

    def get_model_info(self) -> dict:
        """
        Get information about loaded model

        Returns:
            Dictionary with model info
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "cached_models": list(self._model_cache.keys()),
        }

transcriber = WhisperTranscriber()
transcriber.transcribe("c:\\Users\\zebri\\Documents\\GitHub\\IA04_commentaire_sportif\\data\\france_coree_du_sud.mp3")