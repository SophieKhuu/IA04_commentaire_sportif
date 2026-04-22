"""
Configuration module - centralized settings and constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# ============================================================================
# LLM Configuration (Groq)
# ============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "mixtral-8x7b-32768")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))
LLM_TIMEOUT = 30  # seconds

# ============================================================================
# Whisper Configuration
# ============================================================================

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")

# ============================================================================
# FFmpeg Configuration
# ============================================================================

FFMPEG_PATH = os.getenv(
    "FFMPEG_PATH",
    r"c:\Users\zebri\Documents\GitHub\IA04_commentaire_sportif\ffmpeg-essentials_build\bin"
)

# ============================================================================
# Volleyball Scoring Criteria
# ============================================================================

SCORING_CRITERIA = {
    "technique": {
        "name": "Technique",
        "description": "Maîtrise technique du jeu (passes, frappe, etc.)",
        "weight": 0.20,
    },
    "defense": {
        "name": "Défense",
        "description": "Efficacité en défense (blocage, récupération)",
        "weight": 0.25,
    },
    "attitude": {
        "name": "Attitude",
        "description": "Comportement et engagement mental",
        "weight": 0.20,
    },
    "physique": {
        "name": "Physique",
        "description": "Performance physique et explosivité",
        "weight": 0.15,
    },
    "decision_tactique": {
        "name": "Décision tactique",
        "description": "Prise de décision et lecture du jeu",
        "weight": 0.15,
    },
    "autre": {
        "name": "Autre",
        "description": "Autres observations pertinentes",
        "weight": 0.05,
    },
}

# Score range validation
MIN_SCORE = 0
MAX_SCORE = 100

# ============================================================================
# LLM Prompts
# ============================================================================

SYSTEM_PROMPT_VOLLEYBALL = """Tu es un expert en analyse de volleyball avec 20+ ans d'expérience.
Tu dois analyser des commentaires sportifs de volleyball et extraire les informations suivantes en JSON valide:

1. Résumé (1-2 phrases): les faits clés du commentaire
2. Joueurs identifiés: liste des noms/numéros
3. Pour chaque joueur:
   - Technique (0-100): maîtrise technique
   - Défense (0-100): efficacité défensive
   - Attitude (0-100): engagement mental et comportement
   - Physique (0-100): performance physique
   - Décision_tactique (0-100): prise de décision
   - Autre (0-100): observations diverses
   - Résumé: observation narrative

Réponds UNIQUEMENT en JSON valide sans commentaires additionnels.
Format JSON attendu:
{
  "summary": "...",
  "players": [
    {
      "name": "...",
      "number": "...",
      "technique": 75,
      "defense": 80,
      "attitude": 85,
      "physique": 78,
      "decision_tactique": 72,
      "autre": 70,
      "notes": "..."
    }
  ]
}
"""

# ============================================================================
# Application Configuration
# ============================================================================

APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "8501"))

# ============================================================================
# Validation Settings
# ============================================================================

MIN_COMMENTARY_LENGTH = 10  # minimum words
MAX_COMMENTARY_LENGTH = 5000  # maximum words
