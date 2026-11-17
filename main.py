import argparse

from finder import find_leads
from scorer import score_lead
from script_writer import generate_script
from exporter import export_leads
from llm import call_llm
from config import DEFAULT_LEAD_LIMIT, MAX_LEAD_LIMIT


def run(query, limit, use_llm):
    limit = max(1, min(limit, MAX_LEAD_LIMIT))
    print(f"Searching public records for: {query!r} (limit {limit})")

    leads = find_leads(query, limit=limit)
    print(f"Found {len(leads)} candidate organizations.")

    llm_fn = call_llm if use_llm else None

    results = []
    for lead in leads:
        scored = score_lead(lead, llm_fn=llm_fn)
        scored["script"] = generate_script(scored, llm_fn=llm_fn)
        results.append(scored)

    export_leads(results)

    high = sum(1 for r in results if r["export_potential"] == "high")
    medium = sum(1 for r in results if r["export_potential"] == "medium")
    low = sum(1 for r in results if r["export_potential"] == "low")
    total_cost = sum(r["script"]["estimated_cost_usd"] for r in results)

    print(f"Scored: {high} high, {medium} medium, {low} low export potential.")
    print(f"Script cost: ${total_cost:.2f} for {len(results)} scripts (text only, no render).")
    print("Wrote exported_leads.csv and exported_leads.json")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Find public leads, score export potential, draft outreach scripts."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="export trading company",
        help="search query, e.g. 'textile exporter Vietnam'",
    )
    parser.add_argument(
        "--limit", type=int, default=DEFAULT_LEAD_LIMIT, help="max leads to pull"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="skip the optional local-LLM step entirely (rule-based scoring/scripts only)",
    )
    args = parser.parse_args()
    run(args.query, args.limit, use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
