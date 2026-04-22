"""
AfriLang – FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload

Interactive docs:
    http://localhost:8000/docs     (Swagger UI)
    http://localhost:8000/redoc    (ReDoc)
"""
from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router
from app.api.languages import router as languages_router
from app.api.speech import router as speech_router
from app.api.translate import router as translate_router
from app.core.config import settings
from app.core.security import get_dev_key

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s – %(message)s",
)
logger = logging.getLogger("afrilang")


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    dev_key = get_dev_key()
    logger.info("=" * 60)
    logger.info("AfriLang API starting up")
    logger.info("Docs:     %s/docs", settings.base_url)
    logger.info("Dev key:  %s", dev_key)
    logger.info("  └─ Use this key for local development.")
    logger.info("  └─ Issue production keys via POST /api/v1/auth/keys")
    if not settings.sunbird_api_key:
        logger.warning("SUNBIRD_API_KEY not set – Sunbird provider in stub mode")
    if not settings.huggingface_api_key:
        logger.warning("HUGGINGFACE_API_KEY not set – HuggingFace provider in stub mode")
    logger.info("=" * 60)
    yield
    logger.info("AfriLang API shutting down")


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AfriLang API",
    description=(
        "**AfriLang** – Unified translation and speech API for African languages.\n\n"
        "A single endpoint to translate, transcribe, and synthesise speech across "
        "30+ African languages, powered by Sunbird AI, Helsinki-NLP, and NLLB-200.\n\n"
        "## Authentication\n"
        "All endpoints (except `POST /api/v1/auth/keys`) require an API key:\n"
        "```\nAuthorization: Bearer afrlk_<your-key>\n```\n\n"
        "## Quick start\n"
        "1. Issue a key: `POST /api/v1/auth/keys`\n"
        "2. Translate:   `POST /api/v1/translate`\n"
        "3. Batch:       `POST /api/v1/translate/batch`\n"
        "4. Speak:       `POST /api/v1/speech/tts`\n"
        "5. Transcribe:  `POST /api/v1/speech/stt`\n"
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request timing middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    t0 = time.monotonic()
    response = await call_next(request)
    ms = int((time.monotonic() - t0) * 1000)
    response.headers["X-Process-Time-Ms"] = str(ms)
    return response


# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
            }
        },
    )


# ── Routers ───────────────────────────────────────────────────────────────────
PREFIX = "/api/v1"

app.include_router(auth_router,      prefix=PREFIX)
app.include_router(translate_router, prefix=PREFIX)
app.include_router(speech_router,    prefix=PREFIX)
app.include_router(languages_router, prefix=PREFIX)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"], summary="Health check")
async def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "providers": {
            "sunbird":     "live" if settings.sunbird_api_key else "stub",
            "huggingface": "live" if settings.huggingface_api_key else "stub",
        },
    }


@app.get("/", tags=["System"], include_in_schema=False)
async def root():
    return {
        "name": "AfriLang API",
        "version": "1.0.0",
        "docs": f"{settings.base_url}/docs",
        "health": f"{settings.base_url}/health",
    }
