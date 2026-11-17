# The "AI finds 1,000 export customers a day" post, rebuilt free

An Instagram account posted that a founder automated 80% of his export business with AI — ten videos for $1.40, AI finding up to 1,000 customers a day, comment "PLAYBOOK" for the next steps. No code, no repo, just a DM funnel.

So I built the real thing and gave it away.

`ai-export-automation` is a small Python pipeline that searches Wikipedia's public, keyless API for real organizations in a trade niche, scores each one with transparent keyword rules (export, trade, logistics, customs — no black box), and drafts a short talking-head outreach script per lead. Point it at a local model through any OpenAI-compatible endpoint (Ollama by default) and it'll punch up the hook line too. Skip that and it still works, pure rule-based, zero API cost.

What it is not: it's not a LinkedIn scraper, it doesn't touch anything behind a login wall, it doesn't hold contact databases, and it doesn't send a single message on your behalf. It finds public leads and writes scripts. A human still decides who to contact and how. And it does not find 1,000 customers a day — that number was always marketing. A real search returns a handful to a few dozen relevant hits, and some of those are just background articles, not warm prospects. I'd rather tell you that than sell you a fantasy.

`selftest.py` proves every piece works end to end — the finder, the scorer, the script writer, the export — with a canned model reply so the test never depends on a live API.

Code: https://github.com/warboy176/ai-export-automation

This is free and it stays free. If enough of you want a real V2 — better scoring, a proper lead-quality signal, actual video rendering — I'll build it properly and that's when a paid tier might show up. Not before. Not as a teaser.

Witness me.
