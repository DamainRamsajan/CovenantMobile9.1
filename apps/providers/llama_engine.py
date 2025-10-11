import os
from .client import chat_completions, list_models

PROVIDER_MODEL = os.getenv("PROVIDER_MODEL") or "phi-3-mini-instruct"

def health():
    try:
        data = list_models()
        return {"ok": True, "models": [m.get("id") or m for m in data.get("data", [])]}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def chat_complete(system_prompt: str, user_prompt: str, temperature=0.2, max_tokens=512):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    return chat_completions(messages, temperature=temperature, max_tokens=max_tokens, model=PROVIDER_MODEL)
