# Installation

## Requirements

- Python 3.9 or higher
- An AfriLang API key ([get one free](../getting-started/authentication.md))

## Install the SDK

=== "pip"

    ```bash
    pip install afrilang
    ```

=== "poetry"

    ```bash
    poetry add afrilang
    ```

=== "uv"

    ```bash
    uv add afrilang
    ```

## Verify the installation

```python
import afrilang
print(afrilang.__version__)  # 1.0.0
```

## Set your API key

The SDK reads your key from the environment variable `AFRILANG_API_KEY`:

```bash
export AFRILANG_API_KEY="afrlk_your_key_here"
```

Or pass it directly when creating the client:

```python
from afrilang import AfriLang

client = AfriLang(api_key="afrlk_your_key_here")
```

!!! tip "Best practice"
    Store your key in an `.env` file and load it with `python-dotenv`:
    ```bash
    pip install python-dotenv
    ```
    ```python
    from dotenv import load_dotenv
    load_dotenv()

    from afrilang import AfriLang
    client = AfriLang()  # reads AFRILANG_API_KEY from environment
    ```

## Configuration options

```python
client = AfriLang(
    api_key="afrlk_...",          # your API key
    base_url="https://api.afrilang.betatechlabs.io",  # default
    timeout=30,                    # HTTP timeout in seconds
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str` | `AFRILANG_API_KEY` env var | Your AfriLang API key |
| `base_url` | `str` | AfriLang API URL | Override for self-hosted instances |
| `timeout` | `int` | `30` | HTTP request timeout in seconds |

## Next steps

- [Quick Start](quickstart.md) - make your first translation
- [Authentication](authentication.md) - learn about API keys
- [Supported Languages](languages.md) - see all available languages
