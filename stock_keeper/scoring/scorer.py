from typing import Dict


def compute_score(signals: Dict[str, float], weights: Dict[str, float]) -> float:
    score = 0.0
    for k, v in weights.items():
        score += signals.get(k, 0.0) * v
    return score


def build_ticker_signals(expected_return: float, volatility: float, momentum: float, risk_appetite: str = "medium") -> Dict[str, float]:
    risk_modifier = {"low": 0.8, "medium": 1.0, "high": 1.2}.get(risk_appetite, 1.0)
    return {
        "expected_return": expected_return,
        "volatility": max(1e-6, 1.0 - volatility * risk_modifier),
        "momentum": momentum,
    }
