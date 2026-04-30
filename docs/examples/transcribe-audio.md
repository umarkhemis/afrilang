# Transcribe Audio

```python
from afrilang import AfriLang
import httpx

client = AfriLang(api_key="afrlk_...")

# From a local file
with open("speech.wav", "rb") as f:
    stt = client.transcribe(f.read(), language="lug")

print(stt.transcript)
print(f"Language: {stt.language}")
print(f"Time: {stt.latency_ms}ms")

# From a URL
audio = httpx.get("https://example.com/audio.mp3").content
stt = client.transcribe(audio, language="sw")
print(stt.transcript)
```
