run-demo:
	python -m uvicorn stock_keeper.interface.api:app --reload

test:
	python -m pytest -q

lint:
	python -m pip install ruff
	ruff check .
