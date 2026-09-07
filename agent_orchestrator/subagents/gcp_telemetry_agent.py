"""GCP Telemetry & Infrastructure Specialist Sub-Agent with Gemini Function Calling.

Dedicated to continuous real-time extraction and analysis of GCP resources:
- Cloud Asset Inventory posture
- BigQuery audit log trails
- VPC Service Controls perimeters (VPC-SC)
- Cloud KMS key states and IAM role bindings
"""

from typing import Any, Callable, Dict, List, Optional
from agent_orchestrator.llm_subagent import LLMSubAgent
from mcp_server_grc.tools.cloud_security import audit_cloud_security
from mcp_server_grc.tools.data_leakage_prevention import audit_data_leakage_prevention
from mcp_server_grc.tools.monitoring import audit_monitoring_activities
from mcp_server_grc.cloud_inspector import (
    inspect_cloud_kms_key,
    inspect_cloud_storage_bucket,
    inspect_project_iam_policy,
    inspect_cloud_run_services,
    list_cloud_kms_keys,
    list_cloud_storage_buckets,
)


GCP_TELEMETRY_SYSTEM_PROMPT = """
Você é o Auditor Especialista em Telemetria de Nuvem e Infraestrutura GCP (ISO/IEC 27001:2022).
Você possui PODER DE AUDITORIA ATIVA NAS NUVENS com ferramentas de leitura (Read-Only) em tempo real.
Sua missão é extrair, normalizar e auditar a postura de segurança de recursos GCP reais.
Regra inegociável: você NUNCA inventa ou assume conformidade sem evidência direta.
Você SEMPRE executa as tools correspondentes (inspect_cloud_kms, inspect_cloud_storage, inspect_cloud_iam, etc.) e baseia sua análise estritamente no retorno delas.
"""


class GCPTelemetrySubAgent:
    """Specialized ADK Sub-Agent for Google Cloud live posture and telemetry analysis."""

    def __init__(
        self,
        spiffe_id: str = "spiffe://grc.jetsky.gcp/ns/production/sa/subagent-gcp-telemetry",
        client: Optional[Any] = None,
        model_id: Optional[str] = None,
    ):
        self.spiffe_id = spiffe_id
        self.role = "GCP Telemetry & Infrastructure Specialist"

        self.tools: Dict[str, Callable[..., Dict[str, Any]]] = {
            "audit_cloud_security": audit_cloud_security,
            "audit_data_leakage_prevention": audit_data_leakage_prevention,
            "audit_monitoring_activities": audit_monitoring_activities,
            "inspect_cloud_kms": inspect_cloud_kms_key,
            "inspect_cloud_storage": inspect_cloud_storage_bucket,
            "inspect_cloud_iam": inspect_project_iam_policy,
            "inspect_cloud_run": inspect_cloud_run_services,
            "list_cloud_kms": list_cloud_kms_keys,
            "list_cloud_storage": list_cloud_storage_buckets,
        }

        self.llm = LLMSubAgent(
            name="gcp_telemetry_agent",
            system_instruction=GCP_TELEMETRY_SYSTEM_PROMPT,
            tools=self.tools,
            model_id=model_id,
            client=client,
        )

    def run(self, user_task: str, max_turns: int = 4, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runs the LLM function-calling loop for telemetry analysis."""
        return self.llm.run(user_task, max_turns=max_turns, context=context)

    async def arun(self, user_task: str, max_turns: int = 4, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async version of LLM function-calling loop."""
        return await self.llm.arun(user_task, max_turns=max_turns, context=context)

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
