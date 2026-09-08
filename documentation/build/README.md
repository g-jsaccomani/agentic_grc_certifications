# Build & Automation Guide
## Developer Workflow Shortcuts & CI/CD Tooling

> **Platform**: Make • Python 3.12 • uv • Google Cloud SDK  
> **Status**: Production Ready  
> **Language**: English

---

## 1. Overview

This directory contains the automation tooling and `Makefile` for the Agentic GRC repository. To maintain a clean root project workspace, build shortcuts are organized within this dedicated module.

---

## 2. Command Reference

All build targets can be executed directly from the repository root using the `-f` flag, or from within this directory:

### Execution Syntax
```bash
# From repository root:
make -f documentation/build/Makefile <target>

# Or navigate to this directory:
cd documentation/build && make <target>
```

### Available Targets

| Target | Description | Underlying Command |
| :--- | :--- | :--- |
| `make install` | Creates Python virtual environment (`.venv`) and installs dependencies via `uv` or `pip`. | `python3 -m venv .venv && pip install -r requirements.txt` |
| `make test` | Runs the full 184-test automated suite with verbose test reporting. | `pytest tests/ -v` |
| `make lint` | Runs PEP-8 static analysis across the codebase via `flake8`. | `flake8 .` |
| `make run-portal` | Launches the local interactive web portal at `http://localhost:8080/portal`. | `uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload` |
| `make run-mcp` | Launches the standalone Model Context Protocol (MCP) server on port 8080. | `uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080` |
| `make audit-poc` | Executes the standalone POC live audit runner against Google Cloud target assets. | `python documentation/poc/scripts/poc_live_audit.py` |
| `make journey` | Full end-to-end deployment journey: runs 184 tests, builds container via Cloud Build, and deploys to Cloud Run. | `bash scripts/journey.sh` |
| `make provision-org`| Provisions GCP organization folder, host project, and org-level read IAM roles via Terraform. | `bash scripts/provision_org_agent.sh` |
| `make clean` | Cleans temporary cache files, `.pytest_cache`, and bytecode artifacts. | `rm -rf .pytest_cache __pycache__ *.pyc` |

---

## 3. Tooling Prerequisites

- **Python**: 3.11 or 3.12
- **uv** (Recommended): High-speed Python package installer (auto-detected).
- **gcloud**: Google Cloud SDK for container builds and deployment.
- **make**: GNU Make 3.81+
