"""
Pydantic schemas for the /translate endpoint.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate.")
    target_lang: str = Field(
        ..., description="BCP-47 target language code (e.g. 'sw', 'yo', 'lg')."
    )
    source_lang: Optional[str] = Field(
        None,
        description="BCP-47 source language code. Auto-detected if omitted.",
    )


class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="The translated output.")
    detected_source_lang: str = Field(
        ..., description="Source language code (detected or provided)."
    )
    model_used: str = Field(..., description="Identifier of the model that produced the translation.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1).")
