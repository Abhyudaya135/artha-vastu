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
print("\n".join(err) if err else "OK")
if err: sys.exit(1)

# ---- extension file: markets, regulations, approvals ----
import os
if os.path.exists("artha-vastu-ext.json"):
    e = json.load(open("artha-vastu-ext.json", encoding="utf-8"))
    err2 = []
    for k in ["markets", "assumptions_extra", "reg_documents", "regulations", "reg_updates", "approvals", "approval_docs", "jurisdictions"]:
        if not isinstance(e.get(k), list) or not e[k]: err2.append(f"ext: {k} missing or empty")
    if not re.match(r"^\d{4}-\d{2}-\d{2}", str(e.get("edition", ""))): err2.append("ext: edition must start YYYY-MM-DD")
    for k, key in [("reg_documents", "doc_id"), ("regulations", "reg_id"), ("reg_updates", "upd_id"), ("approvals", "key"), ("approval_docs", "doc_key")]:
        ids = [r.get(key) for r in e.get(k, [])]
        if len(ids) != len(set(ids)): err2.append(f"ext: duplicate {key} in {k}")
    docs = {d["doc_id"] for d in e.get("reg_documents", [])}
    for r in e.get("regulations", []):
        if r.get("doc_id") not in docs: err2.append(f"ext: regulation {r.get('reg_id')} points to unknown document")
        if not str(r.get("url", "")).startswith("http"): err2.append(f"ext: regulation {r.get('reg_id')} needs a source URL")
    keys = {a["key"] for a in e.get("approvals", [])}
    for a in e.get("approvals", []):
        for d in filter(None, a.get("depends_on", "").split(",")):
            if f"{a['jid']}:{d}" not in keys: err2.append(f"ext: {a['key']} depends on unknown {d}")
    if err2:
        print("\n".join(err2)); sys.exit(1)
    print("EXT OK")
