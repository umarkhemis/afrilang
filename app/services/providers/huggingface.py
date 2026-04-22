"""
AfriLang – HuggingFace Inference API provider adapter.

Supports:
  • Helsinki-NLP/opus-mt-* models (direct translation)
  • facebook/nllb-200-distilled-600M  (200-language fallback)

The NLLB model requires flores200 language codes (e.g. "eng_Latn").
We map AfriLang codes → flores200 via LANGUAGE_REGISTRY.nllb_code.

Stub mode: if HUGGINGFACE_API_KEY is empty, returns labelled stub text.
"""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional

import httpx

from app.core.config import settings
from app.core.registry import LANGUAGE_REGISTRY
from app.services.providers.base import BaseProvider, TranslationResult

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_RETRY_STATUSES = {429, 500, 502, 503, 504}

# NLLB flores200 codes for languages not in LANGUAGE_REGISTRY
_EXTRA_NLLB: dict[str, str] = {
    "luo": "luo_Latn",
    "ff":  "fuv_Latn",
    "wo":  "wol_Latn",
    "tw":  "twi_Latn",
}


def _nllb_code(lang: str) -> str:
    info = LANGUAGE_REGISTRY.get(lang)
    if info and info.nllb_code:
        return info.nllb_code
    # Try extra map
    if lang in _EXTRA_NLLB:
        return _EXTRA_NLLB[lang]
    # Best-effort: assume flores200 format already
    return lang


class HuggingFaceProvider(BaseProvider):
    """Adapter for HuggingFace Inference API."""

    def __init__(self) -> None:
        self._key = settings.huggingface_api_key
        self._base = settings.huggingface_base_url.rstrip("/")
        self._stub = not bool(self._key)
        if self._stub:
            logger.warning(
                "HUGGINGFACE_API_KEY not set – HuggingFace provider in stub mode."
            )

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._key}"}

    async def _infer(self, model_id: str, payload: dict) -> dict:
        """Call HuggingFace inference with retries."""
        url = f"{self._base}/{model_id}"
        last_exc: Exception = RuntimeError("no attempts made")

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=settings.http_timeout) as client:
                    resp = await client.post(url, json=payload,
                                             headers=self._headers())

                # HuggingFace returns 503 while model is loading
                if resp.status_code == 503:
                    wait = min(20, 5 * attempt)
                    logger.info("HF model loading – waiting %ds (attempt %d)", wait, attempt)
                    await asyncio.sleep(wait)
                    last_exc = httpx.HTTPStatusError(
                        "503 model loading", request=resp.request, response=resp
                    )
                    continue

                if resp.status_code in _RETRY_STATUSES:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
                    last_exc = httpx.HTTPStatusError(
                        f"HTTP {resp.status_code}", request=resp.request, response=resp
                    )
                    continue

                resp.raise_for_status()
                return resp.json()

            except httpx.RequestError as exc:
                logger.error("HuggingFace request error: %s", exc)
                last_exc = exc
                await asyncio.sleep(2 ** attempt)

        raise last_exc

    # ── Translation ──────────────────────────────────────────────────────────

    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        model_id: str,
    ) -> TranslationResult:
        t0 = time.monotonic()

        if self._stub:
            return TranslationResult(
                translated_text=f"[HF-STUB] {text} → ({target_lang})",
                model_used=model_id,
                provider="huggingface",
                quality_score=0.0,
                latency_ms=0,
            )

        is_nllb = "nllb" in model_id.lower()

        if is_nllb:
            # NLLB requires flores200 codes passed as parameters
            payload = {
                "inputs": text,
                "parameters": {
                    "src_lang": _nllb_code(source_lang),
                    "tgt_lang": _nllb_code(target_lang),
                },
            }
        else:
            # Helsinki-NLP models are fine-tuned per pair; just pass text
            payload = {"inputs": text}

        data = await self._infer(model_id, payload)
        latency_ms = int((time.monotonic() - t0) * 1000)

        # HF returns either a list of dicts or a single dict
        if isinstance(data, list):
            translated = data[0].get("translation_text", "")
        else:
            translated = data.get("translation_text", str(data))

        # Quality score: NLLB fallback is lower than specialised models
        score = 0.60 if is_nllb else 0.78

        return TranslationResult(
            translated_text=translated,
            model_used=model_id,
            provider="huggingface",
            quality_score=score,
            latency_ms=latency_ms,
        )
