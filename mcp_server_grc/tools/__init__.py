"""Tools exposed by the GRC MCP Server."""

from mcp_server_grc.tools.cloud_security import audit_cloud_security
from mcp_server_grc.tools.iac_scanner import scan_iac_configuration
from mcp_server_grc.tools.threat_intel import correlate_threat_intelligence
from mcp_server_grc.tools.climate_resilience import audit_climate_resilience

__all__ = [
    "audit_cloud_security",
    "scan_iac_configuration",
    "correlate_threat_intelligence",
    "audit_climate_resilience",
]
