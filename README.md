# Yahoo Finance market data API — examples

Live quote + history for stocks, ETFs and indices — price, volume, day and 52-week range.

**Live page, full schema & pricing → [quanticdata.io/collectors/stock-data-api/](https://quanticdata.io/collectors/stock-data-api/)**

One row per ticker from Yahoo Finance: current price, currency, exchange, previous close, day high/low, 52-week high/low, volume and quote time. Optionally attach the OHLCV history for the requested range. Reads Yahoo's public chart endpoint — no API key, no per-request cap to manage. Works for equities, ETFs, indices (^GSPC) and FX pairs (EURUSD=X).

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/yahoo_finance/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "NVDA"], "max_results": 3}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `symbols` (array, required) — Ticker symbols, e.g. AAPL, MSFT, ^GSPC, EURUSD=X.
- `range` (string) — History range when include_history is on.
- `interval` (string) — History candle interval.
- `include_history` (boolean) — Attach the OHLCV series (last 120 points) to each row.
- `max_results` (integer) — How many symbols to deliver at most (1–50). You pay only for delivered symbols.

## Output — one row per quote

| field | type | description |
|---|---|---|
| `symbol` | string | Ticker symbol. |
| `name` | string | Instrument name. |
| `price` | number | Current price. |
| `currency` | string | Price currency. |
| `exchange` | string | Exchange. |
| `instrument_type` | string | EQUITY, ETF, INDEX, CURRENCY… |
| `previous_close` | number | Previous close. |
| `day_high` | number | Session high. |
| `day_low` | number | Session low. |
| `fifty_two_week_high` | number | 52-week high. |
| `fifty_two_week_low` | number | 52-week low. |
| `volume` | integer | Regular-market volume. |
…and 4 more fields — full schema on the [live page](https://quanticdata.io/collectors/stock-data-api/).

## Pricing

**$0.001 per delivered quote** ($1 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 2,000 quotes — no card required.

## Links

- This collector: https://quanticdata.io/collectors/stock-data-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
