EXPORT_KEYWORDS = {
    "export": 20,
    "import": 15,
    "trade": 15,
    "trading": 15,
    "logistics": 12,
    "manufacturer": 12,
    "manufacturing": 10,
    "wholesale": 10,
    "freight": 10,
    "shipping": 10,
    "supply chain": 10,
    "distributor": 10,
    "customs": 8,
    "international": 8,
}

HIGH_THRESHOLD = 40
MEDIUM_THRESHOLD = 15


def rule_score(text):
    """Deterministic keyword scoring. No AI, no network, no guessing."""
    text_lower = text.lower()
    score = 0
    hits = []
    for keyword, weight in EXPORT_KEYWORDS.items():
        if keyword in text_lower:
            score += weight
            hits.append(keyword)
    score = min(score, 100)

    if score >= HIGH_THRESHOLD:
        label = "high"
    elif score >= MEDIUM_THRESHOLD:
        label = "medium"
    else:
        label = "low"

    return score, label, hits


def score_lead(lead, llm_fn=None):
    """Score a lead's export potential from its public name/summary text.

    The rule-based score is always computed and is the source of truth —
    this works fully offline. If an llm_fn is supplied (e.g. llm.call_llm,
    or a canned stand-in for tests), its opinion is attached as an extra
    'ai_note' and never changes the score itself.
    """
    text = f"{lead.get('name', '')} {lead.get('summary', '')}"
    score, label, hits = rule_score(text)

    result = dict(lead)
    result["export_score"] = score
    result["export_potential"] = label
    result["matched_keywords"] = hits

    if llm_fn is not None:
        note = llm_fn(
            "You are an export business analyst. In one short sentence, say "
            "whether this organization looks like a good export-business lead "
            "and why.",
            f"Name: {lead.get('name', '')}\nSummary: {lead.get('summary', '')}",
        )
        if note:
            result["ai_note"] = note

    return result
