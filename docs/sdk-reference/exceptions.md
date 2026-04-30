# Exceptions

AfriLang raises typed exceptions so you can handle different failure modes precisely.

## Exception hierarchy

```
AfriLangError (base)
├── AuthenticationError     HTTP 401
├── RateLimitError          HTTP 429
├── UnsupportedLanguageError HTTP 422
└── ProviderError           HTTP 503
```

## Import

```python
from afrilang import (
    AfriLangError,
    AuthenticationError,
    RateLimitError,
    UnsupportedLanguageError,
    ProviderError,
)
```

---

## AfriLangError

Base class for all AfriLang exceptions.

```python
class AfriLangError(Exception):
    message:     str
    code:        str   # machine-readable error code
    status_code: int   # HTTP status code
```

---

## AuthenticationError

Raised when the API key is missing, invalid, or expired.

```python
try:
    client = AfriLang()  # no key set
except AuthenticationError as e:
    print(e.code)  # "MISSING_API_KEY"

try:
    result = client.translate("Hello", target="lug")
except AuthenticationError as e:
    print(e.code)         # "INVALID_API_KEY"
    print(e.status_code)  # 401
```

---

## RateLimitError

Raised when the rate limit is exceeded.

```python
class RateLimitError(AfriLangError):
    retry_after: int   # seconds to wait before retrying
```

```python
import time
from afrilang import RateLimitError

try:
    result = client.translate("Hello", target="lug")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
    time.sleep(e.retry_after)
    result = client.translate("Hello", target="lug")  # retry
```

---

## UnsupportedLanguageError

Raised when a language or language pair is not supported.

```python
from afrilang import UnsupportedLanguageError

try:
    result = client.translate("Hello", target="xx")
except UnsupportedLanguageError as e:
    print(e)  # "Language not supported..."
```

---

## ProviderError

Raised when all providers fail to translate the text. Usually transient — retry with exponential backoff.

```python
import time
from afrilang import ProviderError

for attempt in range(3):
    try:
        result = client.translate("Hello", target="lug")
        break
    except ProviderError:
        time.sleep(2 ** attempt)
```

---

## Catching all AfriLang errors

```python
from afrilang import AfriLangError

try:
    result = client.translate("Hello", target="lug")
except AfriLangError as e:
    print(f"AfriLang error [{e.code}]: {e}")
    print(f"HTTP status: {e.status_code}")
```
