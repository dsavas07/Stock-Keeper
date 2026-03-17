import numpy as np
from typing import Dict, List


def mean_variance_optimize(scores: Dict[str, float], cov_matrix: np.ndarray, tickers: List[str], max_weight: float = 0.35, min_weight: float = 0.01) -> Dict[str, float]:
    n = len(tickers)
    if n == 0:
        return {}

    weights = np.array([scores.get(t, 0.0) for t in tickers], dtype=float)
    if np.sum(weights) <= 0:
        weights = np.ones(n, dtype=float)
    weights = np.maximum(weights, 0)
    weights = weights / np.sum(weights)

    # simple constraints
    weights = np.clip(weights, min_weight, max_weight)
    if np.sum(weights) <= 0:
        weights = np.ones(n, dtype=float) / n
    weights = weights / np.sum(weights)
    return {tickers[i]: float(weights[i]) for i in range(n)}


def portfolio_metrics(weights: Dict[str, float], expected_returns: Dict[str, float], cov_matrix: np.ndarray, tickers: List[str]) -> Dict[str, float]:
    w = np.array([weights.get(t, 0.0) for t in tickers])
    mu = np.array([expected_returns.get(t, 0.0) for t in tickers])
    port_mu = float(np.dot(w, mu))
    port_var = float(np.dot(w, cov_matrix.dot(w)))
    port_sigma = float(np.sqrt(max(port_var, 0.0)))
    return {"expected_return": port_mu, "volatility": port_sigma}
