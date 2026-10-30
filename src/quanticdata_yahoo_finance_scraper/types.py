"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class YahooFinanceRow(TypedDict, total=False):
    """One row of `yahoo-finance-scraper quote` (yahoo_finance v1.1.1)."""

    rank: int
    """1-based position."""
    symbol: str
    """Ticker symbol."""
    name: Optional[str]
    """Instrument name."""
    price: Optional[float]
    """Current price."""
    currency: Optional[str]
    """Price currency."""
    exchange: Optional[str]
    """Exchange."""
    instrument_type: Optional[str]
    """EQUITY, ETF, INDEX, CURRENCY…"""
    previous_close: Optional[float]
    """Previous close."""
    day_high: Optional[float]
    """Session high."""
    day_low: Optional[float]
    """Session low."""
    fifty_two_week_high: Optional[float]
    """52-week high."""
    fifty_two_week_low: Optional[float]
    """52-week low."""
    volume: Optional[int]
    """Regular-market volume."""
    market_time: Optional[str]
    """Quote timestamp (ISO 8601)."""
    timezone: Optional[str]
    """Exchange timezone."""
    range: Optional[str]
    """History range returned."""
    history: List[Dict[str, Any]]
    """OHLCV points { date, open, high, low, close, volume }, the last 120 of the range; empty unless --include-history is on."""
    change: Optional[float]
    """Price minus previous_close."""
    change_percent: Optional[float]
    """Change against previous_close, in percent."""
    first_trade_date: Optional[str]
    """First trading day of the instrument (YYYY-MM-DD)."""
    url: str
    """Yahoo Finance quote page."""
