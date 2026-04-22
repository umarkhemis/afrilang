"""
AfriLang – Sunbird AI provider adapter.

Implements:
  • Translation  → POST /tasks/nllb_translate
  • STT          → POST /tasks/stt
  • TTS          → POST /tasks/tts

Authentication: Bearer token in Authorization header.
Base URL: https://api.sunbird.ai  (overridable via SUNBIRD_BASE_URL)

Retry strategy: up to 3 attempts with exponential back-off on 429/5xx.
"""
from __future__ import annotations

import asyncio
import base64
import logging
import time
from typing import Optional

import httpx

from app.core.config import settings
from app.core.registry import LANGUAGE_REGISTRY
from app.services.providers.base import (
    BaseProvider,
    STTResult,
    TTSResult,
    TranslationResult,
)
from app.utils.lang_detect import map_sunbird_lang

logger = logging.getLogger(__name__)

# Sunbird language code map (AfriLang -> Sunbird)
_TO_SUNBIRD: dict[str, str] = {
    "en":  "eng",
    "sw":  "swa",
    "lug": "lug",
    "nyn": "nyn",
    "lgg": "lgg",
    "ach": "ach",
    "teo": "teo",
    "rw":  "kin",
    "xog": "xog",
    "myx": "myx",
    "laj": "laj",
    "adh": "adh",
}

# Sunbird TTS voice IDs
_TTS_VOICE_IDS: dict[str, int] = {
    "ach": 241,
    "teo": 242,
    "nyn": 243,
    "lgg": 245,
    "swa": 246,
    "sw":  246,
    "lug": 248,
}

_MAX_RETRIES = 3
_RETRY_STATUSES = {429, 500, 502, 503, 504}


class SunbirdProvider(BaseProvider):
    """Adapter for the Sunbird AI public API."""

    def __init__(self) -> None:
        self._base = settings.sunbird_base_url.rstrip("/")
        self._key = settings.sunbird_api_key
        self._stub = not bool(self._key)
        if self._stub:
            logger.warning(
                "SUNBIRD_API_KEY not set – Sunbird provider running in stub mode."
            )

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
        }

    async def _post_with_retry(
        self, url: str, json: dict, timeout: int = settings.http_timeout
    ) -> dict:
        """POST with exponential back-off retries."""
        last_exc: Exception = RuntimeError("no attempts made")
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    resp = await client.post(url, json=json, headers=self._headers())

                if resp.status_code not in _RETRY_STATUSES:
                    resp.raise_for_status()
                    return resp.json()

                # Retryable status
                wait = 2 ** attempt
                logger.warning(
                    "Sunbird %s returned %s (attempt %d/%d) – retrying in %ds",
                    url, resp.status_code, attempt, _MAX_RETRIES, wait,
                )
                await asyncio.sleep(wait)
                last_exc = httpx.HTTPStatusError(
                    f"HTTP {resp.status_code}", request=resp.request, response=resp
                )
            except httpx.RequestError as exc:
                logger.error("Sunbird request error: %s", exc)
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
                translated_text=f"[SUNBIRD-STUB] {text} → ({target_lang})",
                model_used=model_id,
                provider="sunbird",
                quality_score=0.0,
                latency_ms=0,
            )

        src = _TO_SUNBIRD.get(source_lang, source_lang)
        tgt = _TO_SUNBIRD.get(target_lang, target_lang)

        payload = {
            "source_language": src,
            "target_language": tgt,
            "text": text,
        }

        data = await self._post_with_retry(
            f"{self._base}/tasks/nllb_translate", json=payload
        )

        output = data.get("output", {})
        translated = output.get("translated_text") or output.get("text", "")
        latency_ms = int((time.monotonic() - t0) * 1000)

        return TranslationResult(
            translated_text=translated,
            model_used=model_id,
            provider="sunbird",
            quality_score=0.92,
            latency_ms=latency_ms,
        )

    # ── Speech-to-Text ───────────────────────────────────────────────────────

    async def speech_to_text(
        self,
        audio_bytes: bytes,
        language: str,
        filename: str = "audio.wav",
    ) -> STTResult:
        t0 = time.monotonic()

        if self._stub:
            return STTResult(
                transcript="[SUNBIRD-STUB] STT not available without API key.",
                detected_lang=language,
                model_used="sunbird/stt",
                provider="sunbird",
                latency_ms=0,
            )

        sunbird_lang = _TO_SUNBIRD.get(language, language)
        url = f"{self._base}/tasks/stt"

        last_exc: Exception = RuntimeError("no attempts made")
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=settings.http_timeout_stt) as client:
                    files = {"audio": (filename, audio_bytes, "audio/wav")}
                    data_form = {"language": sunbird_lang}
                    headers = {"Authorization": f"Bearer {self._key}"}
                    resp = await client.post(url, files=files, data=data_form,
                                             headers=headers)
                if resp.status_code not in _RETRY_STATUSES:
                    resp.raise_for_status()
                    break
                wait = 2 ** attempt
                await asyncio.sleep(wait)
                last_exc = httpx.HTTPStatusError(
                    f"HTTP {resp.status_code}", request=resp.request, response=resp
                )
            except httpx.RequestError as exc:
                last_exc = exc
                await asyncio.sleep(2 ** attempt)
        else:
            raise last_exc

        out = resp.json().get("output", {})
        transcript = out.get("text") or out.get("transcript", "")
        detected = map_sunbird_lang(out.get("detected_language", language))
        latency_ms = int((time.monotonic() - t0) * 1000)

        return STTResult(
            transcript=transcript,
            detected_lang=detected,
            model_used="sunbird/stt",
            provider="sunbird",
            latency_ms=latency_ms,
        )

    # ── Text-to-Speech ───────────────────────────────────────────────────────

    async def text_to_speech(
        self,
        text: str,
        language: str,
        voice_id: Optional[int] = None,
    ) -> TTSResult:
        t0 = time.monotonic()

        if self._stub:
            return TTSResult(
                audio_url=None,
                audio_base64=None,
                content_type="audio/mpeg",
                model_used="sunbird/tts",
                provider="sunbird",
                latency_ms=0,
            )

        vid = voice_id or _TTS_VOICE_IDS.get(language)
        if vid is None:
            raise ValueError(
                f"No TTS voice available for language '{language}'. "
                f"Supported: {list(_TTS_VOICE_IDS.keys())}"
            )

        payload = {"text": text, "voice_id": vid}
        data = await self._post_with_retry(
            f"{self._base}/tasks/tts", json=payload
        )

        latency_ms = int((time.monotonic() - t0) * 1000)
        output = data.get("output", {})

        # Sunbird may return a signed URL or raw base64
        audio_url = output.get("audio_url") or output.get("url")
        audio_b64 = output.get("audio_base64") or output.get("audio")

        return TTSResult(
            audio_url=audio_url,
            audio_base64=audio_b64,
            content_type="audio/mpeg",
            model_used="sunbird/tts",
            provider="sunbird",
            latency_ms=latency_ms,
        )
