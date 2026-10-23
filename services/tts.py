"""Synthèse texte -> audio (Together AI). Étape 7 du guide."""
import config


def clean_text(text: str) -> str:
    """Retire markdown, code et emojis avant la synthèse. À faire."""
    raise NotImplementedError


def split_text(text: str, max_chars: int = config.TTS_MAX_CHARS) -> list[str]:
    """Découpe le texte par phrases (limite de longueur par requête). À faire."""
    raise NotImplementedError


def synthesize(text: str) -> bytes:
    """Renvoie les octets audio de la réponse, lisibles avec st.audio. À faire."""
    raise NotImplementedError("TTS pas encore implémenté (étape 7)")
