run-demo:
	python -m uvicorn stock_keeper.interface.api:app --reload

test:
	python -m pip install pytest
	python -m pytest -q

lint:
	python -m pip install ruff
	ruff check --fix --output_format=github .
