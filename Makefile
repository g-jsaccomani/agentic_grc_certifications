.PHONY: install test lint run-mcp run-orchestrator clean journey

PYTHON := .venv/bin/python
UV := /Users/jsaccomani/.local/bin/uv

install:
	$(UV) pip install -r requirements.txt --python $(PYTHON)

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m flake8 . || true

run-mcp:
	$(PYTHON) -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload

run-portal:
	@echo "Opening GEAP Client Portal on http://localhost:8080/portal"
	$(PYTHON) -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload

audit-poc:
	$(PYTHON) scripts/poc_live_audit.py

journey:
	@bash scripts/journey.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
