"""
Groq LLM client with retry logic and error handling
"""

import time
import logging
from typing import Optional
from groq import Groq

from src.config import (
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LLM_TIMEOUT,
    SYSTEM_PROMPT_VOLLEYBALL,
)

logger = logging.getLogger(__name__)


class GroqLLMClient:
    """Groq LLM client with exponential backoff retry logic"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = LLM_MODEL,
        temperature: float = LLM_TEMPERATURE,
        max_tokens: int = LLM_MAX_TOKENS,
        max_retries: int = 3,
        timeout: int = LLM_TIMEOUT,
    ):
        """
        Initialize Groq LLM client

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
            model: Model name (default: mixtral-8x7b-32768)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            max_retries: Number of retry attempts
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not provided and not found in environment variables"
            )

        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.timeout = timeout

        logger.info(f"Initialized Groq client with model: {self.model}")

    def _format_prompt(self, commentary: str) -> str:
        """Format the input commentary as a user prompt"""
        return f"""Analysez ce commentaire sportif de volleyball et extrayez les informations:

{commentary}

Répondez UNIQUEMENT en JSON valide."""

    def analyze_commentary(self, commentary: str) -> str:
        """
        Analyze volleyball commentary using Groq LLM with retry logic

        Args:
            commentary: Text commentary to analyze

        Returns:
            JSON string with extracted analysis

        Raises:
            ValueError: If analysis fails after retries
        """
        if not commentary or not commentary.strip():
            raise ValueError("Commentary cannot be empty")

        prompt = self._format_prompt(commentary)
        last_error = None

        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"Sending request to Groq (attempt {attempt + 1}/{self.max_retries})"
                )

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT_VOLLEYBALL,
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                )

                # Extract response content
                if response.choices and len(response.choices) > 0:
                    result = response.choices[0].message.content
                    logger.info("Successfully analyzed commentary")
                    return result
                else:
                    raise ValueError("Empty response from Groq API")

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")

                # Calculate backoff delay (exponential)
                if attempt < self.max_retries - 1:
                    backoff_time = 2 ** attempt
                    logger.info(f"Retrying after {backoff_time}s...")
                    time.sleep(backoff_time)
                continue

        # All retries exhausted
        error_msg = (
            f"Failed to analyze commentary after {self.max_retries} attempts. "
            f"Last error: {str(last_error)}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    def extract_json(self, commentary: str) -> dict:
        """
        Analyze commentary and return parsed JSON response

        Args:
            commentary: Text commentary to analyze

        Returns:
            Parsed JSON dictionary

        Raises:
            ValueError: If JSON parsing fails
        """
        import json

        raw_response = self.analyze_commentary(commentary)

        try:
            # Try to extract JSON from response
            # Handle cases where LLM might add extra text
            json_start = raw_response.find("{")
            json_end = raw_response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = raw_response[json_start:json_end]
                parsed = json.loads(json_str)
                logger.info("Successfully parsed JSON response")
                return parsed
            else:
                raise ValueError("No valid JSON found in response")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            logger.error(f"Raw response: {raw_response[:200]}...")
            raise ValueError(f"Invalid JSON in LLM response: {str(e)}")
