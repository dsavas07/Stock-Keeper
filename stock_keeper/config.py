from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PortfolioRequest:
    tickers: List[str]
    horizon_days: int = 30
    risk_appetite: str = "medium"  # low, medium, high
    max_allocation_per_ticker: float = 0.35
    sector_constraints: Optional[dict] = None
    top_n: int = 10

@dataclass
class ForecastParams:
    method: str = "linear"
    window_days: int = 90

@dataclass
class ScoringParams:
    expected_return_weight: float = 0.5
    volatility_weight: float = 0.3
    momentum_weight: float = 0.2

@dataclass
class OptimizationParams:
    max_weight: float = 0.35
    min_weight: float = 0.01
    target_risk: float = 0.15
