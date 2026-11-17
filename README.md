<img src="cover.png" alt="ai-export-automation" width="100%">

# ai-export-automation

**A free rebuild of the "AI finds you 1,000 export customers a day" pitch, minus the login-walled scraping and the paid API.**

An Instagram post claimed a founder automated 80% of an export business with AI: videos that cost pennies, and AI that finds up to 1,000 customers a day. That's the trend — AI-run lead generation and outreach for small export/trading businesses. This is the honest, open-source version of the pipeline: it searches public, keyless data for real organizations in a trade niche, scores them with transparent rules, and drafts an outreach script for each one. No LinkedIn scraping, no paid OpenAI key required, no made-up numbers.

## What it does

1. **Finds leads** (`finder.py`) — queries Wikipedia's public search API for a trade query (e.g. `"textile exporter Vietnam"`) and returns real, publicly documented organizations and topics, no login required.
2. **Scores them** (`scorer.py`) — rule-based keyword scoring (export, trade, logistics, customs, etc.) gives every lead a transparent 0-100 score and a high/medium/low label. Fully deterministic, no AI required.
3. **Drafts a script** (`script_writer.py`) — writes a ~25-second talking-head outreach script (hook, body, CTA) for each lead from a small template library. Costs $0 — it's text, not a rendered video.
4. **Exports results** (`exporter.py`) — writes `exported_leads.csv` and `exported_leads.json`.
5. Optionally, if you point it at a local model, it'll ask the model to punch up the hook line and add a one-line note per lead. This is entirely optional and off by default behavior degrades to pure rule-based output if no model is reachable.

## Run it

```
pip install -r requirements.txt   # no third-party deps, this just confirms Python
python3 main.py "textile exporter Vietnam" --limit 10
python3 selftest.py
```

To try the optional local-LLM polish (requires [Ollama](https://ollama.com) running locally, or any OpenAI-compatible endpoint):

```
ollama pull llama3.2
python3 main.py "coffee exporter Colombia" --limit 10
```

To skip the LLM step entirely:

```
python3 main.py "textile exporter Vietnam" --no-llm
```

## What it is not

- **Not a LinkedIn scraper.** It never touches a site behind a login wall. It searches public Wikipedia data only.
- **Not a contact database.** Results are organizations and topics with public summaries and URLs — no emails, no phone numbers, no private data.
- **Not a video generator.** `script_writer.py` writes text scripts. Turning a script into an actual talking-head video needs a separate TTS/avatar tool (several free, local ones exist) — that step isn't included here.
- **Not a 1,000-leads-a-day machine.** See below.
- **Not a sales-automation or spam tool.** It drafts one script per lead for a human to use or discard. It does not send messages, DM anyone, or place orders.

## The honest limits

- "AI finds up to 1,000 customers a day" is marketing. A single Wikipedia search query realistically returns a handful to a few dozen relevant results (`--limit` caps it, capped again at 50) — not 1,000, and not all of them are "customers," some are just topic articles.
- Wikipedia search is a blunt instrument for lead generation. It's reliable and free, but it was built to find encyclopedia articles, not warm sales prospects. Treat it as a research starting point, not a verified prospect list.
- The $0 script cost is real because nothing here calls a paid API or renders video. The moment you turn a script into an actual video with voice and a face, that step has its own real cost — this project doesn't include or hide that.
- Scoring is keyword-based. It will misjudge anything that doesn't mention trade-flavored words in its summary, and it has no idea whether a lead is still in business.

## How it fits together

| File | Role |
|---|---|
| `config.py` | Env-driven settings: optional LLM endpoint, Wikipedia API URL, timeouts, lead limits |
| `finder.py` | Queries the public Wikipedia search API for leads, with one retry on failure |
| `scorer.py` | Rule-based export-potential scoring (0-100, high/medium/low) |
| `script_writer.py` | Template-based outreach script generator, optional LLM hook rewrite |
| `exporter.py` | Writes results to CSV and JSON |
| `llm.py` | Thin client for any OpenAI-compatible endpoint (Ollama by default); returns `None` if unreachable |
| `main.py` | Orchestrates find → score → write script → export, prints a summary |
| `selftest.py` | End-to-end checks with a canned model reply — no real LLM calls, prints `SELFTEST PASS` |

Built by Warboy. Free, and it stays free.
