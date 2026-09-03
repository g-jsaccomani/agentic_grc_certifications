"""GCP Telemetry & Infrastructure Specialist Sub-Agent.

Dedicated to continuous real-time extraction and analysis of GCP resources:
- Cloud Asset Inventory posture
- BigQuery audit log trails
- VPC Service Controls perimeters (VPC-SC)
- Cloud KMS key states and IAM role bindings
"""

from typing import Any, Dict, List, Optional
from mcp_server_grc.tools.cloud_security import audit_cloud_security
from mcp_server_grc.tools.data_leakage_prevention import audit_data_leakage_prevention
from mcp_server_grc.tools.monitoring import audit_monitoring_activities


class GCPTelemetrySubAgent:
    """Specialized ADK Sub-Agent for Google Cloud live posture and telemetry analysis."""

    def __init__(self, spiffe_id: str = "spiffe://grc.jetsky.gcp/ns/production/sa/subagent-gcp-telemetry"):
        self.spiffe_id = spiffe_id
        self.role = "GCP Telemetry & Infrastructure Specialist"

    def scan_project_infrastructure(
        self,
        project_id: str,
        assets: List[Dict[str, Any]],
        bearer_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Scans a batch of GCP assets and maps compliance states."""
        audit_results = []
        for asset in assets:
            res_type = asset.get("type", "")
            res_name = asset.get("name", "")
            config = asset.get("config", {})

            if res_type == "vpc_sc_perimeter":
                res = audit_data_leakage_prevention(
                    perimeter_name=res_name,
                    perimeter_config=config,
                    bearer_token=bearer_token,
                )
            elif res_type == "monitoring_pipeline":
                res = audit_monitoring_activities(
                    project_id=project_id,
                    monitoring_config=config,
                    bearer_token=bearer_token,
                )
            else:
                res = audit_cloud_security(
                    resource_type=res_type,
                    resource_name=res_name,
                    config=config,
                    bearer_token=bearer_token,
                )
            audit_results.append(res)

        return {
            "project_id": project_id,
            "subagent_spiffe": self.spiffe_id,
            "total_assets_scanned": len(assets),
            "findings": audit_results,
        }
