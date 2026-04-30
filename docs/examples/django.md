# Django Integration

```python
# settings.py
import os
AFRILANG_API_KEY = os.environ.get("AFRILANG_API_KEY")

# utils/translation.py
from django.conf import settings
from afrilang import AfriLang

_client = None

def get_client() -> AfriLang:
    global _client
    if _client is None:
        _client = AfriLang(api_key=settings.AFRILANG_API_KEY)
    return _client

# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from utils.translation import get_client
import json

@csrf_exempt
@require_POST
def translate_view(request):
    data = json.loads(request.body)
    client = get_client()
    result = client.translate(
        data["text"],
        target=data["target_lang"],
    )
    return JsonResponse({"translated_text": str(result)})
```
