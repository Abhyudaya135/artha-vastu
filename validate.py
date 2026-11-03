"""Checks artha-vastu-data.json before a routine commits it. Exit code 1 means do not commit."""
import json, re, sys
d = json.load(open("artha-vastu-data.json", encoding="utf-8"))
err = []
if not re.match(r"^\d{4}-\d{2}-\d{2}", str(d.get("edition", ""))): err.append("edition must start YYYY-MM-DD")
need = {"assumptions": ["id","city","micro","level","category","parameter","segment","unit","low","base","high","confidence","as_of","rationale","sources","deal_asset","kpi"],
        "deals": ["deal_id","asset","city","micro","tenant","building","area_sqft","rent_psf","tenure_yrs","escalation","rent_free","deposit","date","source","url","note"],
        "trends": ["series_id","scope","micro","parameter","unit","period","value","basis","source","url"],
        "news": ["news_id","date","city","micro","category","headline","summary","source","url"]}
for k, cols in need.items():
    rows = d.get(k)
    if not isinstance(rows, list) or not rows: err.append(f"{k} missing or empty"); continue
    keyf = cols[0]; seen = set()
    for i, r in enumerate(rows):
        miss = [c for c in cols if c not in r]
        if miss: err.append(f"{k}[{i}] missing {miss}")
        key = (r.get("series_id"), r.get("period")) if k == "trends" else r.get(keyf)
        if key in seen: err.append(f"{k} duplicate key {key}")
        seen.add(key)
for r in d.get("assumptions", []):
    for f in ("low","base","high"):
        if r.get(f) is not None and not isinstance(r[f], (int, float)): err.append(f"{r['id']}.{f} not numeric")
    if not r.get("sources"): err.append(f"{r['id']} has no sources")
for n in d.get("news", []):
    if not str(n.get("url","")).startswith("http"): err.append(f"news {n.get('news_id')} needs a real URL")
if len(d.get("assumptions", [])) < 140: err.append("assumptions shrank below 140 rows; refusing")
print("\n".join(err) if err else "OK"); sys.exit(1 if err else 0)
