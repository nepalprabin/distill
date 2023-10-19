.PHONY: start
start:
	uvicorn app.main:app --reload --port 8000

.PHONY: format
format:
	black .
	isort .