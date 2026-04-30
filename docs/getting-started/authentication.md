# Authentication

AfriLang uses API keys for authentication. Every request must include your key in the `Authorization` header.

## Getting an API key

### Via the REST API

```bash
curl -X POST https://api.afrilang.betatechlabs.io/api/v1/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"name": "production-app"}'
```

```json
{
  "api_key": "afrlk_a1b2c3d4e5f6...",
  "name": "production-app",
  "expires_at": "2027-04-23T00:00:00Z",
  "note": "Store this key securely. It will NOT be shown again."
}
```

!!! warning "Save your key immediately"
    The plain-text key is only returned **once**. Store it in a secrets manager, `.env` file, or environment variable immediately. It cannot be recovered.

### Via the Python SDK

```python
# Keys are issued via the REST API — the SDK uses them, not creates them
# Use the curl command above or the /docs UI to create your first key
```

## Using your key

=== "Python SDK"

    ```python
    from afrilang import AfriLang

    # Option 1: pass directly
    client = AfriLang(api_key="afrlk_...")

    # Option 2: environment variable (recommended)
    import os
    os.environ["AFRILANG_API_KEY"] = "afrlk_..."
    client = AfriLang()
    ```

=== "REST API"

    ```bash
    # Include in every request
    curl -H "Authorization: Bearer afrlk_..." \
         https://api.afrilang.betatechlabs.io/api/v1/translate \
         -d '...'
    ```

=== ".env file"

    ```bash
    # .env
    AFRILANG_API_KEY=afrlk_...
    ```

    ```python
    from dotenv import load_dotenv
    load_dotenv()

    from afrilang import AfriLang
    client = AfriLang()  # auto-reads AFRILANG_API_KEY
    ```

## Inspecting your key

```python
# Via REST API
curl -H "Authorization: Bearer afrlk_..." \
     https://api.afrilang.betatechlabs.io/api/v1/auth/keys/me
```

```json
{
  "name": "production-app",
  "created_at": "2025-04-23T10:00:00Z",
  "expires_at": "2027-04-23T10:00:00Z",
  "requests_total": 1432
}
```

## Key format

All AfriLang API keys follow this format:

```
afrlk_<40 hex characters>
```

Example: `afrlk_a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`

## Security best practices

!!! danger "Never expose your key"
    - Do not commit API keys to source control
    - Do not include keys in client-side code (JavaScript, mobile apps)
    - Do not share keys in Slack, email, or screenshots

!!! tip "Use environment variables"
    Always load keys from environment variables or a secrets manager:
    ```bash
    # Good
    export AFRILANG_API_KEY="afrlk_..."

    # Bad - never hardcode in source
    client = AfriLang(api_key="afrlk_...")  # in committed code
    ```

!!! tip "Use separate keys per environment"
    Create different keys for development, staging, and production.
    This way you can revoke a compromised key without affecting other environments.

## Error responses

| HTTP Status | Code | Meaning |
|---|---|---|
| `401` | `MISSING_API_KEY` | No Authorization header provided |
| `401` | `INVALID_API_KEY` | Key is wrong, expired, or revoked |

```json
{
  "detail": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid or has expired."
  }
}
```
