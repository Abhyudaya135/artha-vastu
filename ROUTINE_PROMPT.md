# Artha-Vāstu daily refresh (paste everything below into the routine's prompt)

You maintain Artha-Vāstu, an India real estate assumption book published from this repository with GitHub Pages. The page (index.html) reads `artha-vastu-data.json`; you only ever edit that JSON file and CHANGELOG.md. Never edit index.html or validate.py.

Today, do the following, using web search and fetching original pages. Work only from sources you actually opened in this run; never invent a figure, date, deal or headline.

1. **News (every day).** Find real estate stories from the last 7 days for India and for each city in the file: Mumbai (MMR), Bengaluru, Delhi NCR, Hyderabad, Pune, Chennai, Kolkata, and where possible their micro-markets as named in the `micro` values already in the file. Cover office leasing, residential launches and sales, land deals, REITs and investment, warehousing, retail, hotels and infrastructure that affects real estate. Add each new story as a `news` row: a new `news_id` (next N number), ISO `date`, `city` ("" for national), `micro` ("" if none, otherwise exactly an existing micro value), `category` (one of Office, Residential, Land, Capital markets, Warehousing, Retail, Hospitality, Infrastructure), a `headline` and a one- or two-sentence `summary` written in your own words (no quotes longer than a few words), `source` (publication name) and the article `url`. Skip duplicates of stories already in the file. Keep at most the 80 most recent rows; drop the oldest.

2. **Rates (every day).** Check the RBI repo rate and the 10-year G-sec yield. If either has changed from the `base` of rows `IN-DEBT-REPO` / `IN-DEBT-GSEC`, update `base` (and `low`/`high` if the change moves outside them), `as_of`, and add a sentence to `rationale` with the new source appended to `sources` in the format `Label|URL` separated by `;;`. Append a point to the matching `trends` series (`in-repo`, `in-gsec`) for the current month if the month is not already there; otherwise update that month's value.

3. **Market data (every day, but most days nothing changes).** Look for newly published quarterly or half-yearly reports and deals: JLL, CBRE, Colliers, Cushman & Wakefield, Knight Frank, Anarock, Vestian, CRE Matrix and Propstack registrations, REIT valuation reports and NCD issues, HVS Anarock hotel monitors. Only when a source publishes a newer figure than the row's `as_of`:
   - update that assumption's `low`/`base`/`high`, `as_of`, `rationale` and `sources`, keeping the house approach: base cases are judgements that weigh two or more sources, and `confidence` is "High: multiple sources" only when at least two independent sources agree;
   - add newly registered office leases with a reported rent to `deals` (next D number), using an existing city and micro value;
   - append the new data point to the matching `trends` series with `basis` "Reported" (or "Derived from reported …" if back-calculated).
   Do not change a number just because a blog or listing site quotes a different asking rent.

4. **Edition and log.** Set `edition` to today's date and time in IST as `YYYY-MM-DDTHH:MM` (it must sort later than the previous value). Add one dated line per change to the top of CHANGELOG.md, naming the row id and the source. If nothing changed except news, say so.

5. **Check and publish.** Run `python3 validate.py`. If it prints anything other than OK, fix the JSON and run it again; if you cannot fix it, discard your changes and write the problem into CHANGELOG.md only. When it prints OK, commit to the default branch with the message `Daily refresh <edition>` and push.

Keep the JSON's structure, field names and existing ids exactly as they are, and keep it UTF-8 with Indian rupee symbols intact.
