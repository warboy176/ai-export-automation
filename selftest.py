import json
import os
import sys

from finder import find_leads
from scorer import score_lead
from script_writer import generate_script
from exporter import export_leads

# Clearly-labelled canned reply - selftest never calls a real model.
CANNED_LLM_REPLY = "CANNED: strong export fit, trades internationally."


def canned_llm(system_prompt, user_prompt, max_tokens=120):
    return CANNED_LLM_REPLY


def check(label, condition):
    print(f"[{'ok' if condition else 'FAIL'}] {label}")
    return condition


def main():
    results = []

    # 1. Real network call to a public, keyless source (Wikipedia search API).
    #    find_leads() retries once internally before raising.
    try:
        leads = find_leads("export trading company", limit=5)
    except Exception as e:
        print(f"[FAIL] finder.find_leads could not reach Wikipedia: {e}")
        leads = []

    results.append(check("finder returns at least one real lead", len(leads) >= 1))
    results.append(check(
        "every lead has a name and a url",
        bool(leads) and all(lead.get("name") and lead.get("url") for lead in leads),
    ))

    # 2. Rule-based scoring is deterministic and needs no network or LLM.
    hot_lead = {
        "name": "Acme Export Trading Co",
        "summary": "An international trading and logistics company handling export and import of manufactured goods.",
    }
    cold_lead = {
        "name": "Riverside Garden Club",
        "summary": "A local hobby club for gardeners.",
    }
    hot_scored = score_lead(hot_lead)
    cold_scored = score_lead(cold_lead)

    results.append(check(
        "export-flavoured text scores higher than unrelated text",
        hot_scored["export_score"] > cold_scored["export_score"],
    ))
    results.append(check(
        "export-flavoured text is labelled medium/high",
        hot_scored["export_potential"] in ("medium", "high"),
    ))
    results.append(check(
        "unrelated text is labelled low",
        cold_scored["export_potential"] == "low",
    ))

    # 3. Scoring with a canned LLM note attached - no real model call.
    noted = score_lead(hot_lead, llm_fn=canned_llm)
    results.append(check(
        "canned LLM note is attached without changing the rule score",
        noted.get("ai_note") == CANNED_LLM_REPLY
        and noted["export_score"] == hot_scored["export_score"],
    ))

    # 4. Script generation, template-only: zero LLM, zero network, zero cost.
    script = generate_script(hot_scored)
    results.append(check("template script has a hook, body and CTA", len(script["lines"]) >= 3))
    results.append(check("script cost is $0 (text only, no paid API)", script["estimated_cost_usd"] == 0.0))
    results.append(check("script duration estimate is positive", script["estimated_seconds"] > 0))

    # 5. Script generation with a canned LLM rewrite of the hook line.
    llm_script = generate_script(hot_scored, llm_fn=canned_llm)
    results.append(check(
        "canned LLM reply replaces the hook line",
        llm_script["lines"][0] == CANNED_LLM_REPLY,
    ))

    # 6. Export to CSV + JSON and read both back.
    csv_path = "selftest_leads.csv"
    json_path = "selftest_leads.json"
    sample = [dict(hot_scored, script=script)]
    rows = export_leads(sample, csv_path=csv_path, json_path=json_path)

    results.append(check("exporter returns one row", len(rows) == 1))
    results.append(check("csv file was written", os.path.exists(csv_path)))
    results.append(check("json file was written", os.path.exists(json_path)))

    with open(json_path, encoding="utf-8") as f:
        reloaded = json.load(f)
    results.append(check("json round-trips the lead name", reloaded[0]["name"] == hot_lead["name"]))

    os.remove(csv_path)
    os.remove(json_path)

    if all(results):
        print("SELFTEST PASS")
        return 0

    print("SELFTEST FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
