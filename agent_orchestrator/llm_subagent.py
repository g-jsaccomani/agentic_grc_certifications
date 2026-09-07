"""LLMSubAgent: Real Multi-Agent Base Class with Gemini Function Calling & Grounding.

Conforms to Gemini Enterprise Agent Platform (GEAP) multi-agent standards.
Each subagent possesses a distinct Persona (System Instruction), a scoped set of
deterministic MCP tools, and executes real function-calling cycles against Gemini
via Google Cloud Vertex AI / google-genai SDK.
"""

import asyncio
import inspect
import logging
import os
from typing import Any, Callable, Dict, List, Optional
import google.auth
from google import genai
from google.genai import types

logger = logging.getLogger("grc.llm_subagent")


class LLMSubAgent:
    """Enterprise LLM Sub-Agent with Gemini Function Calling & Grounding."""

    def __init__(
        self,
        name: str,
        system_instruction: str,
        tools: Optional[Dict[str, Callable[..., Dict[str, Any]]]] = None,
        tool_declarations: Optional[List[types.FunctionDeclaration]] = None,
        model_id: Optional[str] = None,
        client: Any = "UNSET",
        timeout: float = 15.0,
    ):
        self.name = name
        self.system_instruction = system_instruction
        self.tools = tools or {}
        self.timeout = timeout
        self.model_id = model_id or os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")

        # Initialize Client if available
        if client != "UNSET":
            self.client = client
        else:
            try:
                use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in ("true", "1", "yes")
                project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("PROJECT_ID")
                location = os.getenv("GOOGLE_CLOUD_LOCATION") or os.getenv("REGION", "us-central1")
                if use_vertex or (project and not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY")):
                    logger.info("Initializing GenAI client with Vertex AI: project=%s, location=%s", project, location)
                    self.client = genai.Client(vertexai=True, project=project, location=location)
                else:
                    self.client = genai.Client()
            except Exception as exc:
                logger.warning("Google GenAI client initialization failed for '%s': %s", name, exc)
                self.client = None

        # Build function declarations from tools if not provided
        self.tool_declarations = tool_declarations or self._generate_tool_declarations()

        # Build GenerateContentConfig
        gen_tools = [types.Tool(function_declarations=self.tool_declarations)] if self.tool_declarations else None
        self.config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=gen_tools,
            temperature=0.0,  # Determinism > Creativity for compliance auditing
        )

    def _generate_tool_declarations(self) -> List[types.FunctionDeclaration]:
        """Automatically generates Gemini FunctionDeclarations for registered tools."""
        declarations: List[types.FunctionDeclaration] = []
        known_schemas = {
            "audit_cloud_security": {
                "type": "object",
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "description": "Resource type (gcs_bucket, kms_key, firewall_rule, iam_binding)",
                    },
                    "resource_name": {"type": "string", "description": "Cloud resource name or URI"},
                    "config": {"type": "object", "description": "Resource configuration parameters"},
                },
                "required": ["resource_type", "resource_name"],
            },
            "audit_monitoring_activities": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                    "monitoring_config": {"type": "object", "description": "Log sinks and retention configuration"},
                },
                "required": ["project_id"],
            },
            "audit_data_leakage_prevention": {
                "type": "object",
                "properties": {
                    "perimeter_name": {"type": "string", "description": "VPC-SC perimeter identifier"},
                    "perimeter_config": {"type": "object", "description": "Perimeter ingress and egress rules"},
                },
                "required": ["perimeter_name"],
            },
            "scan_iac_configuration": {
                "type": "object",
                "properties": {
                    "iac_type": {"type": "string", "description": "IaC format ('terraform' or 'ansible')"},
                    "content": {"type": "string", "description": "IaC source code to scan"},
                    "filename": {"type": "string", "description": "Optional file path"},
                },
                "required": ["iac_type", "content"],
            },
            "audit_cryptography_a824": {
                "type": "object",
                "properties": {
                    "key_id": {"type": "string", "description": "KMS key identifier"},
                    "config": {"type": "object", "description": "Key protection and rotation parameters"},
                },
                "required": ["key_id"],
            },
            "audit_secure_development_a828": {
                "type": "object",
                "properties": {
                    "repo_id": {"type": "string", "description": "Repository identifier"},
                    "dev_policy": {"type": "object", "description": "CI/CD security policies and branch protections"},
                },
                "required": ["repo_id"],
            },
            "correlate_threat_intelligence": {
                "type": "object",
                "properties": {
                    "log_sink_name": {"type": "string", "description": "Audit sink name"},
                    "sink_destination": {"type": "string", "description": "Sink export destination"},
                    "recent_events": {"type": "array", "description": "Recent security events"},
                    "threat_feed_enabled": {"type": "boolean", "description": "Active threat feed flag"},
                },
                "required": ["log_sink_name", "sink_destination"],
            },
            "audit_climate_resilience": {
                "type": "object",
                "properties": {
                    "workload_id": {"type": "string", "description": "Target workload identifier"},
                    "topology": {"type": "object", "description": "Multi-region architecture topology"},
                    "climate_risk_assessed": {"type": "boolean", "description": "Climate risk assessment flag"},
                },
                "required": ["workload_id", "topology"],
            },
        }

        for fn_name, fn in self.tools.items():
            schema = known_schemas.get(fn_name)
            doc = inspect.getdoc(fn) or f"Executes GRC audit tool {fn_name}."
            first_line_doc = doc.strip().split("\n")[0]

            if schema:
                decl = types.FunctionDeclaration(
                    name=fn_name,
                    description=first_line_doc,
                    parameters=schema,
                )
            else:
                decl = types.FunctionDeclaration(
                    name=fn_name,
                    description=first_line_doc,
                    parameters={"type": "object", "properties": {}},
                )
            declarations.append(decl)

        return declarations

    @staticmethod
    def _extract_function_calls(resp: Any) -> List[Any]:
        """Extracts all function calls from Gemini response candidate."""
        if not resp or not getattr(resp, "candidates", None):
            return []
        candidate = resp.candidates[0]
        if not candidate.content or not candidate.content.parts:
            return []
        calls = []
        for part in candidate.content.parts:
            if getattr(part, "function_call", None):
                calls.append(part.function_call)
        return calls

    @staticmethod
    def _extract_function_call(resp: Any) -> Optional[Any]:
        """Extracts first function call from Gemini response candidate for backward compatibility."""
        calls = LLMSubAgent._extract_function_calls(resp)
        return calls[0] if calls else None

    def run(
        self,
        user_task: str,
        max_turns: int = 4,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Runs the subagent execution loop with function calling and deterministic fallback."""
        if self.client is None:
            logger.info("GenAI client unavailable; running deterministic fallback for '%s'", self.name)
            return self._fallback_execute(user_task, context)

        contents = [types.Content(role="user", parts=[types.Part(text=user_task)])]
        tool_evidence: List[Dict[str, Any]] = []

        try:
            for _ in range(max_turns):
                resp = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=self.config,
                )
                calls = self._extract_function_calls(resp)
                if not calls:
                    narrative = resp.text or "Audit analysis completed."
                    return {
                        "agent": self.name,
                        "status": "SUCCESS",
                        "narrative": narrative,
                        "tool_evidence": tool_evidence,
                        "execution_mode": "llm_function_calling",
                    }

                response_parts = []
                for call in calls:
                    fn = self.tools.get(call.name)
                    args = dict(call.args) if call.args else {}
                    if fn:
                        try:
                            result = fn(**args)
                        except Exception as err:
                            result = {"status": "ERROR", "error": f"Tool execution failure: {str(err)}"}
                    else:
                        result = {"status": "ERROR", "error": f"Unknown tool '{call.name}'"}

                    tool_evidence.append({"tool": call.name, "args": args, "result": result})
                    response_parts.append(types.Part.from_function_response(name=call.name, response=result))

                # Append model thoughts and all function responses with exact parity
                contents.append(resp.candidates[0].content)
                contents.append(
                    types.Content(
                        role="user",
                        parts=response_parts,
                    )
                )

            return {
                "agent": self.name,
                "status": "MAX_TURNS_REACHED",
                "narrative": "Max turns reached during function calling sequence.",
                "tool_evidence": tool_evidence,
                "execution_mode": "llm_function_calling",
            }

        except Exception as exc:
            logger.warning("LLM call failed for subagent '%s' (%s); invoking deterministic fallback.", self.name, exc)
            fallback_res = self._fallback_execute(user_task, context)
            fallback_res["fallback_reason"] = str(exc)
            return fallback_res

    async def arun(
        self,
        user_task: str,
        max_turns: int = 4,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Asynchronous execution loop using client.aio or non-blocking threadpool."""
        if self.client is None or not hasattr(self.client, "aio"):
            return await asyncio.to_thread(self.run, user_task, max_turns, context)

        contents = [types.Content(role="user", parts=[types.Part(text=user_task)])]
        tool_evidence: List[Dict[str, Any]] = []

        try:
            for _ in range(max_turns):
                resp = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=self.config,
                )
                calls = self._extract_function_calls(resp)
                if not calls:
                    narrative = resp.text or "Audit analysis completed."
                    return {
                        "agent": self.name,
                        "status": "SUCCESS",
                        "narrative": narrative,
                        "tool_evidence": tool_evidence,
                        "execution_mode": "llm_async_function_calling",
                    }

                response_parts = []
                for call in calls:
                    fn = self.tools.get(call.name)
                    args = dict(call.args) if call.args else {}
                    if fn:
                        try:
                            if inspect.iscoroutinefunction(fn):
                                result = await fn(**args)
                            else:
                                result = await asyncio.to_thread(fn, **args)
                        except Exception as err:
                            result = {"status": "ERROR", "error": f"Tool execution failure: {str(err)}"}
                    else:
                        result = {"status": "ERROR", "error": f"Unknown tool '{call.name}'"}

                    tool_evidence.append({"tool": call.name, "args": args, "result": result})
                    response_parts.append(types.Part.from_function_response(name=call.name, response=result))

                contents.append(resp.candidates[0].content)
                contents.append(
                    types.Content(
                        role="user",
                        parts=response_parts,
                    )
                )

            return {
                "agent": self.name,
                "status": "MAX_TURNS_REACHED",
                "narrative": "Max turns reached during async function calling sequence.",
                "tool_evidence": tool_evidence,
                "execution_mode": "llm_async_function_calling",
            }

        except Exception as exc:
            logger.warning("Async LLM call failed for '%s' (%s); trying sync runner.", self.name, exc)
            try:
                return await asyncio.to_thread(self.run, user_task, max_turns, context)
            except Exception as sync_exc:
                logger.warning("Sync LLM call failed for '%s' (%s); falling back to deterministic execution.", self.name, sync_exc)
                return await asyncio.to_thread(self._fallback_execute, user_task, context)

    def _fallback_execute(
        self,
        user_task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Deterministic fallback: executes relevant tools directly from context parameters."""
        context = context or {}
        tool_evidence: List[Dict[str, Any]] = []

        for tool_name, tool_fn in self.tools.items():
            if tool_name in context:
                tool_args = context[tool_name]
                try:
                    res = tool_fn(**tool_args)
                    tool_evidence.append({"tool": tool_name, "args": tool_args, "result": res})
                except Exception as err:
                    tool_evidence.append({"tool": tool_name, "args": tool_args, "result": {"status": "ERROR", "error": str(err)}})

        if tool_evidence:
            has_violations = any(
                isinstance(e.get("result"), dict) and e["result"].get("status") in ("NON_COMPLIANT", "ERROR")
                for e in tool_evidence
            )
            has_undetermined = any(
                isinstance(e.get("result"), dict) and e["result"].get("status") == "UNDETERMINED"
                for e in tool_evidence
            )
            if has_violations:
                verdict = "NON_COMPLIANT"
                narrative = (
                    f"Auditor '{self.name}': Non-compliance detected across assessed controls. "
                    "Remediations required per ISO/IEC 27001:2022 specifications."
                )
            elif has_undetermined:
                verdict = "UNDETERMINED"
                narrative = (
                    f"Auditor '{self.name}': Telemetry insufficient to establish definitive compliance. "
                    "Status remains UNDETERMINED."
                )
            else:
                verdict = "COMPLIANT"
                narrative = (
                    f"Auditor '{self.name}': Technical evidence validates full adherence to assessed ISO 27001 requirements."
                )
        else:
            verdict = "UNDETERMINED"
            narrative = (
                f"Auditor '{self.name}': No verified telemetry or configuration provided by caller. "
                "User claims or free-text descriptions cannot be treated as verified audit evidence. "
                "Status remains UNDETERMINED."
            )

        return {
            "agent": self.name,
            "status": verdict,
            "narrative": narrative,
            "tool_evidence": tool_evidence,
            "execution_mode": "deterministic_fallback",
        }
