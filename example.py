"""Minimal Yahoo Finance market data API call — one typed row per quote.

Docs & schema: https://quanticdata.io/collectors/stock-data-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/yahoo_finance/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "symbols": [
            "AAPL",
            "MSFT",
            "NVDA"
        ],
        "max_results": 3
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("name"), row.get("price"), row.get("currency"))
print(f"{len(data['results'])} quotes, cost ${data['cost']}")
