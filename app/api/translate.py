"""
POST /translate endpoint.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.translate import TranslateRequest, TranslateResponse
from app.utils.lang_detect import detect_language
from app.services.routing import select_model
from app.services.providers.huggingface import HuggingFaceProvider
from app.services.providers.sunbird import SunbirdProvider

router = APIRouter()

# Map provider name → adapter instance
_PROVIDERS = {
    "huggingface": HuggingFaceProvider(),
    "sunbird": SunbirdProvider(),
}


@router.post("/translate", response_model=TranslateResponse)
def translate(request: TranslateRequest) -> TranslateResponse:
    """
    Translate text to the requested target language.

    - If *source_lang* is omitted, the language is auto-detected.
    - The best available model is selected from the registry.
    - Falls back to facebook/nllb-200-distilled-600M when no specific model is registered.
    """
    # 1. Resolve source language
    source_lang = request.source_lang
    if not source_lang:
        detected = detect_language(request.text)
        if not detected:
            raise HTTPException(
                status_code=422,
                detail="Could not detect source language. Please provide source_lang explicitly.",
            )
        source_lang = detected

    # 2. Select best model
    model_entry = select_model(source_lang, request.target_lang)

    # 3. Get provider adapter
    provider = _PROVIDERS.get(model_entry.provider)
    if provider is None:
        raise HTTPException(
            status_code=500,
            detail=f"No adapter registered for provider '{model_entry.provider}'.",
        )

    # 4. Run translation
    try:
        result = provider.translate(
            text=request.text,
            source_lang=source_lang,
            target_lang=request.target_lang,
            model_id=model_entry.model_id,
            endpoint=model_entry.endpoint,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider error: {exc}") from exc

    return TranslateResponse(
        translated_text=result["translated_text"],
        detected_source_lang=source_lang,
        model_used=model_entry.model_id,
        confidence=result["confidence"],
    )
