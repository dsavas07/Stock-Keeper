from typing import Dict


def parse_investment_prompt(prompt: str) -> Dict:
    # Simple heuristic parser for prioritized criteria
    parsed = {
        "risk_appetite": "medium",
        "horizon_days": 30,
        "symbols": [],
    }
    lower = prompt.lower()
    if "low risk" in lower or "conservative" in lower:
        parsed["risk_appetite"] = "low"
    if "high risk" in lower or "aggressive" in lower:
        parsed["risk_appetite"] = "high"
    if "short-term" in lower:
        parsed["horizon_days"] = 14
    if "long-term" in lower:
        parsed["horizon_days"] = 180

    # parse tickers by all uppercase words
    tokens = prompt.split()
    symbols = [t.strip(",.") for t in tokens if t.isupper() and len(t) <= 5 and t.isalpha()]
    parsed["symbols"] = symbols
    return parsed
