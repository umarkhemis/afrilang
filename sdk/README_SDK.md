# afrilang

Official Python SDK for the **AfriLang API** — unified translation and speech for 30+ African languages.

## Install

```bash
pip install afrilang
```

## Quick start

```python
from afrilang import AfriLang

client = AfriLang(api_key="afrlk_...")   # or set AFRILANG_API_KEY env var

# Translate
result = client.translate("Hello, how are you?", target="sw")
print(result)                  # Habari, ukoje?
print(result.model_used)       # Helsinki-NLP/opus-mt-en-sw
print(result.quality_score)    # 0.85

# Auto-detect source language
result = client.translate("Bonjour le monde", target="sw")
print(result.detected_source_lang)   # fr

# Force a provider
result = client.translate("Good morning", target="lug", provider="sunbird")
```

## Batch translation

```python
batch = client.translate_batch([
    {"id": "1", "text": "Good morning",  "target": "lug"},
    {"id": "2", "text": "Thank you",     "target": "yo"},
    {"id": "3", "text": "How are you?",  "target": "ha"},
])

print(f"{batch.succeeded}/{batch.total} succeeded")

for item in batch:
    if item.success:
        print(f"[{item.id}] {item.translated_text}")
    else:
        print(f"[{item.id}] ERROR: {item.error}")
```

## Speech-to-Text

```python
# From file path
stt = client.transcribe("greeting.wav", language="lug")
print(stt.transcript)

# From bytes
with open("speech.mp3", "rb") as f:
    stt = client.transcribe(f.read(), language="sw")
print(stt.transcript)
```

## Text-to-Speech

```python
tts = client.synthesise("Oli otya?", language="lug")

if tts.audio_url:
    print(f"Download audio: {tts.audio_url}")

if tts.audio_base64:
    import base64
    audio_bytes = base64.b64decode(tts.audio_base64)
    with open("output.mp3", "wb") as f:
        f.write(audio_bytes)
```

## List languages

```python
for lang in client.languages():
    caps = []
    if lang.supports_translation: caps.append("translate")
    if lang.supports_stt:         caps.append("stt")
    if lang.supports_tts:         caps.append("tts")
    print(f"{lang.code:6} {lang.name:20} [{', '.join(caps)}]")
```

## Async usage

```python
import asyncio
from afrilang import AfriLang

async def main():
    async with AfriLang(api_key="afrlk_...") as client:
        result = await client.async_translate("Hello", target="sw")
        print(result)

        batch = await client.async_translate_batch([
            {"id": "a", "text": "Good night", "target": "lug"},
        ])
        print(batch.results[0])

asyncio.run(main())
```

## Error handling

```python
from afrilang import (
    AfriLang,
    AuthenticationError,
    RateLimitError,
    UnsupportedLanguageError,
    ProviderError,
)

client = AfriLang(api_key="afrlk_...")

try:
    result = client.translate("Hello", target="xx")  # invalid language
except UnsupportedLanguageError as e:
    print(f"Language not supported: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except ProviderError as e:
    print(f"All providers failed: {e}")
```

## Supported languages

| Code  | Language    | Region          | Translate | STT | TTS |
|-------|-------------|-----------------|-----------|-----|-----|
| sw    | Swahili     | East Africa     | ✅        | ✅  | ✅  |
| lug   | Luganda     | East Africa     | ✅        | ✅  | ✅  |
| nyn   | Runyankole  | East Africa     | ✅        | ✅  | ✅  |
| ach   | Acholi      | East Africa     | ✅        | ✅  | ✅  |
| teo   | Ateso       | East Africa     | ✅        | ✅  | ✅  |
| lgg   | Lugbara     | East Africa     | ✅        | ✅  | ✅  |
| yo    | Yoruba      | West Africa     | ✅        | —   | —   |
| ha    | Hausa       | West Africa     | ✅        | —   | —   |
| ig    | Igbo        | West Africa     | ✅        | —   | —   |
| zu    | Zulu        | Southern Africa | ✅        | —   | —   |
| rw    | Kinyarwanda | East Africa     | ✅        | ✅  | —   |
| am    | Amharic     | East Africa     | ✅        | —   | —   |
| …     | 20+ more    | …               | ✅        | —   | —   |

Full list: `client.languages()`

## License

MIT
