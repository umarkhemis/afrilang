"""
Hugging Face Inference API adapter.

Makes an HTTP POST to the HF Inference API endpoint for the selected model.
In the MVP stub the call is simulated when no API key is configured so the
app can run end-to-end without real credentials.

TODO: replace the stub response with a real HTTP call once HF_API_KEY is set.
"""

import requests

from app.core.config import settings
from app.services.providers.base import BaseProvider

# Timeout for real HTTP calls (seconds)
_HTTP_TIMEOUT = 30


class HuggingFaceProvider(BaseProvider):
    """Adapter for Hugging Face Inference API models."""

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        model_id: str,
        endpoint: str | None = None,
    ) -> dict:
        api_key = settings.huggingface_api_key

        # ------------------------------------------------------------------
        # Stub mode: no API key configured → return a simulated response so
        # the app is runnable locally without credentials.
        # ------------------------------------------------------------------
        if not api_key:
            return {
                "translated_text": f"[STUB] {text} -> ({target_lang})",
                "confidence": 0.0,
            }

        # ------------------------------------------------------------------
        # Real mode: call the HF Inference API
        # TODO: handle model loading delays (503) with retry logic
        # ------------------------------------------------------------------
        url = endpoint or f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": text}

        response = requests.post(url, headers=headers, json=payload, timeout=_HTTP_TIMEOUT)
        response.raise_for_status()

        data = response.json()

        # HF translation pipelines return a list of dicts with "translation_text"
        if isinstance(data, list) and data:
            translated = data[0].get("translation_text", "")
        else:
            translated = str(data)

        return {
            "translated_text": translated,
            "confidence": 0.9,  # HF API does not return confidence; use fixed proxy
        }
