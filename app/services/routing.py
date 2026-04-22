"""
AfriLang – Routing service.

Selects the best provider + model for a given language pair,
with automatic fallback if the primary provider fails.

Fallback chain:
  1. Best model for the pair (highest quality_score)
  2. NLLB-200 via HuggingFace (universal fallback)
"""
from __future__ import annotations

import logging
from typing import Optional

from app.core.registry import ModelEntry, get_model_fast
from app.schemas.translate import Provider
from app.services.providers.base import BaseProvider, TranslationResult
from app.services.providers.huggingface import HuggingFaceProvider
from app.services.providers.sunbird import SunbirdProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

# Lazy singleton providers (one instance per process)
_SUNBIRD: Optional[SunbirdProvider] = None
_HUGGINGFACE: Optional[HuggingFaceProvider] = None


def _sunbird() -> SunbirdProvider:
    global _SUNBIRD
    if _SUNBIRD is None:
        _SUNBIRD = SunbirdProvider()
    return _SUNBIRD


def _huggingface() -> HuggingFaceProvider:
    global _HUGGINGFACE
    if _HUGGINGFACE is None:
        _HUGGINGFACE = HuggingFaceProvider()
    return _HUGGINGFACE


def _get_provider(provider_id: str) -> BaseProvider:
    if provider_id == "sunbird":
        return _sunbird()
    return _huggingface()


async def route_translation(
    text: str,
    source_lang: str,
    target_lang: str,
    preferred_provider: Provider = Provider.auto,
) -> TranslationResult:
    """
    Translate text from source_lang to target_lang.

    If preferred_provider is Provider.auto, selects the highest-quality model.
    Falls back to NLLB-200 if the primary provider raises an exception.
    """
    # 1. Select primary model
    entry: ModelEntry = get_model_fast(source_lang, target_lang)

    # Override provider if caller specified one
    if preferred_provider != Provider.auto:
        provider_id = preferred_provider.value
    else:
        provider_id = entry.provider

    primary_provider = _get_provider(provider_id)

    # 2. Attempt primary
    try:
        return await primary_provider.translate(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            model_id=entry.model_id,
        )
    except Exception as exc:
        logger.error(
            "Primary provider '%s' failed for %s→%s: %s – falling back to NLLB",
            provider_id, source_lang, target_lang, exc,
        )

    # 3. Fallback: NLLB-200 via HuggingFace
    fallback_model = settings.default_model_id
    try:
        return await _huggingface().translate(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            model_id=fallback_model,
        )
    except Exception as exc2:
        logger.error("NLLB fallback also failed: %s", exc2)
        raise RuntimeError(
            f"All providers failed for {source_lang}→{target_lang}. "
            f"Last error: {exc2}"
        ) from exc2
