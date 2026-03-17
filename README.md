# Stock Keeper

AI-driven stock portfolio recommendation engine.

## Quick Start

1. Install dependencies:

   ```bash
   python -m pip install -e .
   ```

2. Run CLI:

   ```bash
   stock-keeper --symbols AAPL,MSFT --api-key <YOUR_FINNHUB_KEY>
   ```

3. Run API:

   ```bash
   uvicorn stock_keeper.interface.api:app --reload
   ```

4. Use interactive agent:

   ```python
   from stock_keeper.interface.agent import InteractivePortfolioAgent
   agent = InteractivePortfolioAgent(api_key='<YOUR_KEY>')
   agent.answer_question('Recommend medium risk with AAPL MSFT NVDA', symbols=['AAPL','MSFT','NVDA'])
   ```

5. Windows quick demo:

   ```powershell
   .\scripts\run_demo.bat YOUR_FINNHUB_API_KEY
   ```

## Project Structure

- `stock_keeper/clients`: API clients (Finnhub)
- `stock_keeper/data`: Feature engineering
- `stock_keeper/forecasting`: Forecast models
- `stock_keeper/scoring`: Scoring rules
- `stock_keeper/optimization`: Portfolio allocation
- `stock_keeper/interface`: CLI and API
