"""
Sunbird Sunflower API adapter (stub).

Sunbird AI provides translation for 30+ Ugandan languages via their
Sunflower model family. Real API access is pending partnership approval.

TODO: Replace stub with real Sunbird API call once access is granted.
      Sunbird docs: https://docs.sunbird.ai/
"""

from app.core.config import settings
from app.services.providers.base import BaseProvider


class SunbirdProvider(BaseProvider):
    """Stub adapter for the Sunbird Sunflower translation API."""

    # TODO: update once Sunbird provides official endpoint details
    _BASE_URL = "https://api.sunbird.ai/tasks/nllb_translate"

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        model_id: str,
        endpoint: str | None = None,
    ) -> dict:
        api_key = settings.sunbird_api_key

        # ------------------------------------------------------------------
        # Stub: Sunbird API access not yet available.
        # Returns a clearly labelled placeholder so the pipeline stays
        # runnable end-to-end.
        # ------------------------------------------------------------------
        if not api_key:
            return {
                "translated_text": (
                    f"[SUNBIRD STUB] Translation of '{text}' to '{target_lang}' "
                    "not available yet. Add SUNBIRD_API_KEY to .env when access is granted."
                ),
                "confidence": 0.0,
            }

        # TODO: implement real Sunbird HTTP call here
        # Example (subject to actual Sunbird API spec):
        #
        # import requests
        # url = endpoint or self._BASE_URL
        # headers = {"Authorization": f"Bearer {api_key}"}
        # payload = {
        #     "source_language": source_lang,
        #     "target_language": target_lang,
        #     "text": text,
        # }
        # response = requests.post(url, headers=headers, json=payload, timeout=30)
        # response.raise_for_status()
        # data = response.json()
        # return {
        #     "translated_text": data["output"]["translated_text"],
        #     "confidence": data.get("confidence", 0.9),
        # }

        return {
            "translated_text": f"[SUNBIRD STUB] {text}",
            "confidence": 0.0,
        }
