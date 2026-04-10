"""
Static in-memory model registry.

Each entry describes a translation model for a specific language pair.
Fields:
  - source_lang:    BCP-47 / ISO-639-1 source language code
  - target_lang:    BCP-47 / ISO-639-1 target language code
  - provider:       "huggingface" | "sunbird"
  - model_id:       provider-specific model identifier or HF repo id
  - endpoint:       full inference URL (None = use provider default)
  - quality_score:  float 0-1 (higher = better); used by router to pick best model
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class ModelEntry:
    source_lang: str
    target_lang: str
    provider: str
    model_id: str
    endpoint: Optional[str]
    quality_score: float


# ---------------------------------------------------------------------------
# Registry: list of known models for MVP language pairs
# ---------------------------------------------------------------------------
MODEL_REGISTRY: list[ModelEntry] = [
    # --- Swahili ---
    ModelEntry(
        source_lang="en",
        target_lang="sw",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-en-sw",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-sw",
        quality_score=0.82,
    ),
    ModelEntry(
        source_lang="sw",
        target_lang="en",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-sw-en",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-sw-en",
        quality_score=0.82,
    ),
    # --- Yoruba ---
    ModelEntry(
        source_lang="en",
        target_lang="yo",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-en-yo",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-yo",
        quality_score=0.75,
    ),
    ModelEntry(
        source_lang="yo",
        target_lang="en",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-yo-en",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-yo-en",
        quality_score=0.75,
    ),
    # --- Hausa ---
    ModelEntry(
        source_lang="en",
        target_lang="ha",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-en-ha",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ha",
        quality_score=0.77,
    ),
    ModelEntry(
        source_lang="ha",
        target_lang="en",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-ha-en",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-ha-en",
        quality_score=0.77,
    ),
    # --- Igbo ---
    ModelEntry(
        source_lang="en",
        target_lang="ig",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-en-ig",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ig",
        quality_score=0.72,
    ),
    ModelEntry(
        source_lang="ig",
        target_lang="en",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-ig-en",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-ig-en",
        quality_score=0.72,
    ),
    # --- Zulu ---
    ModelEntry(
        source_lang="en",
        target_lang="zu",
        provider="huggingface",
        model_id="AfriScience-MT/nllb_200_distilled_600m-eng-zul",
        endpoint="https://api-inference.huggingface.co/models/AfriScience-MT/nllb_200_distilled_600m-eng-zul",
        quality_score=0.78,
    ),
    ModelEntry(
        source_lang="zu",
        target_lang="en",
        provider="huggingface",
        model_id="Helsinki-NLP/opus-mt-zu-en",
        endpoint="https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-zu-en",
        quality_score=0.74,
    ),
    # --- Ugandan languages via Sunbird Sunflower ---
    # TODO: replace model_id and endpoint with real Sunbird values once API access is granted
    ModelEntry(
        source_lang="en",
        target_lang="lg",
        provider="sunbird",
        model_id="sunbird-sunflower-lg",
        endpoint=None,  # set via SUNBIRD_API_KEY / provider adapter
        quality_score=0.85,
    ),
    ModelEntry(
        source_lang="lg",
        target_lang="en",
        provider="sunbird",
        model_id="sunbird-sunflower-lg",
        endpoint=None,
        quality_score=0.85,
    ),
    ModelEntry(
        source_lang="en",
        target_lang="nyn",
        provider="sunbird",
        model_id="sunbird-sunflower-nyn",
        endpoint=None,
        quality_score=0.83,
    ),
    ModelEntry(
        source_lang="en",
        target_lang="luo",
        provider="sunbird",
        model_id="sunbird-sunflower-luo",
        endpoint=None,
        quality_score=0.80,
    ),
    ModelEntry(
        source_lang="en",
        target_lang="lgg",
        provider="sunbird",
        model_id="sunbird-sunflower-lgg",
        endpoint=None,
        quality_score=0.78,
    ),
    ModelEntry(
        source_lang="en",
        target_lang="teo",
        provider="sunbird",
        model_id="sunbird-sunflower-teo",
        endpoint=None,
        quality_score=0.78,
    ),
]


def get_models_for_pair(source_lang: str, target_lang: str) -> list[ModelEntry]:
    """Return all registry entries matching the given language pair."""
    return [
        m
        for m in MODEL_REGISTRY
        if m.source_lang == source_lang and m.target_lang == target_lang
    ]
