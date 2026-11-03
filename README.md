# Artha-Vāstu (अर्थवास्तु)

India real estate assumption book: cities, micro-markets, rents, cap rates, debt, deals, trends and news.

- `index.html`: the site. It loads `artha-vastu-data.json` whenever that file is newer than its built-in edition, and pulls live Google News headlines for the selected market.
- `artha-vastu-data.json`: all data. A Claude routine refreshes it daily at 9:00 IST (see ROUTINE_PROMPT.md).
- `validate.py`: schema check the routine runs before every commit.
- `CHANGELOG.md`: what changed in each refresh, with sources.
