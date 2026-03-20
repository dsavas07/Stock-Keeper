import datetime
from typing import Dict, List, Optional
## import numpy as np
import pandas as pd

from stock_keeper.clients.finnhub_client import FinnhubClient
from stock_keeper.data.feature_engineering import compute_returns, compute_volatility, compute_momentum ##, compute_moving_average 
from stock_keeper.data.sentiment import sentiment_score
from stock_keeper.forecasting.forecaster import Forecaster
from stock_keeper.scoring.scorer import build_ticker_signals, compute_score
from stock_keeper.optimization.optimizer import mean_variance_optimize, portfolio_metrics


class PortfolioAgent:
    def __init__(self, api_key: str, window_days: int = 365, cache_path: str = "data/finnhub_cache.json"):
        self.client = FinnhubClient(api_key, cache_path=cache_path)
        self.window_days = window_days

    def _get_price_df(self, symbol: str) -> pd.DataFrame:
        to_ts = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        from_ts = int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=self.window_days)).timestamp())
        data = self.client.get_historical_prices(symbol, from_ts=from_ts, to_ts=to_ts)
        if data.get("s") != "ok":
            raise ValueError(f"No price data for {symbol}")
        df = pd.DataFrame({
            "ts": data["t"],
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"],
            "volume": data["v"],
        })
        df["date"] = pd.to_datetime(df["ts"], unit="s")
        return df.set_index("date")

    def _get_profile(self, symbol: str) -> Dict:
        try:
            return self.client.get_company_profile(symbol)
        except Exception:
            return {}

    def _get_sentiment(self, symbol: str) -> float:
        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)
        news_data = self.client.get_news(symbol, from_dt=start.isoformat(), to_dt=end.isoformat())
        headlines = [item.get("headline", "") for item in news_data if isinstance(item, dict)]
        return sentiment_score(headlines)

    def recommend(
        self,
        symbols: List[str],
        horizon: int = 30,
        risk_appetite: str = "medium",
        weights: Optional[Dict[str, float]] = None,
        max_allocation: float = 0.35,
        min_allocation: float = 0.01,
        top_n: int = 10,
        sector_constraints: Optional[Dict[str, float]] = None,
    ) -> Dict:
        if not symbols:
            return {"error": "No symbols provided"}

        if weights is None:
            weights = {"expected_return": 0.5, "volatility": 0.25, "momentum": 0.2, "sentiment": 0.05}

        data = {}
        scores = {}
        exp_returns = {}
        raw_returns = {}

        sector_map = {}
        for symbol in symbols:
            df = self._get_price_df(symbol)
            if df.empty:
                continue

            returns = compute_returns(df)
            momentum = compute_momentum(df, window=20).iloc[-1] if len(df) > 20 else 0.0
            volatility = compute_volatility(df, window=20).iloc[-1]
            sent = self._get_sentiment(symbol)
            forecast = Forecaster(method="linear", window=90).forecast(df["close"], horizon=horizon)
            expected_return = float(forecast["expected_return"])

            signals = build_ticker_signals(
                expected_return=expected_return,
                volatility=float(volatility),
                momentum=float(momentum),
                risk_appetite=risk_appetite,
            )
            signals["sentiment"] = sent
            score = compute_score(signals, weights)

            profile = self._get_profile(symbol)
            sector = profile.get("finnhubIndustry", "Unknown")
            sector_map[symbol] = sector

            data[symbol] = {
                "expected_return": expected_return,
                "volatility": float(volatility),
                "momentum": float(momentum),
                "sentiment": sent,
                "score": score,
                "sector": sector,
                "forecast_trend": float(forecast.get("trend", 0.0)),
            }
            scores[symbol] = score
            exp_returns[symbol] = expected_return
            raw_returns[symbol] = returns

        tickers = list(scores.keys())
        if not tickers:
            return {"error": "No valid historical data for symbols"}

        returns_df = pd.DataFrame(raw_returns).fillna(0)
        cov = returns_df.cov().fillna(0).values

        allocation = mean_variance_optimize(scores, cov, tickers, max_weight=max_allocation, min_weight=min_allocation)

        # Enforce sector constraints if provided
        if sector_constraints:
            sector_weights = {}
            for symbol, weight in allocation.items():
                sector = sector_map.get(symbol, "Unknown")
                sector_weights.setdefault(sector, 0.0)
                sector_weights[sector] += weight

            for sector, cap in sector_constraints.items():
                if sector_weights.get(sector, 0.0) > cap:
                    excess = sector_weights[sector] - cap
                    # reduce all symbols in that sector proportionally
                    names = [s for s in tickers if sector_map.get(s) == sector]
                    if names:
                        for name in names:
                            reduction = min(allocation[name], allocation[name] * (excess / sector_weights[sector]))
                            allocation[name] = max(min_allocation, allocation[name] - reduction)

            # renormalize
            total = sum(allocation.values())
            if total > 0:
                for symbol in allocation:
                    allocation[symbol] = allocation[symbol] / total

        # fallback to topN scoring if optimization outputs invalid
        if any(w <= 0 for w in allocation.values()) or abs(sum(allocation.values()) - 1.0) > 1e-6:
            top_symbols = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:top_n]
            fallback = {s: 1.0 / len(top_symbols) for s in top_symbols}
            for s in scores:
                allocation[s] = fallback.get(s, 0.0)

        metrics = portfolio_metrics(allocation, exp_returns, cov, tickers)
        risk_notes = []
        if metrics["volatility"] > 0.2 and risk_appetite == "low":
            risk_notes.append("High portfolio volatility for low risk appetite.")
        if metrics["expected_return"] < 0:
            risk_notes.append("Negative expected return. Consider safer assets or longer horizon.")

        return {
            "request": {
                "symbols": symbols,
                "horizon_days": horizon,
                "risk_appetite": risk_appetite,
                "weights": weights,
                "sector_constraints": sector_constraints,
                "top_n": top_n,
            },
            "scores": data,
            "allocation": allocation,
            "portfolio_metrics": metrics,
            "risk_notes": risk_notes,
        }
