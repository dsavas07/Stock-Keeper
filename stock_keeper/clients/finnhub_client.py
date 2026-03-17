import json
import os
import time
from typing import Dict, Optional
import requests


class FinnhubClient:
    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key: str, rate_limit_s: float = 0.35, cache_path: Optional[str] = None):
        self.api_key = api_key
        self.rate_limit_s = rate_limit_s
        self._last_call = 0.0
        self.cache_path = cache_path
        if cache_path:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            if not os.path.exists(cache_path):
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump({}, f)

    def _load_cache(self) -> Dict:
        if not self.cache_path or not os.path.exists(self.cache_path):
            return {}
        with open(self.cache_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}

    def _save_cache(self, cache: Dict) -> None:
        if not self.cache_path:
            return
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)

    def _make_cache_key(self, path: str, params: Optional[Dict]) -> str:
        params = params or {}
        sorted_items = sorted(params.items())
        return f"{path}:{sorted_items}"

    def _get(self, path: str, params: Optional[Dict] = None) -> Dict:
        if params is None:
            params = {}
        params["token"] = self.api_key
        key = self._make_cache_key(path, params)

        cache = self._load_cache()
        if key in cache:
            return cache[key]

        now = time.time()
        if now - self._last_call < self.rate_limit_s:
            time.sleep(self.rate_limit_s - (now - self._last_call))
        self._last_call = time.time()
        url = f"{self.BASE_URL}/{path}"
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        cache[key] = data
        self._save_cache(cache)
        return data

    def get_historical_prices(self, symbol: str, from_ts: int, to_ts: int, resolution: str = "D") -> Dict:
        return self._get("stock/candle", {"symbol": symbol, "from": from_ts, "to": to_ts, "resolution": resolution})

    def get_company_profile(self, symbol: str) -> Dict:
        return self._get("stock/profile2", {"symbol": symbol})

    def get_company_basic_financials(self, symbol: str) -> Dict:
        return self._get("stock/metric", {"symbol": symbol, "metric": "all"})

    def get_news(self, symbol: str, from_dt: str, to_dt: str) -> Dict:
        return self._get("company-news", {"symbol": symbol, "from": from_dt, "to": to_dt})
