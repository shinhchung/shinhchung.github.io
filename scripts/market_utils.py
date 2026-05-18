#!/usr/bin/env python3
"""Shared utilities for morning brief and stage 2 radar scripts."""

import datetime as dt
import json
import urllib.parse
import urllib.request
from pathlib import Path

YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?{query}"
DEFAULT_BENCHMARK = "SPY"


def get_text(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "ignore")


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_chart(symbol: str, years: int = 1, min_rows: int = 2):
    """Fetch daily price data from Yahoo Finance.

    Returns list of dicts with keys: ts, close, adjclose, volume.
    """
    end = int(dt.datetime.now(dt.timezone.utc).timestamp())
    start = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365 * years + 20)).timestamp())
    query = urllib.parse.urlencode(
        {
            "period1": start,
            "period2": end,
            "interval": "1d",
            "includeAdjustedClose": "true",
            "events": "div,splits",
        }
    )
    data = get_json(YAHOO_CHART.format(symbol=urllib.parse.quote(symbol), query=query))
    result = data["chart"]["result"][0]
    timestamps = result.get("timestamp") or []
    quote = ((result.get("indicators") or {}).get("quote") or [{}])[0]
    adjclose = ((result.get("indicators") or {}).get("adjclose") or [{}])[0].get("adjclose") or []
    closes = quote.get("close") or []
    volumes = quote.get("volume") or []
    rows = []
    for ts, close, adj, vol in zip(timestamps, closes, adjclose, volumes):
        if close is None or adj is None:
            continue
        rows.append({"ts": ts, "close": close, "adjclose": adj, "volume": vol or 0})
    if len(rows) < min_rows:
        raise ValueError(f"Not enough chart data for {symbol}")
    return rows


def load_tickers(path: Path):
    """Load ticker symbols from a text file (one per line, or comma/space separated)."""
    text = path.read_text(encoding="utf-8")
    out, seen = [], set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for token in line.replace(",", " ").split():
            token = token.strip().upper()
            if token and token not in seen:
                seen.add(token)
                out.append(token)
    return out


def total_return(rows):
    """Calculate total return from a list of price rows."""
    return rows[-1]["adjclose"] / rows[0]["adjclose"] - 1.0


def annualized_return(rows):
    """Calculate annualized return from a list of price rows."""
    start_ts = rows[0]["ts"]
    end_ts = rows[-1]["ts"]
    years = max((end_ts - start_ts) / (365.25 * 24 * 3600), 0.01)
    tr = total_return(rows)
    return (1 + tr) ** (1 / years) - 1


def sma(values, window):
    """Simple moving average of the last `window` values."""
    return sum(values[-window:]) / window if len(values) >= window else None


def fmt_pct(x):
    return f"{x * 100:.1f}%"
