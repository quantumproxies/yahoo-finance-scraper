"""Yahoo Finance Scraper: Yahoo Finance scraper for Python and the command line: live quotes for stocks, ETFs, indices and currency pairs with price, change, volume, day and 52-week range, plus OHLCV price history, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_yahoo_finance_scraper import YahooFinanceScraper

    scraper = YahooFinanceScraper()   # saved login (`yahoo-finance-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.quote(...)   # quote and optional price history for one or more ticker symbols
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["YahooFinanceScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class YahooFinanceScraper:
    """Yahoo Finance Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="yahoo-finance-scraper/0.1.0 (+https://github.com/quantumproxies/yahoo-finance-scraper)", timeout=timeout)

    def quote(
        self, symbols: Union[str, Sequence[str]],
        *,
        range: Optional[str] = None,
        interval: Optional[str] = None,
        include_history: Optional[bool] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Quote of each ticker symbol: price, change, volume, day and 52-week range, exchange and currency, with the OHLCV price history when --include-history is on.

        Args:
            symbols: Ticker symbols as Yahoo Finance writes them, e.g. AAPL, MSFT, ^GSPC, EURUSD=X.
            range: How far back the price history goes when --include-history is on. One of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.
            interval: Candle size of the price history. One of: 1m, 5m, 15m, 1h, 1d, 1wk, 1mo.
            include_history: Attach the OHLCV price history (the last 120 points) to each row.
            max_results: How many symbols to deliver at most (1–50). Set it to the number of symbols you send when that is more than 10. You pay only for delivered symbols.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per quote: see ``types.YahooFinanceRow``.
        """
        payload = {
            "symbols": _as_list(symbols),
            "range": range,
            "interval": interval,
            "include_history": include_history,
            "max_results": max_results,
        }
        return self.client.run_collector("yahoo_finance", payload, wait=wait, timeout=timeout)
