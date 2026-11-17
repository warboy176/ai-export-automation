import csv
import json

FIELDNAMES = [
    "name",
    "source",
    "url",
    "export_score",
    "export_potential",
    "matched_keywords",
    "script_hook",
    "estimated_seconds",
    "estimated_cost_usd",
]


def export_leads(leads, csv_path="exported_leads.csv", json_path="exported_leads.json"):
    """Write scored leads + scripts to CSV (spreadsheet) and JSON (programmatic)."""
    rows = []
    for lead in leads:
        script = lead.get("script") or {}
        lines = script.get("lines") or []
        rows.append({
            "name": lead.get("name", ""),
            "source": lead.get("source", ""),
            "url": lead.get("url", ""),
            "export_score": lead.get("export_score", 0),
            "export_potential": lead.get("export_potential", ""),
            "matched_keywords": ";".join(lead.get("matched_keywords") or []),
            "script_hook": lines[0] if lines else "",
            "estimated_seconds": script.get("estimated_seconds", 0),
            "estimated_cost_usd": script.get("estimated_cost_usd", 0),
        })

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    return rows
