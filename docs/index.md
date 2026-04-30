---
title: AfriLang - African Language AI Infrastructure
description: Unified translation and speech API for 30+ African languages
hide:
  - navigation
  - toc
---

<div class="afrilang-hero" markdown>

# AfriLang

**Unified translation and speech API for 30+ African languages.**

One API. Intelligent routing. Production-grade from day one.
Built by [Beta-Tech Labs](https://betatechlabs.io) for developers who are serious about reaching Africa's 1.4 billion people.

[Get Started :octicons-arrow-right-24:](getting-started/installation.md){ .md-button .md-button--primary }
[View on GitHub :octicons-mark-github-24:](https://github.com/umarkhemis/afrilang){ .md-button }

</div>

---

```bash
pip install afrilang
```

```python
from afrilang import AfriLang

client = AfriLang(api_key="afrlk_...")

# Translate English to Luganda
result = client.translate("Hello, how are you?", target="lug")
print(result)  # "Oli otya?"

# Batch translate to multiple languages
batch = client.translate_batch([
    {"id": "1", "text": "Good morning", "target": "yo"},
    {"id": "2", "text": "Thank you",    "target": "sw"},
    {"id": "3", "text": "Welcome",      "target": "ha"},
])

# Text to speech
audio = client.synthesise("Oli otya?", language="lug")
print(audio.audio_url)
```

---

## Why AfriLang?

<div class="feature-grid" markdown>

<div class="feature-card" markdown>
<div class="feature-icon">🌍</div>
### 30+ African Languages
Luganda, Swahili, Yoruba, Hausa, Igbo, Zulu, Acholi, Runyankole, Ateso, Lugbara, Kinyarwanda, Amharic, and more — with new languages added regularly.
</div>

<div class="feature-card" markdown>
<div class="feature-icon">🧠</div>
### Intelligent Routing
AfriLang automatically selects the highest-quality model for every language pair — Sunbird AI for Ugandan languages, Helsinki-NLP for West and East Africa, with universal fallback for 100+ languages.
</div>

<div class="feature-card" markdown>
<div class="feature-icon">🔊</div>
### Speech AI
Speech-to-text and text-to-speech for East African languages, powered by Sunbird AI — which outperforms GPT-4 on 24 out of 31 Ugandan languages.
</div>

<div class="feature-card" markdown>
<div class="feature-icon">⚡</div>
### Batch Processing
Translate up to 50 texts in a single API call with concurrent processing, per-item error isolation, and full result metadata.
</div>

<div class="feature-card" markdown>
<div class="feature-icon">🐍</div>
### Python SDK
A clean, typed Python client with sync and async support, rich return objects, and typed exceptions — designed to feel native in any codebase.
</div>

<div class="feature-card" markdown>
<div class="feature-icon">🔒</div>
### Production Ready
API key authentication, Redis-backed rate limiting, automatic retries with exponential backoff, structured logging, and Docker deployment — all included.
</div>

</div>

---

## Providers

AfriLang routes each request to the best available model:

| Provider | Languages | Quality |
|---|---|---|
| **Sunbird AI** | Luganda, Acholi, Runyankole, Ateso, Lugbara | 0.92 |
| **Helsinki-NLP** | Swahili, Yoruba, Hausa, Igbo, Zulu, Kinyarwanda | 0.78-0.85 |
| **opus-mt-en-mul** | 100+ language fallback | 0.62 |

---

## Quick navigation

<div class="feature-grid" markdown>

<div class="feature-card" markdown>
### :material-rocket-launch: Get Started
Install AfriLang and make your first translation call in under 5 minutes.

[Installation](getting-started/installation.md) · [Quick Start](getting-started/quickstart.md)
</div>

<div class="feature-card" markdown>
### :material-api: API Reference
Full reference for every REST endpoint with request/response examples.

[Translation](api-reference/translation.md) · [Speech](api-reference/stt.md) · [Errors](api-reference/errors.md)
</div>

<div class="feature-card" markdown>
### :material-language-python: Python SDK
Complete SDK reference with type signatures and docstrings.

[Client](sdk-reference/client.md) · [Async](sdk-reference/async.md) · [Types](sdk-reference/types.md)
</div>

<div class="feature-card" markdown>
### :material-book-open-variant: Guides
Step-by-step guides for common use cases and integrations.

[Multilingual App](guides/multilingual-app.md) · [Batch Processing](guides/batch-at-scale.md)
</div>

</div>

---

## Built by Beta-Tech Labs

AfriLang is an open-source project by [Beta-Tech Labs](https://betatechlabs.io), an enterprise software company building infrastructure for Africa's digital economy.

- :octicons-mark-github-24: [GitHub](https://github.com/umarkhemis/afrilang) — source code, issues, contributions
- :octicons-package-24: [PyPI](https://pypi.org/project/afrilang/) — `pip install afrilang`
- :octicons-law-24: [MIT License](https://github.com/umarkhemis/afrilang/blob/main/LICENSE) — free to use commercially
