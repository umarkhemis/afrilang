"""
Language detection utility.

Uses the `langdetect` library for MVP. Returns an ISO-639-1 language code.
Falls back to "en" if detection fails.
"""

from typing import Optional


def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of *text* and return its ISO-639-1 code.

    Returns None if detection fails or the input is too short to be reliable.
    """
    try:
        from langdetect import detect, LangDetectException  # type: ignore

        lang = detect(text)
        return lang
    except Exception:
        return None
