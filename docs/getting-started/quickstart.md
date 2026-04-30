# Quick Start

Get AfriLang working in under 5 minutes.

## 1. Install

```bash
pip install afrilang
```

## 2. Get an API key

```bash
curl -X POST https://api.afrilang.betatechlabs.io/api/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"name": "my-app"}'
```

```json
{
  "api_key": "afrlk_a1b2c3d4...",
  "name": "my-app",
  "expires_at": "2026-04-23T00:00:00Z",
  "note": "Store this key securely. It will NOT be shown again."
}
```

## 3. Translate text

=== "Python SDK"

    ```python
    from afrilang import AfriLang

    client = AfriLang(api_key="afrlk_...")

    result = client.translate("Hello, how are you?", target="lug")

    print(result)                # "Oli otya?"
    print(result.target_lang)    # "lug"
    print(result.provider)       # "sunbird"
    print(result.quality_score)  # 0.92
    print(result.latency_ms)     # 820
    ```

=== "REST API"

    ```bash
    curl -X POST https://api.afrilang.betatechlabs.io/api/v1/translate \
      -H "Authorization: Bearer afrlk_..." \
      -H "Content-Type: application/json" \
      -d '{
        "text": "Hello, how are you?",
        "target_lang": "lug"
      }'
    ```

    ```json
    {
      "translated_text": "Oli otya?",
      "detected_source_lang": "en",
      "target_lang": "lug",
      "model_used": "sunbird/nllb_translate",
      "provider": "sunbird",
      "quality_score": 0.92,
      "latency_ms": 820,
      "characters_translated": 19
    }
    ```

## 4. Batch translate

Translate multiple texts in a single call:

```python
batch = client.translate_batch([
    {"id": "greeting", "text": "Good morning",  "target": "yo"},
    {"id": "thanks",   "text": "Thank you",     "target": "sw"},
    {"id": "welcome",  "text": "You are welcome","target": "ha"},
])

print(f"{batch.succeeded}/{batch.total} succeeded")

for item in batch:
    if item.success:
        print(f"{item.id}: {item.translated_text}")
    else:
        print(f"{item.id}: ERROR - {item.error}")
```

## 5. Speech

=== "Text to Speech"

    ```python
    tts = client.synthesise("Oli otya?", language="lug")
    print(tts.audio_url)
    # https://cdn.sunbird.ai/tts/abc123.mp3
    ```

=== "Speech to Text"

    ```python
    with open("audio.wav", "rb") as f:
        stt = client.transcribe(f.read(), language="lug")

    print(stt.transcript)
    ```

## 6. List available languages

```python
for lang in client.languages():
    caps = []
    if lang.supports_translation: caps.append("translate")
    if lang.supports_stt:         caps.append("stt")
    if lang.supports_tts:         caps.append("tts")
    print(f"{lang.code:6}  {lang.name:20}  [{', '.join(caps)}]")
```

```
lug     Luganda               [translate, stt, tts]
ach     Acholi                [translate, stt, tts]
nyn     Runyankole            [translate, stt, tts]
sw      Swahili               [translate, stt, tts]
yo      Yoruba                [translate]
ha      Hausa                 [translate]
...
```

## What's next?

- [Authentication](authentication.md) - manage API keys
- [Supported Languages](languages.md) - full language list
- [API Reference](../api-reference/translation.md) - complete endpoint reference
- [SDK Reference](../sdk-reference/client.md) - full SDK documentation
- [Guides](../guides/index.md) - real-world use cases
