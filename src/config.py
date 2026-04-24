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

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")

# ============================================================================
# FFmpeg Configuration
# ============================================================================

FFMPEG_PATH = os.getenv(
    "FFMPEG_PATH",
    r"c:\Users\zebri\Documents\GitHub\IA04_commentaire_sportif\ffmpeg-essentials_build\bin"
)

# ============================================================================
# Volleyball Scoring Criteria (0-20 scale based on concrete metrics)
# ============================================================================

SCORING_CRITERIA = {
    "technique": {
        "name": "Technique",
        "description": "Maîtrise technique du geste - Formula: (points + aces×2) - (erreurs×2)",
        "weight": 0.20,
    },
    "defense": {
        "name": "Défense",
        "description": "Capacité défensive - Formula: (blocks×3) - erreurs",
        "weight": 0.25,
    },
    "attitude": {
        "name": "Attitude",
        "description": "Cohérence et régularité - Formula: 20 - erreurs",
        "weight": 0.20,
    },
    "physique": {
        "name": "Physique",
        "description": "Intensité et fréquence d'actions - Formula: (points + aces + blocks) / 2",
        "weight": 0.15,
    },
    "decision_tactique": {
        "name": "Décision tactique",
        "description": "Efficacité des choix tactiques - Formula: (points×2) / (points + erreurs + blocks) × 20",
        "weight": 0.25,
    },
}

# Score range validation (0-20 scale)
MIN_SCORE = 0
MAX_SCORE = 20

# ============================================================================
# LLM Prompts
# ============================================================================

SYSTEM_PROMPT_VOLLEYBALL = """Tu es un analyste expert de matchs de volley-ball.

Ton rôle est de transformer une transcription de match en JSON STRICT et d'évaluer les joueurs.

RÈGLES IMPORTANTES :
- Tu dois répondre UNIQUEMENT en JSON valide
- Aucun texte hors JSON
- Ne pas inventer de joueurs inexistants
- Si une info manque, mettre null ou 0
- Noter chaque joueur sur 20 selon 5 critères concrets

CRITÈRES DE NOTATION (0-20) :
1. technique : Basé sur le ratio (points + aces) / erreurs. Maîtrise du geste.
   Formula: (points + aces*2) - (erreurs*2) = note/20
   
2. defense : Basé sur le nombre de blocks réussis et erreurs de défense.
   Formula: (blocks*3) - (erreurs) = note/20
   
3. attitude : Évalué par la cohérence et la récurrence des bonnes actions.
   Formula: 20 - (erreurs) = note/20
   
4. physique : Évalué par l'intensité et la fréquence des actions.
   Formula: (points + aces + blocks) / 2 = note/20
   
5. decision_tactique : Évalué par l'efficacité des actions.
   Formula: (points*2) / (points + erreurs + blocks) * 20 = note/20

FORMAT OBLIGATOIRE :
{
  "summary": "string",
  "players": [
    {
      "name": "string",
      "number": null,
      "points": 0,
      "aces": 0,
      "blocks": 0,
      "errors": 0,
      "scores": {
        "technique": 0,
        "defense": 0,
        "attitude": 0,
        "physique": 0,
        "decision_tactique": 0
      },
      "final_score": 0,
      "notes": "string"
    }
  ]
}

INSTRUCTIONS SUPPLÉMENTAIRES :
- final_score = moyenne des 5 critères arrondie à 1 décimale
- notes : synthèse courte de la performance du joueur et ses points forts/faibles
- Être précis, structuré et cohérent dans l'analyse
- Les scores doivent refléter UNIQUEMENT ce qui est observé dans la transcription
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
