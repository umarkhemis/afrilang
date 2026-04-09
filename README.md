# AfriLang

**Simplifying Access to African Language AI**

AfriLang is a unified translation API that gives developers a single endpoint to translate African languages. It auto-detects source language, routes each request to the best available model, and returns clean JSON — abstracting away fragmented research models and providers.

---

## Features

- **POST /translate** — one endpoint for all supported language pairs
- **Auto-detect** source language (powered by `langdetect`)
- **Intelligent routing** — selects the highest-quality model from the registry
- **Fallback** to `facebook/nllb-200-distilled-600M` for unsupported pairs
- **Stub mode** — runs end-to-end without real API keys (great for local dev)
- **Extensible** — add new models/providers by editing `app/core/registry.py`

---

## Supported Languages (MVP)

| Language     | Code  | Provider          |
|-------------|-------|-------------------|
| Swahili     | `sw`  | Hugging Face      |
| Yoruba      | `yo`  | Hugging Face      |
| Hausa       | `ha`  | Hugging Face      |
| Igbo        | `ig`  | Hugging Face      |
| Zulu        | `zu`  | Hugging Face      |
| Luganda     | `lg`  | Sunbird (pending) |
| Runyankole  | `nyn` | Sunbird (pending) |
| Luo         | `luo` | Sunbird (pending) |
| Lugbara     | `lgg` | Sunbird (pending) |
| Teso        | `teo` | Sunbird (pending) |

---

## Project Structure

```
afrilang/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── api/
│   │   └── translate.py           # POST /translate endpoint
│   ├── core/
│   │   ├── config.py              # Settings (API keys, base URL)
│   │   └── registry.py            # Static in-memory model registry
│   ├── schemas/
│   │   └── translate.py           # Pydantic request/response models
│   ├── services/
│   │   ├── routing.py             # Best-model selector
│   │   └── providers/
│   │       ├── base.py            # Provider interface (ABC)
│   │       ├── huggingface.py     # Hugging Face adapter
│   │       └── sunbird.py         # Sunbird adapter (stub)
│   └── utils/
│       └── lang_detect.py         # Language auto-detection
├── tests/
│   └── test_translate.py          # Endpoint tests (pytest)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Local Development

### 1. Clone & install dependencies

```bash
git clone https://github.com/umarkhemis/afrilang.git
cd afrilang
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your API keys (optional for stub mode)
```

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

## Example Request

```bash
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "target_lang": "sw"
  }'
```

### Response

```json
{
  "translated_text": "Habari, ukoje?",
  "detected_source_lang": "en",
  "model_used": "Helsinki-NLP/opus-mt-en-sw",
  "confidence": 0.9
}
```

> **Note:** Without a `HUGGINGFACE_API_KEY`, the response will be a labelled stub (e.g. `[STUB] Hello, how are you? -> (sw)`). This lets you develop and test the full pipeline locally without credentials.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Adding a New Model

1. Open `app/core/registry.py`
2. Add a new `ModelEntry` to `MODEL_REGISTRY`
3. If it uses a new provider, create an adapter in `app/services/providers/` that extends `BaseProvider`
4. Register the adapter in `app/api/translate.py` under `_PROVIDERS`

---

## Roadmap

- [ ] Real Hugging Face API integration (remove stub)
- [ ] Sunbird Sunflower integration (once API access granted)
- [ ] Python SDK (`pip install afrilang`)
- [ ] More language pairs
- [ ] Caching layer (Redis)
- [ ] Rate limiting & auth
- [ ] Deploy to Render / Fly.io

---

## License

MIT
