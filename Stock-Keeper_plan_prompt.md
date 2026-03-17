## Plan: Build Python AI Agent for Stock Portfolio Recommendation

Great news — we have a clear path: use Python + Finnhub, with modular ingestion, forecasting, scoring, and optimization. Next I’ll outline the full implementation phases and then get your signoff before coding.

### ✅ Phase 1: Architecture & Data Pipeline
1. Define core modules:
   - Data ingestion: API clients for Finnhub (pluggable for others)
   - Feature engineering: numeric and textual signals
   - Forecasting models: statistical/time-series + simple ML ensembles
   - Scoring & portfolio optimizer
   - Interface: CLI/REST endpoint and question-based prompts
2. Design data contracts (daily/weekly OHLC, fundamentals, news sentiment).

### ✅ Phase 2: Ingestion + Preprocessing
1. Implement `FinnhubClient` with rate-limit handling and caching.
2. Fetch:
   - historical prices (daily/weekly)
   - company fundamentals/ratings
   - news/sentiment text
3. Preprocess:
   - compute returns, moving averages, volatility, momentum, drawdowns
   - normalize and align time series
   - derive sentiment scores from text

### ✅ Phase 3: Forecasting + Evaluation
1. Implement forecasting strategies:
   - Rolling stats + linear regression baseline
   - ARIMA/Prophet-like forecast
   - Optional LightGBM/Neural models for returns
2. Evaluate using backtesting windows and metrics (MAE, RMSE, Sharpe, drawdown).
3. Keep model selection configurable (short/long horizon).

### ✅ Phase 4: Criteria-Based Scoring + Optimization
1. Build investment scoring:
   - expected return vs risk
   - sector constraints
   - short-term vs long-term priorities
   - risk appetite weight (higher vs lower risk)
2. Portfolio construction:
   - mean-variance (Markowitz) optimizer plus CVaR guardrails
   - simple rule-based fallback (top-N per score with caps)
3. Output recommended allocations and narrative rationale.

### ✅ Phase 5: Interface & Questions
1. Build question-driven flow:
   - “For short-term growth with moderate risk in tech, recommend best mix”
   - Accept prioritized criteria and constraints
2. Return structured JSON: selected vehicles, weights, expected metrics, risk notes.
3. Add CLI and API wrapper for integration or dashboards.

### ✅ Verification
- Unit tests for ingestion, feature pipeline, forecast model outputs, scoring rules, optimizer.
- End-to-end sample run on known symbols and historical backtest.
- Behavior tests: criteria toggles must change portfolio outputs.

---

## Minimal Prototype First Option
- Build a working prototype with data ingestion, one forecasting method, simple scoring, and a basic portfolio allocation.
- Then expand to full criteria and advanced optimization.

## Full Feature Agent Option
- Build all modules at once, including text sentiment ingestion, multiple forecasting algorithms, criteria weight balancing, and API + CLI.
- Recommended when you need production-ready capabilities quickly.
