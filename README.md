<div align="center">
  <h1>AfriLang</h1>
  <p><strong>Unified translation and speech API for 30+ African languages</strong></p>
  <p>Built by <a href="https://betatechlabs.io">Beta-Tech Labs</a></p>

  <p>
    <a href="https://pypi.org/project/afrilang/"><img alt="PyPI" src="https://img.shields.io/pypi/v/afrilang?color=0d5fa0&label=PyPI"></a>
    <a href="https://pypi.org/project/afrilang/"><img alt="Python" src="https://img.shields.io/pypi/pyversions/afrilang?color=0d5fa0"></a>
    <a href="https://github.com/umarkhemis/afrilang/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-0d5fa0"></a>
    <a href="https://github.com/umarkhemis/afrilang/actions"><img alt="CI" src="https://github.com/umarkhemis/afrilang/actions/workflows/ci-cd.yml/badge.svg"></a>
    <a href="https://docs.afrilang.betatechlabs.io"><img alt="Docs" src="https://img.shields.io/badge/docs-live-0d5fa0"></a>
  </p>
</div>

---

## What is AfriLang?

AfriLang is a production-grade API and Python SDK for translating text and processing speech across 30+ African languages. It intelligently routes each request to the best available model — Sunbird AI for Ugandan languages, Helsinki-NLP for West and East Africa — and falls back gracefully when needed.

```bash
pip install afrilang
```

```python
from afrilang import AfriLang

client = AfriLang(api_key="afrlk_...")

# Translate
result = client.translate("Hello, how are you?", target="lug")
print(result)  # "Oli otya?"

# Batch
batch = client.translate_batch([
    {"id": "1", "text": "Good morning", "target": "yo"},
    {"id": "2", "text": "Thank you",    "target": "sw"},
    {"id": "3", "text": "Welcome",      "target": "ha"},
])

# Speech to Text
stt = client.transcribe("audio.wav", language="lug")
print(stt.transcript)

# Text to Speech
tts = client.synthesise("Oli otya?", language="lug")
print(tts.audio_url)
```

## Features

- **30+ African languages** - Luganda, Swahili, Yoruba, Hausa, Igbo, Zulu, Acholi, Runyankole, Ateso, Lugbara, Kinyarwanda, Amharic, and more
- **Intelligent routing** - automatically selects the highest-quality model per language pair
- **Speech AI** - STT and TTS for East African languages via Sunbird AI
- **Batch processing** - translate up to 50 texts in one API call
- **Async support** - full `async`/`await` for FastAPI, Django async, and asyncio
- **Production ready** - auth, Redis rate limiting, retries, Docker deployment
- **MIT licensed** - free for commercial use

## Provider routing

| Provider | Languages | Quality |
|---|---|---|
| Sunbird AI | lug, nyn, ach, teo, lgg | 0.92 |
| Helsinki-NLP | sw, yo, ha, ig, zu, rw | 0.78-0.85 |
| opus-mt-en-mul | 100+ language fallback | 0.62 |

## Documentation

Full documentation at **[docs.afrilang.betatechlabs.io](https://docs.afrilang.betatechlabs.io)**

- [Installation](https://docs.afrilang.betatechlabs.io/getting-started/installation/)
- [Quick Start](https://docs.afrilang.betatechlabs.io/getting-started/quickstart/)
- [API Reference](https://docs.afrilang.betatechlabs.io/api-reference/)
- [Python SDK](https://docs.afrilang.betatechlabs.io/sdk-reference/)
- [Guides](https://docs.afrilang.betatechlabs.io/guides/)

## Self-hosting

```bash
# Clone and configure
git clone https://github.com/umarkhemis/afrilang.git
cd afrilang
cp env.example .env    # fill in your API keys

# Start with Docker
docker compose up -d

# API is live at http://localhost/docs
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway, Render, and DigitalOcean instructions.

## Deploy in 5 minutes (Railway)

```bash
npm install -g @railway/cli
railway login
railway up
# Add HUGGINGFACE_API_KEY and SUNBIRD_API_KEY in Railway dashboard
```

## Contributing

We welcome contributions - new languages especially. See [CONTRIBUTING.md](docs/contributing.md).

```bash
git clone https://github.com/umarkhemis/afrilang.git
cd afrilang
pip install -r requirements.txt
pytest tests/ -v    # 52 tests
```

## License

MIT - see [LICENSE](LICENSE)

---

<div align="center">
  <sub>Built with care for Africa's 1.4 billion people by <a href="https://betatechlabs.io">Beta-Tech Labs</a></sub>
</div>
