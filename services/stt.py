"""Transcription audio -> texte (Groq Whisper). Étape 6 du guide."""
import config


def transcribe_audio(audio_file) -> str:
    """Reçoit l'audio WAV de st.chat_input et renvoie le texte transcrit.

    À faire : appeler l'endpoint de transcription de Groq avec
    config.STT_MODEL et config.STT_LANGUAGE (langue précisée : français).
    """
    raise NotImplementedError("STT pas encore implémenté (étape 6)")
