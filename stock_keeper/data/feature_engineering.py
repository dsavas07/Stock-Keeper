import numpy as np
import pandas as pd


def compute_returns(df: pd.DataFrame, price_column: str = "close") -> pd.Series:
    returns = df[price_column].pct_change().fillna(0)
    return returns


def compute_moving_average(df: pd.DataFrame, price_column: str = "close", window: int = 20) -> pd.Series:
    return df[price_column].rolling(window=window).mean().bfill()


def compute_volatility(df: pd.DataFrame, price_column: str = "close", window: int = 20) -> pd.Series:
    returns = compute_returns(df, price_column)
    return returns.rolling(window=window).std().bfill()


def compute_momentum(df: pd.DataFrame, price_column: str = "close", window: int = 20) -> pd.Series:
    return df[price_column].pct_change(periods=window).fillna(0)


def normalize_signal(x: np.ndarray) -> np.ndarray:
    min_v = np.min(x)
    max_v = np.max(x)
    if max_v - min_v < 1e-9:
        return np.zeros_like(x)
    return (x - min_v) / (max_v - min_v)
