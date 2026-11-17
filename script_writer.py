import re

HOOK_TEMPLATES = [
    "Attention {name} — you might already be losing export deals without knowing it.",
    "If you work with {name}, this is the 30 seconds that could save a shipment.",
    "{name}: here's what most export buyers get wrong on their first order.",
]

BODY_LINES = [
    "We looked at the public record and your trade footprint fits international buyers.",
    "Keyword match: {keywords}.",
    "A script like this one costs nothing to write — only a render costs money, and that's optional.",
]

CTA_LINE = "Reply to this video or check the link in bio to talk logistics."

WORDS_PER_SECOND = 2.5


def _pick_hook(name):
    # Deterministic pick (not hash()) so the same lead always gets the same hook.
    index = sum(ord(c) for c in name) % len(HOOK_TEMPLATES)
    return HOOK_TEMPLATES[index].format(name=name or "there")


def build_template_script(lead):
    keywords = ", ".join(lead.get("matched_keywords") or ["general trade"])
    hook = _pick_hook(lead.get("name", ""))
    body = [line.format(keywords=keywords) for line in BODY_LINES]
    return [hook] + body + [CTA_LINE]


def estimate_seconds(lines, words_per_second=WORDS_PER_SECOND):
    words = sum(len(re.findall(r"\S+", line)) for line in lines)
    return round(words / words_per_second, 1)


def generate_script(lead, llm_fn=None):
    """Draft a short talking-head outreach script for a lead.

    Template-only mode works offline and costs $0 — no video is rendered,
    only the script text. If llm_fn is supplied, it may punch up the hook
    line; everything else stays the same either way.
    """
    lines = build_template_script(lead)

    if llm_fn is not None:
        rewritten_hook = llm_fn(
            "You write blunt, punchy one-line hooks for 30-second talking-head "
            "sales videos. Rewrite the given hook in under 20 words, no hashtags.",
            lines[0],
        )
        if rewritten_hook:
            lines[0] = rewritten_hook.strip()

    return {
        "lines": lines,
        "estimated_seconds": estimate_seconds(lines),
        "estimated_cost_usd": 0.0,
    }
