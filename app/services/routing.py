"""
Routing layer: selects the best translation model for a given language pair.

Selection logic:
  1. Query MODEL_REGISTRY for all entries matching (source_lang, target_lang).
  2. Return the entry with the highest quality_score.
  3. If no entry is found, fall back to the default NLLB model (HuggingFace).
"""

from app.core.registry import ModelEntry, get_models_for_pair
from app.core.config import settings

# Fallback model used when no registry entry matches the requested pair
_FALLBACK_MODEL = ModelEntry(
    source_lang="*",
    target_lang="*",
    provider="huggingface",
    model_id=settings.default_model_id,
    endpoint=(
        f"https://api-inference.huggingface.co/models/{settings.default_model_id}"
    ),
    quality_score=0.6,
)


def select_model(source_lang: str, target_lang: str) -> ModelEntry:
    """
    Return the best ModelEntry for the given language pair.

    Falls back to the default NLLB model if no entry is registered.
    """
    candidates = get_models_for_pair(source_lang, target_lang)
    if not candidates:
        return _FALLBACK_MODEL
    return max(candidates, key=lambda m: m.quality_score)
