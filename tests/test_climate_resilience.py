"""Unit tests for ISO/IEC 27001:2022 / Amd 1:2024 Climate Action Amendment."""

import pytest
from mcp_server_grc.tools.climate_resilience import audit_climate_resilience


def test_climate_resilience_fully_compliant():
    topology = {
        "primary_region": "us-central1",
        "secondary_region": "us-east4",
        "storage_redundancy": "multi-region",
        "automated_failover": True,
        "rto_minutes": 30,
        "rpo_minutes": 5,
    }
    result = audit_climate_resilience(
        workload_id="core-banking-db",
        topology=topology,
        climate_risk_assessed=True,
    )
    assert result["status"] == "COMPLIANT"
    assert len(result["violations"]) == 0
    assert result["standard"] == "ISO/IEC 27001:2022 + Amd 1:2024"


def test_climate_resilience_single_region_spof():
    topology = {
        "primary_region": "us-central1",
        "secondary_region": None,
        "storage_redundancy": "single-region",
        "automated_failover": False,
        "rto_minutes": 240,
        "rpo_minutes": 60,
    }
    result = audit_climate_resilience(
        workload_id="customer-portal",
        topology=topology,
        climate_risk_assessed=False,
    )
    assert result["status"] == "NON_COMPLIANT"
    assert len(result["violations"]) >= 3
    assert any("climate change risk assessment" in v for v in result["violations"])
    assert any("single region" in v for v in result["violations"])
    assert any("automated regional failover" in v for v in result["violations"])
