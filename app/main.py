"""
AfriLang API – entry point.

Run locally:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.translate import router as translate_router

app = FastAPI(
    title="AfriLang",
    description=(
        "A unified translation API for African languages. "
        "Supports auto-detection of source language and intelligent routing "
        "to the best available translation model."
    ),
    version="0.1.0",
)

app.include_router(translate_router, prefix="/api/v1", tags=["translation"])


@app.get("/health", tags=["health"])
def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok"}
