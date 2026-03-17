import pandas as pd
from stock_keeper.forecasting.forecaster import Forecaster
from stock_keeper.scoring.scorer import build_ticker_signals, compute_score

def test_forecaster_linear():
    prices = pd.Series([100, 101, 102, 104, 107, 110, 112, 115])
    f = Forecaster(method="linear", window=5)
    out = f.forecast(prices, horizon=5)
    assert "expected_return" in out
    assert isinstance(out["expected_return"], float)


def test_scoring():
    signals = build_ticker_signals(0.05, 0.02, 0.03, risk_appetite="medium")
    score = compute_score(signals, {"expected_return": 0.5, "volatility": 0.3, "momentum": 0.2})
    assert score > 0
