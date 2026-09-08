.PHONY: install test lint run-mcp run-portal audit-poc journey provision-org clean

REPO_ROOT ?= $(shell git rev-parse --show-toplevel 2>/dev/null || echo "../..")
VENV ?= $(REPO_ROOT)/.venv
PYTHON ?= $(shell if [ -f "$(VENV)/bin/python" ]; then echo "$(VENV)/bin/python"; else echo python3; fi)
UV ?= $(shell command -v uv 2>/dev/null || echo "")

install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment in $(VENV)..."; \
		python3 -m venv "$(VENV)"; \
	fi
	@if [ -n "$(UV)" ]; then \
		echo "Installing dependencies using uv..."; \
		$(UV) pip install -r "$(REPO_ROOT)/requirements.txt" --python "$(VENV)/bin/python"; \
	else \
		echo "Installing dependencies using standard pip..."; \
		"$(VENV)/bin/pip" install -r "$(REPO_ROOT)/requirements.txt"; \
	fi

test:
	cd "$(REPO_ROOT)" && "$(PYTHON)" -m pytest tests/ -v

lint:
	cd "$(REPO_ROOT)" && "$(PYTHON)" -m flake8 . || true

run-mcp:
	cd "$(REPO_ROOT)" && ALLOW_DEV_AUTH_BYPASS=true "$(PYTHON)" -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload

run-portal:
	@echo "Opening GEAP Client Portal on http://localhost:8080/portal"
	cd "$(REPO_ROOT)" && ALLOW_DEV_AUTH_BYPASS=true "$(PYTHON)" -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload

audit-poc:
	cd "$(REPO_ROOT)" && "$(PYTHON)" documentation/poc/scripts/poc_live_audit.py

journey:
	cd "$(REPO_ROOT)" && bash scripts/journey.sh

provision-org:
	cd "$(REPO_ROOT)" && bash scripts/provision_org_agent.sh

deploy:
	cd "$(REPO_ROOT)" && bash scripts/deploy.sh

clean:
	cd "$(REPO_ROOT)" && find . -type d -name "__pycache__" -exec rm -rf {} +
	cd "$(REPO_ROOT)" && find . -type f -name "*.pyc" -delete
	cd "$(REPO_ROOT)" && rm -rf .pytest_cache .coverage htmlcov
