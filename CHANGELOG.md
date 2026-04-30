# Changelog

All notable changes to AfriLang are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
AfriLang follows [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2025-04-23

Initial public release by Beta-Tech Labs.

### Added
- Translation API with auto language detection (`POST /api/v1/translate`)
- Batch translation up to 50 items (`POST /api/v1/translate/batch`)
- Speech-to-text for East African languages (`POST /api/v1/speech/stt`)
- Text-to-speech for 6 East African languages (`POST /api/v1/speech/tts`)
- Languages endpoint (`GET /api/v1/languages`)
- API key authentication with SHA-256 hashing
- Redis-backed rate limiting (in-memory fallback)
- Sunbird AI integration (Luganda, Acholi, Runyankole, Ateso, Lugbara)
- Helsinki-NLP integration (Swahili, Yoruba, Hausa, Igbo, Zulu, Kinyarwanda)
- opus-mt-en-mul universal fallback (100+ languages)
- Python SDK (`pip install afrilang`) with sync and async support
- Docker + Docker Compose + Nginx production stack
- GitHub Actions CI/CD (test, build, deploy, security scan)
- GitHub Actions docs deployment to GitHub Pages
- PyPI publish workflow with trusted publishing
- Railway, Render, DigitalOcean deployment configs
- MkDocs Material documentation site (30+ pages)
- 52 unit and integration tests

### Providers
- Sunbird AI: quality score 0.92 for Ugandan languages
- Helsinki-NLP: quality score 0.78-0.85 for West/East Africa
- opus-mt-en-mul: quality score 0.62 universal fallback

### Languages
- 30+ languages at launch across East, West, Southern, and North Africa
- STT: 10 languages (lug, ach, nyn, teo, lgg, sw, en, rw, xog, myx)
- TTS: 6 languages (lug, ach, nyn, teo, lgg, sw)
