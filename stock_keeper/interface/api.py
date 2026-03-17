from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from stock_keeper.interface.cli import recommend_portfolio, recommend_from_prompt

app = FastAPI(title="Stock Keeper API")

class PortfolioRequest(BaseModel):
    symbols: Optional[List[str]] = None
    api_key: str
    horizon: int = 30
    risk_appetite: str = "medium"
    prompt: Optional[str] = None

@app.post("/recommend")
def recommend(req: PortfolioRequest):
    if req.prompt:
        return recommend_from_prompt(req.prompt, req.api_key)

    if not req.symbols:
        raise HTTPException(status_code=400, detail="Either symbols or prompt required")
    return recommend_portfolio(req.symbols, req.api_key, horizon=req.horizon, risk_appetite=req.risk_appetite)
