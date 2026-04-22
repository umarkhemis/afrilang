"""
afrilang – Official Python SDK for the AfriLang API.

Quick start::

    from afrilang import AfriLang

    client = AfriLang(api_key="afrlk_...")

    # Translate
    result = client.translate("Hello, how are you?", target="sw")
    print(result)  # Habari, ukoje?

    # Batch
    batch = client.translate_batch([
        {"id": "1", "text": "Good morning", "target": "lug"},
        {"id": "2", "text": "Thank you",    "target": "yo"},
    ])
    for item in batch:
        print(item.id, item)

    # Speech-to-Text
    stt = client.transcribe("speech.wav", language="lug")
    print(stt.transcript)

    # Text-to-Speech
    tts = client.synthesise("Oli otya?", language="lug")
    print(tts.audio_url)

    # List languages
    for lang in client.languages():
        print(lang)
"""

from .client import (
    AfriLang,
    AfriLangError,
    AuthenticationError,
    BatchItemResult,
    BatchResult,
    Language,
    ProviderError,
    RateLimitError,
    STTResult,
    TTSResult,
    TranslationResult,
    UnsupportedLanguageError,
)

__all__ = [
    "AfriLang",
    # Results
    "TranslationResult",
    "BatchResult",
    "BatchItemResult",
    "STTResult",
    "TTSResult",
    "Language",
    # Exceptions
    "AfriLangError",
    "AuthenticationError",
    "RateLimitError",
    "UnsupportedLanguageError",
    "ProviderError",
]

__version__ = "1.0.0"
