"""Réglages centralisés : provider, modèles, clés, paramètres.

Rien de tout cela ne doit être écrit en dur dans les services ou dans app.py.
Les noms de modèles changent souvent : vérifie-les dans le catalogue du provider.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

# --- Clés API (lues depuis .env, jamais écrites ici) ---
GROQ_API_KEY = os.getenv("GROQ_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# --- LLM / VLM (Groq) ---
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "qwen/qwen3.8-27b"  # TODO: à vérifier dans le catalogue Groq
TEMPERATURE = 0.7
MAX_TOKENS = 1024

# --- Images ---
MAX_IMAGE_SIZE = 512  # px, plus grand côté
JPEG_QUALITY = 80

# --- STT (Groq Whisper) ---
STT_MODEL = "whisper-large-v3-turbo"
STT_LANGUAGE = "fr"

# --- TTS (Together AI) ---
TTS_MODEL = "TODO"  # modèle TTS parlant français (catalogue Together AI)
TTS_VOICE = "TODO"
TTS_MAX_CHARS = 200  # longueur max par requête

# --- Prompt système ---
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system.md"
