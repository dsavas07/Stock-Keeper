from __future__ import annotations
from typing import Dict ##, List
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class Forecaster:
    def __init__(self, method: str = "linear", window: int = 90):
        self.method = method
        self.window = window

    def forecast(self, prices: pd.Series, horizon: int = 30) -> Dict[str, float]:
        if len(prices) < 5:
            return {"expected_return": 0.0, "trend": 0.0}

        if self.method == "linear":
            return self._linear_forecast(prices, horizon)
        return self._linear_forecast(prices, horizon)

    def _linear_forecast(self, prices: pd.Series, horizon: int) -> Dict[str, float]:
        series = prices.dropna().astype(float)
        if len(series) < 10:
            return {"expected_return": 0.0, "trend": 0.0}

        y = np.log(series.values[-self.window:]) if len(series) > self.window else np.log(series.values)
        x = np.arange(len(y)).reshape(-1, 1)
        model = LinearRegression()
        model.fit(x, y)
        pred = model.predict(np.array([[len(y) + horizon]]))[0]
        current = y[-1]
        expected_return = float(np.exp(pred) / np.exp(current) - 1)
        return {"expected_return": expected_return, "trend": float(model.coef_[0])}

    def backtest(self, prices: pd.Series, horizon: int = 5) -> Dict[str, float]:
        out = self.forecast(prices, horizon)
        return {
            "mae": abs(out["expected_return"]),
            "rmse": np.sqrt(out["expected_return"] ** 2),
            "expected_return": out["expected_return"],
        }
