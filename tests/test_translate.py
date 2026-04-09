"""
Basic tests for the POST /api/v1/translate endpoint.

Run with:
    pytest tests/
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# /translate – happy-path tests (stub mode, no real API key required)
# ---------------------------------------------------------------------------

def test_translate_with_source_lang():
    """Translate English to Swahili with explicit source language."""
    payload = {
        "text": "Hello, how are you?",
        "source_lang": "en",
        "target_lang": "sw",
    }
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert data["detected_source_lang"] == "en"
    assert "model_used" in data
    assert 0.0 <= data["confidence"] <= 1.0


def test_translate_auto_detect():
    """Translate without providing source_lang (auto-detect)."""
    payload = {
        "text": "Hello world",
        "target_lang": "sw",
    }
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert "detected_source_lang" in data


def test_translate_to_yoruba():
    payload = {
        "text": "Good morning",
        "source_lang": "en",
        "target_lang": "yo",
    }
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_source_lang"] == "en"


def test_translate_to_luganda_uses_sunbird():
    """Luganda is served by the Sunbird provider (stub response expected)."""
    payload = {
        "text": "Thank you",
        "source_lang": "en",
        "target_lang": "lg",
    }
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sunbird" in data["model_used"].lower() or "sunbird" in data["translated_text"].lower()


def test_translate_fallback_model():
    """Unknown language pair should fall back to the NLLB default model."""
    payload = {
        "text": "Hello",
        "source_lang": "en",
        "target_lang": "xx",  # not in registry
    }
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "nllb" in data["model_used"].lower() or "facebook" in data["model_used"].lower()


# ---------------------------------------------------------------------------
# /translate – validation error tests
# ---------------------------------------------------------------------------

def test_translate_missing_text():
    """Request without 'text' should return 422."""
    payload = {"target_lang": "sw"}
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 422


def test_translate_missing_target_lang():
    """Request without 'target_lang' should return 422."""
    payload = {"text": "Hello"}
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 422


def test_translate_empty_text():
    """Empty string for 'text' should return 422 (min_length=1)."""
    payload = {"text": "", "target_lang": "sw"}
    response = client.post("/api/v1/translate", json=payload)
    assert response.status_code == 422
