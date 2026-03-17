from typing import Optional, Dict

from stock_keeper.interface.prompter import parse_investment_prompt
from stock_keeper.pipeline import PortfolioAgent


class InteractivePortfolioAgent:
    def __init__(self, api_key: str, cache_path: str = "data/finnhub_cache.json"):
        self.api_key = api_key
        self.cache_path = cache_path

    def answer_question(
        self,
        question: str,
        symbols: Optional[list[str]] = None,
        horizon: Optional[int] = None,
        risk_appetite: Optional[str] = None,
        sector_constraints: Optional[Dict[str, float]] = None,
    ) -> Dict:
        parsed = parse_investment_prompt(question)
        selected_symbols = symbols or parsed.get("symbols", [])
        if not selected_symbols:
            raise ValueError("No symbols discovered; provide ticker symbols directly or in the prompt.")

        horizon = horizon or parsed.get("horizon_days", 30)
        risk = risk_appetite or parsed.get("risk_appetite", "medium")

        agent = PortfolioAgent(api_key=self.api_key, cache_path=self.cache_path)
        return agent.recommend(
            symbols=selected_symbols,
            horizon=horizon,
            risk_appetite=risk,
            sector_constraints=sector_constraints,
        )


__all__ = ["InteractivePortfolioAgent"]
