import html
import json
import re
import time
import urllib.parse
import urllib.request

from config import WIKI_API_URL, USER_AGENT, HTTP_TIMEOUT_SECONDS

_TAG_RE = re.compile(r"<[^>]+>")


def find_leads(query, limit=10, retries=1):
    """Find real, publicly documented organizations for a trade query.

    Uses Wikipedia's public, keyless search API — no login wall, no scraped
    profile data, no private contact info. This is a research/discovery
    tool over public encyclopedia entries, not a sales contact database.
    Retries once on network failure before raising.
    """
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    }
    url = WIKI_API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    last_error = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            results = body.get("query", {}).get("search", [])
            leads = []
            for r in results:
                snippet = html.unescape(_TAG_RE.sub("", r.get("snippet", "")))
                title = r["title"]
                leads.append({
                    "name": title,
                    "source": "wikipedia",
                    "summary": snippet,
                    "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                })
            return leads
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(1)

    raise RuntimeError(
        f"could not reach the Wikipedia search API after {retries + 1} attempt(s): {last_error}"
    )
