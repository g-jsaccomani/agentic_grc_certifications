.PHONY: install test lint run-mcp run-orchestrator clean journey

VENV ?= .venv
PYTHON ?= $(shell if [ -f $(VENV)/bin/python ]; then echo $(VENV)/bin/python; else echo python3; fi)
UV ?= $(shell command -v uv 2>/dev/null || echo "")

install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment in $(VENV)..."; \
		python3 -m venv $(VENV); \
	fi
	@if [ -n "$(UV)" ]; then \
		echo "Installing dependencies using uv..."; \
		$(UV) pip install -r requirements.txt --python $(VENV)/bin/python; \
	else \
		echo "Installing dependencies using standard pip..."; \
		$(VENV)/bin/pip install -r requirements.txt; \
	fi

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

provision-org:
	@bash scripts/provision_org_agent.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
