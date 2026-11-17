import json
import urllib.request

from config import FORGE_ENDPOINT, FORGE_MODEL, FORGE_API_KEY, LLM_TIMEOUT_SECONDS


def call_llm(system_prompt, user_prompt, max_tokens=120):
    """Call an OpenAI-compatible chat endpoint (Ollama by default).

    Returns the reply text, or None if no endpoint is reachable. Nothing
    in this project requires this to succeed; it only adds a bit of polish
    on top of the deterministic, rule-based pipeline.
    """
    url = FORGE_ENDPOINT.rstrip("/") + "/chat/completions"
    payload = {
        "model": FORGE_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FORGE_API_KEY}",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
