import os

# Optional local/self-hosted LLM, reached through an OpenAI-compatible endpoint.
# Defaults to a local Ollama server. Everything in this project also works
# with FORGE_ENDPOINT unset/unreachable — the LLM step is a bonus, not a dependency.
FORGE_ENDPOINT = os.getenv("FORGE_ENDPOINT", "http://localhost:11434/v1")
FORGE_MODEL = os.getenv("FORGE_MODEL", "llama3.2")
FORGE_API_KEY = os.getenv("FORGE_API_KEY", "ollama")

# Public, keyless Wikipedia search API used to find real, publicly documented
# companies and trade organizations. No login, no scraping behind a wall.
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "ai-export-automation/1.0 (https://github.com/warboy176/ai-export-automation)"

HTTP_TIMEOUT_SECONDS = 10
LLM_TIMEOUT_SECONDS = 15

DEFAULT_LEAD_LIMIT = 10
MAX_LEAD_LIMIT = 50
