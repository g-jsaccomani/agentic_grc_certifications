"""Tools exposed by the GRC MCP Server."""

from mcp_server_grc.tools.cloud_security import audit_cloud_security
from mcp_server_grc.tools.iac_scanner import scan_iac_configuration
from mcp_server_grc.tools.threat_intel import correlate_threat_intelligence
from mcp_server_grc.tools.climate_resilience import audit_climate_resilience
from mcp_server_grc.tools.data_leakage_prevention import audit_data_leakage_prevention
from mcp_server_grc.tools.monitoring import audit_monitoring_activities

__all__ = [
    "audit_cloud_security",
    "scan_iac_configuration",
    "correlate_threat_intelligence",
    "audit_climate_resilience",
    "audit_data_leakage_prevention",
    "audit_monitoring_activities",
]
