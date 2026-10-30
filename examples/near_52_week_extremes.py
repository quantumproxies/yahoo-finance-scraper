"""Which symbols trade near their 52-week high or low.

    python near_52_week_extremes.py AAPL MSFT NVDA AMZN GOOGL META --within 5

Prints each symbol's distance from its 52-week high and low, in percent, and
writes the ones within --within percent of either end to near_extremes.csv.
"""

import argparse

from quanticdata_yahoo_finance_scraper import YahooFinanceScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("symbols", nargs="+")
    parser.add_argument("--within", type=float, default=5.0, help="percent from the 52-week high or low")
    parser.add_argument("--out", default="near_extremes.csv")
    args = parser.parse_args()

    yahoo = YahooFinanceScraper()
    flagged = []
    for i in range(0, len(args.symbols), 50):
        batch = args.symbols[i:i + 50]
        for q in yahoo.quote(batch, max_results=len(batch)):
            price, high, low = q.get("price"), q.get("fifty_two_week_high"), q.get("fifty_two_week_low")
            if not price or not high or not low:
                print(f"{q['symbol']:10} no 52-week range in the quote")
                continue
            below_high = (high - price) / high * 100
            above_low = (price - low) / low * 100
            flag = "near high" if below_high <= args.within else "near low" if above_low <= args.within else ""
            print(f"{q['symbol']:10} {price:>12,.2f}  {below_high:5.1f}% below high  {above_low:6.1f}% above low  {flag}")
            if flag:
                flagged.append({"symbol": q["symbol"], "name": q.get("name"), "price": price, "flag": flag,
                                "pct_below_high": round(below_high, 2), "pct_above_low": round(above_low, 2),
                                "fifty_two_week_high": high, "fifty_two_week_low": low})

    write(flagged, args.out)
    print(f"{len(flagged)} of {len(args.symbols)} symbols written to {args.out}")


if __name__ == "__main__":
    main()
