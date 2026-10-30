# Yahoo Finance Scraper

[![ci](https://github.com/quantumproxies/yahoo-finance-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/yahoo-finance-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Yahoo Finance from Python or the command line: the quote of any ticker symbol (stocks, ETFs, indices such as ^GSPC, currency pairs such as EURUSD=X) with price, change, volume, day range and 52-week range, and on request its OHLCV price history, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/yahoo-finance-scraper
yahoo-finance-scraper login
yahoo-finance-scraper quote AAPL MSFT NVDA -o quotes.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=yahoo-finance-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `yahoo-finance-scraper quote` | ticker symbols | Price, change, volume, day and 52-week range, OHLCV history, 21 fields per row ([fields and price](https://quanticdata.io/collectors/stock-data-api/?utm_source=github&utm_medium=readme&utm_campaign=yahoo-finance-scraper)) | up to 50 |

`--include-history` adds the OHLCV series (the last 120 points) to every row: pick its span with `--range` (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max) and its candle with `--interval` (1m, 5m, 15m, 1h, 1d, 1wk, 1mo). Each row states its `instrument_type` (EQUITY, ETF, INDEX, CURRENCY) and the `currency` of its prices.

## Sample output

A real row from `yahoo-finance-scraper quote AAPL MSFT NVDA --max-results 3` (2026-10-23):

```json
{
  "url": "https://finance.yahoo.com/quote/AAPL",
  "name": "Apple Inc.",
  "rank": 1,
  "price": 348.22,
  "range": "1mo",
  "change": 4.23,
  "symbol": "AAPL",
  "volume": 46845411,
  "day_low": 342.28,
  "history": [],
  "currency": "USD",
  "day_high": 348.36,
  "exchange": "NasdaqGS",
  "timezone": "America/New_York",
  "market_time": "2026-10-22T20:00:01.000Z",
  "change_percent": 1.23,
  "previous_close": 343.99,
  "instrument_type": "EQUITY",
  "first_trade_date": "1980-12-12",
  "fifty_two_week_low": 243.42,
  "fifty_two_week_high": 348.36
}
```

## Python

```python
from quanticdata_yahoo_finance_scraper import YahooFinanceScraper

yahoo = YahooFinanceScraper()  # saved login, or QUANTICDATA_API_KEY

quotes = yahoo.quote(["AAPL", "MSFT", "NVDA", "^GSPC", "EURUSD=X"])
for q in quotes:
    print(q["symbol"], q["price"], q["currency"], q["change_percent"], q["volume"])
quotes.to_csv("quotes.csv")

tsla = yahoo.quote(["TSLA"], range="1y", interval="1wk", include_history=True)
for point in tsla.rows[0]["history"]:
    print(point["date"], point["close"], point["volume"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Watchlist snapshots**: Read a watchlist file and append each symbol's price, change, volume and 52-week range to a CSV with a timestamp, from cron after the close. See [`examples/watchlist_snapshot.py`](examples/watchlist_snapshot.py).
- **Price history to CSV**: Download the OHLCV series of a list of tickers for a range and candle size into one long-format CSV, one row per symbol and date, ready for pandas or a spreadsheet chart. See [`examples/history_to_csv.py`](examples/history_to_csv.py).
- **52-week range screen**: Flag the symbols of a list that trade within a few percent of their 52-week high or low. See [`examples/near_52_week_extremes.py`](examples/near_52_week_extremes.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `yahoo-finance-scraper run <id> -o out.csv` collects it later.

### `yahoo-finance-scraper quote`

Quote of each ticker symbol: price, change, volume, day and 52-week range, exchange and currency, with the OHLCV price history when --include-history is on.

```
yahoo-finance-scraper quote SYMBOLS [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `SYMBOLS` | string[] |  | Ticker symbols as Yahoo Finance writes them, e.g. AAPL, MSFT, ^GSPC, EURUSD=X. |
| `--range` | 1d / 5d / 1mo / 3mo / 6mo / 1y / 2y / 5y / 10y / ytd / max | `1mo` | How far back the price history goes when --include-history is on. |
| `--interval` | 1m / 5m / 15m / 1h / 1d / 1wk / 1mo | `1d` | Candle size of the price history. |
| `--include-history` | boolean | `False` | Attach the OHLCV price history (the last 120 points) to each row. |
| `--max-results` | integer | `10` | How many symbols to deliver at most (1–50). Set it to the number of symbols you send when that is more than 10. You pay only for delivered symbols. |

## Output fields

<details><summary><code>yahoo-finance-scraper quote</code>: 21 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `symbol` | string | Ticker symbol. |
| `name` | string or null | Instrument name. |
| `price` | number or null | Current price. |
| `currency` | string or null | Price currency. |
| `exchange` | string or null | Exchange. |
| `instrument_type` | string or null | EQUITY, ETF, INDEX, CURRENCY… |
| `previous_close` | number or null | Previous close. |
| `day_high` | number or null | Session high. |
| `day_low` | number or null | Session low. |
| `fifty_two_week_high` | number or null | 52-week high. |
| `fifty_two_week_low` | number or null | 52-week low. |
| `volume` | integer or null | Regular-market volume. |
| `market_time` | string or null | Quote timestamp (ISO 8601). |
| `timezone` | string or null | Exchange timezone. |
| `range` | string or null | History range returned. |
| `history` | object[] | OHLCV points { date, open, high, low, close, volume }, the last 120 of the range; empty unless --include-history is on. |
| `change` | number or null | Price minus previous_close. |
| `change_percent` | number or null | Change against previous_close, in percent. |
| `first_trade_date` | string or null | First trading day of the instrument (YYYY-MM-DD). |
| `url` | string | Yahoo Finance quote page. |

</details>

## Sign-in and API keys

- `yahoo-finance-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `yahoo-finance-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `yahoo-finance-scraper login --api-key`.
- `yahoo-finance-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=yahoo-finance-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/yahoo_finance/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"symbols": ["AAPL", "MSFT", "NVDA"], "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=yahoo-finance-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=yahoo-finance-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Yahoo Finance scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send ticker symbols and get rows back; the requests run on QuanticData's side. There is no Yahoo account or cookie to set up either.

**Which symbols does it accept?**

The symbols Yahoo Finance uses on its quote pages: stocks such as AAPL, ETFs, indices with a caret such as ^GSPC and currency pairs ending in =X such as EURUSD=X. The instrument_type field says which kind each row is.

**How many symbols can one run return?**

Up to 50 symbols per run, 10 by default: raise it with --max-results and you pay only for what is delivered. With --include-history each row also carries the last 120 points of its price series.

**Can I export to CSV or Excel?**

Add -o quotes.csv (or .json, .jsonl) and the file opens cleanly in Excel or Google Sheets. The price history is a nested list; examples/history_to_csv.py turns it into one row per symbol and date.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/watchlist_snapshot.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Financial Data API](https://github.com/quantumproxies/financial-data-api): Financial data API for Python and the command line.
- [Google SERP API](https://github.com/quantumproxies/google-serp-api): Google SERP API for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=yahoo-finance-scraper).
