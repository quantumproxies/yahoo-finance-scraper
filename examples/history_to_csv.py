"""OHLCV price history of a list of tickers, in one long-format CSV.

    python history_to_csv.py AAPL MSFT ^GSPC --range 1y --interval 1wk

Writes price_history.csv with one row per symbol and date (open, high, low,
close, volume). Each series holds the last 120 points of the range: a year of
weekly candles fits whole, a year of daily candles keeps the latest 120.
"""

import argparse

from quanticdata_yahoo_finance_scraper import YahooFinanceScraper, write

RANGES = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
INTERVALS = ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("symbols", nargs="+")
    parser.add_argument("--range", default="6mo", choices=RANGES)
    parser.add_argument("--interval", default="1d", choices=INTERVALS)
    parser.add_argument("--out", default="price_history.csv")
    args = parser.parse_args()

    yahoo = YahooFinanceScraper()
    rows = []
    for i in range(0, len(args.symbols), 50):
        batch = args.symbols[i:i + 50]
        run = yahoo.quote(batch, range=args.range, interval=args.interval, include_history=True,
                          max_results=len(batch))
        for quote in run:
            points = quote.get("history") or []
            rows.extend({"symbol": quote["symbol"], "currency": quote.get("currency"), **p} for p in points)
            print(f"{quote['symbol']}: {len(points)} points")

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()
