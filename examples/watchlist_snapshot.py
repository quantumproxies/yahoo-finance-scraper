"""Append a snapshot of a watchlist to a CSV.

Reads ticker symbols from watchlist.txt (one per line), fetches their quote and
appends one row per symbol to quotes_history.csv with a UTC timestamp. Run it
from cron after the close to build a daily history:

    python watchlist_snapshot.py --watchlist watchlist.txt
    30 21 * * 1-5  cd /path/to/here && python watchlist_snapshot.py

Needs a login (`yahoo-finance-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_yahoo_finance_scraper import YahooFinanceScraper

FIELDS = ["checked_at", "symbol", "name", "price", "currency", "change", "change_percent", "volume",
          "day_low", "day_high", "fifty_two_week_low", "fifty_two_week_high", "market_time"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--watchlist", default="watchlist.txt", help="file with one ticker symbol per line")
    parser.add_argument("--out", default="quotes_history.csv")
    args = parser.parse_args()

    with open(args.watchlist, encoding="utf-8") as fh:
        symbols = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    yahoo = YahooFinanceScraper()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        # One run takes up to 50 symbols.
        for i in range(0, len(symbols), 50):
            batch = symbols[i:i + 50]
            for quote in yahoo.quote(batch, max_results=len(batch)):
                writer.writerow({"checked_at": checked_at, **quote})
                written += 1
    print(f"{written} quotes appended to {args.out}")


if __name__ == "__main__":
    main()
