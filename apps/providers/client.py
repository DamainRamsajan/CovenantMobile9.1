import os, json, requests

PROVIDER_BASE_URL = os.getenv("PROVIDER_BASE_URL") or "http://127.0.0.1:8080/v1"
PROVIDER_MODEL = os.getenv("PROVIDER_MODEL") or "phi-3-mini-instruct"

def _url(path: str) -> str:
    return f"{PROVIDER_BASE_URL.rstrip('/')}/{path.lstrip('/')}"

def list_models():
    r = requests.get(_url("/models"), timeout=20)
    r.raise_for_status()
    return r.json()

def chat_completions(messages, temperature=0.2, max_tokens=512, stop=None, model=None, **kw):
    payload = {
        "model": model or PROVIDER_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    if stop:
        payload["stop"] = stop
    r = requests.post(_url("/chat/completions"), json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # OpenAI-compatible: choices[0].message.content
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return json.dumps(data, indent=2)
