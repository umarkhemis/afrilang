# Changelog

All notable changes to AfriLang are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
AfriLang follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2025-04-23

Initial public release of AfriLang by Beta-Tech Labs.

### Added

**API**

- `POST /api/v1/translate` - single text translation with auto language detection
- `POST /api/v1/translate/batch` - batch translation of up to 50 items concurrently
- `POST /api/v1/speech/stt` - speech-to-text for East African languages via Sunbird AI
- `POST /api/v1/speech/tts` - text-to-speech for 6 East African languages via Sunbird AI
- `GET /api/v1/languages` - list all supported languages with capability flags
- `POST /api/v1/auth/keys` - issue API keys
- `GET /api/v1/auth/keys/me` - inspect current API key metadata
- `GET /api/v1/debug/env` - environment diagnostics (requires `DEBUG=true`)
- `GET /api/v1/debug/providers` - live provider connectivity check
- `GET /health` - health check with provider status

**Provider routing**

- Sunbird AI integration for Ugandan languages (Luganda, Acholi, Runyankole, Ateso, Lugbara)
- Helsinki-NLP integration for West and East African languages (Swahili, Yoruba, Hausa, Igbo, Zulu, Kinyarwanda)
- opus-mt-en-mul as universal fallback covering 100+ languages
- Automatic fallback chain: primary provider → HuggingFace fallback
- Exponential backoff retries (up to 3 attempts) on 5xx errors

**Security**

- API key authentication with SHA-256 hashing (keys never stored in plaintext)
- Constant-time key comparison to prevent timing attacks
- Rate limiting: 60 req/min for translate/speech, 10 req/min for batch
- Redis-backed rate limiting in production (in-memory fallback for dev)

**Infrastructure**

- Multi-stage Dockerfile (non-root user, ~180MB image)
- Docker Compose with API + Redis + Nginx
- GitHub Actions CI/CD pipeline (test → build → deploy → security scan)
- Railway and Render one-click deployment configs
- DigitalOcean automated setup script

**Python SDK**

- `AfriLang` client class with sync and async support
- `translate()` and `async_translate()` methods
- `translate_batch()` and `async_translate_batch()` methods
- `transcribe()` for speech-to-text
- `synthesise()` / `synthesize()` for text-to-speech
- `languages()`, `translation_languages()`, `speech_languages()` methods
- Typed return objects: `TranslationResult`, `BatchResult`, `STTResult`, `TTSResult`, `Language`
- Typed exceptions: `AuthenticationError`, `RateLimitError`, `UnsupportedLanguageError`, `ProviderError`

**Languages supported at launch**

- Translation: 30+ languages across East, West, Southern, and North Africa
- STT: Luganda, Acholi, Runyankole, Ateso, Lugbara, Swahili, English, Kinyarwanda, Lusoga, Lumasaba
- TTS: Luganda, Acholi, Runyankole, Ateso, Lugbara, Swahili

**Documentation**

- MkDocs Material documentation site
- Getting started, API reference, SDK reference, guides, and examples

**Tests**

- 52 unit and integration tests with 100% pass rate
- Live test suite (`test_live.py`) covering all endpoints
- Smoke test script (`smoke_test.py`)
- Stress/load test script (`stress_test.py`)

---

## Roadmap

The following features are planned for upcoming releases:

### [1.1.0] - Planned

- [ ] JavaScript/TypeScript SDK (`npm install afrilang`)
- [ ] Real-time streaming translation via WebSocket
- [ ] Language detection endpoint (`POST /api/v1/detect`)
- [ ] Additional Sunbird languages (Kinyarwanda TTS, Lango STT)

### [1.2.0] - Planned

- [ ] Go SDK
- [ ] Usage dashboard and analytics
- [ ] Webhook support for async batch jobs
- [ ] Custom glossary support (domain-specific terminology)

### [2.0.0] - Future

- [ ] 50+ language support
- [ ] Document translation (PDF, DOCX)
- [ ] Real-time translation API (streaming)
- [ ] Self-hosted model deployment guide

---

Have a feature request? [Open an issue on GitHub](https://github.com/umarkhemis/afrilang/issues/new?template=feature_request.md).
