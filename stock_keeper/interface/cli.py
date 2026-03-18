## import argparse
## import datetime
## from typing import Dict, List
## import pandas as pd

from stock_keeper.pipeline import PortfolioAgent
from stock_keeper.interface.prompter import parse_investment_prompt


def recommend_portfolio(symbols, api_key, horizon=30, risk_appetite="medium", weights=None):
    agent = PortfolioAgent(api_key)
    return agent.recommend(symbols=symbols, horizon=horizon, risk_appetite=risk_appetite, weights=weights)


def recommend_from_prompt(prompt: str, api_key: str):
    parsed = parse_investment_prompt(prompt)
    agent = PortfolioAgent(api_key)
    return agent.recommend(
        symbols=parsed.get("symbols", []),
        horizon=parsed.get("horizon_days", 30),
        risk_appetite=parsed.get("risk_appetite", "medium"),
    )


def run_cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Stock Keeper portfolio recommendation CLI")
    parser.add_argument("--symbols", required=False, help="Comma-separated ticker symbols")
    parser.add_argument("--api-key", required=True, help="Finnhub API key")
    parser.add_argument("--horizon", type=int, default=30, help="Forecast horizon in days")
    parser.add_argument("--risk-appetite", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--prompt", default=None, help="Optional investment question prompt")
    args = parser.parse_args()

    if args.prompt:
        result = recommend_from_prompt(args.prompt, args.api_key)
    else:
        if not args.symbols:
            raise ValueError("Either --symbols or --prompt is required.")
        symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
        result = recommend_portfolio(symbols, args.api_key, horizon=args.horizon, risk_appetite=args.risk_appetite)

    print("\n=== Portfolio Recommendation ===")
    print(result)
