import os, json, urllib.request

LLAMA_URL = os.getenv("LLAMA_URL", "http://127.0.0.1:8080")

def complete(prompt: str, n_predict: int = 128) -> str:
    req = urllib.request.Request(
        f"{LLAMA_URL}/completion",
        data=json.dumps({"prompt": prompt, "n_predict": n_predict}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    # Handle either {"content": "..."} or {"choices":[{"text":"..."}]}
    if isinstance(data, dict) and "content" in data:
        return data["content"]
    if isinstance(data, dict) and data.get("choices"):
        return (data["choices"][0].get("text") or "").strip()
    return str(data)
