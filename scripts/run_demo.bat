@echo off
REM Run Stock Keeper demo API server
setlocal
if "%~1"=="" (
  echo Usage: run_demo.bat <FINNHUB_API_KEY>
  echo Example: run_demo.bat your_key_here
  exit /b 1
)
set FINNHUB_API_KEY=%1
echo Starting Stock Keeper API with FINNHUB_API_KEY=%FINNHUB_API_KEY%
python -m uvicorn stock_keeper.interface.api:app --reload
