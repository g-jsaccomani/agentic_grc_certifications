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


def suppress_genai_client_cleanup_warning() -> None:
    """Suppresses benign google-genai SDK cleanup warning when Client() fails to initialize.

    When Client() fails (e.g. absent credentials), Python garbage-collects the partially
    initialized BaseApiClient instance. BaseApiClient.__del__ unconditionally schedules
    aclose() in the running event loop. Because initialization aborted before _async_httpx_client
    was attached, aclose() raises AttributeError: 'BaseApiClient' object has no attribute '_async_httpx_client',
    logged by asyncio as 'Task exception was never retrieved'.
    This patch ensures cleanup is only performed if _async_httpx_client was actually initialized.
    """
    try:
        from google.genai.client import BaseApiClient

        _orig_aclose = getattr(BaseApiClient, "aclose", None)
        if _orig_aclose and getattr(BaseApiClient, "_grc_safe_cleanup_patched", False) is not True:
            async def _safe_aclose(self) -> None:
                if not hasattr(self, "_async_httpx_client") or self._async_httpx_client is None:
                    return
                try:
                    await _orig_aclose(self)
                except (AttributeError, Exception):
                    pass

            BaseApiClient.aclose = _safe_aclose

        _orig_del = getattr(BaseApiClient, "__del__", None)
        if _orig_del and getattr(BaseApiClient, "_grc_safe_del_patched", False) is not True:
            def _safe_del(self) -> None:
                if not hasattr(self, "_async_httpx_client") or self._async_httpx_client is None:
                    return
                try:
                    _orig_del(self)
                except Exception:
                    pass

            BaseApiClient.__del__ = _safe_del
            BaseApiClient._grc_safe_cleanup_patched = True
            BaseApiClient._grc_safe_del_patched = True
    except Exception as exc:
        logger.debug("Failed to patch google-genai BaseApiClient cleanup: %s", exc)


suppress_genai_client_cleanup_warning()


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
                "required": [],
            },
            "audit_climate_resilience": {
                "type": "object",
                "properties": {
                    "workload_id": {"type": "string", "description": "Target workload identifier"},
                    "topology": {"type": "object", "description": "Multi-region architecture topology"},
                    "climate_risk_assessed": {"type": "boolean", "description": "Climate risk assessment flag"},
                },
                "required": [],
            },
            "inspect_cloud_kms": {
                "type": "object",
                "properties": {
                    "key_name": {"type": "string", "description": "KMS key identifier or name (e.g. 'my-key')"},
                    "location": {"type": "string", "description": "Optional GCP region/location (e.g. 'global', 'us-central1')"},
                    "keyring_name": {"type": "string", "description": "Optional KeyRing name"},
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                },
                "required": ["key_name"],
            },
            "inspect_cloud_storage": {
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "Cloud Storage bucket name to inspect"},
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                },
                "required": ["bucket_name"],
            },
            "inspect_cloud_iam": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID to inspect IAM policy for"},
                },
                "required": [],
            },
            "inspect_cloud_run": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "GCP region (e.g. 'us-central1')"},
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                },
                "required": [],
            },
            "list_cloud_kms": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Optional location"},
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                },
                "required": [],
            },
            "list_cloud_storage": {
                "type": "object",
                "properties": {
                    "project_id": {"type": "string", "description": "GCP Project ID"},
                },
                "required": [],
            },
            "get_questionnaire_summary": {
                "type": "object",
                "properties": {
                    "framework": {"type": "string", "description": "Compliance framework identifier (default ISO27001:2022)"},
                },
                "required": [],
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
    def _extract_usage(resp: Any) -> Dict[str, int]:
        """Extracts token counts from Gemini response usage_metadata."""
        usage = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "cached_content_token_count": 0,
            "total_token_count": 0,
        }
        if not resp:
            return usage
        meta = getattr(resp, "usage_metadata", None)
        if not meta and isinstance(resp, dict):
            meta = resp.get("usage_metadata")
        if meta:
            if isinstance(meta, dict):
                p = meta.get("prompt_token_count") or 0
                c = meta.get("candidates_token_count") or 0
                ca = meta.get("cached_content_token_count") or 0
                t = meta.get("total_token_count") or (p + c)
            else:
                p = getattr(meta, "prompt_token_count", 0) or 0
                c = getattr(meta, "candidates_token_count", 0) or 0
                ca = getattr(meta, "cached_content_token_count", 0) or 0
                t = getattr(meta, "total_token_count", 0) or (p + c)
            usage["prompt_token_count"] = int(p)
            usage["candidates_token_count"] = int(c)
            usage["cached_content_token_count"] = int(ca)
            usage["total_token_count"] = int(t)
        return usage

    @staticmethod
    def _extract_function_call(resp: Any) -> Optional[Any]:
        """Extracts first function call from Gemini response candidate for backward compatibility."""
        calls = LLMSubAgent._extract_function_calls(resp)
        return calls[0] if calls else None

    @staticmethod
    def _build_contents(user_task: str, history: Optional[List[Dict[str, str]]] = None) -> List[types.Content]:
        """Constructs alternating multi-turn Content list for Gemini models."""
        contents: List[types.Content] = []
        if history:
            for turn in history:
                role = "user" if turn.get("role") == "user" else "model"
                text = str(turn.get("content") or "").strip()
                if not text:
                    continue
                if contents and contents[-1].role == role:
                    contents[-1].parts[0].text += "\n\n" + text
                else:
                    contents.append(types.Content(role=role, parts=[types.Part(text=text)]))
            if contents and contents[-1].role == "user":
                contents[-1].parts[0].text += "\n\n" + user_task
            else:
                contents.append(types.Content(role="user", parts=[types.Part(text=user_task)]))
        else:
            contents = [types.Content(role="user", parts=[types.Part(text=user_task)])]
        return contents

    def run(
        self,
        user_task: str,
        max_turns: int = 4,
        context: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Runs the subagent execution loop with function calling and deterministic fallback."""
        if self.client is None:
            logger.info("GenAI client unavailable; running deterministic fallback for '%s'", self.name)
            return self._fallback_execute(user_task, context)

        contents = self._build_contents(user_task, history)
        tool_evidence: List[Dict[str, Any]] = []
        accumulated_usage = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "cached_content_token_count": 0,
            "total_token_count": 0,
        }

        try:
            for _ in range(max_turns):
                resp = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=self.config,
                )
                turn_usage = self._extract_usage(resp)
                for k in accumulated_usage:
                    accumulated_usage[k] += turn_usage[k]

                calls = self._extract_function_calls(resp)
                if not calls:
                    narrative = resp.text or "Audit analysis completed."
                    return {
                        "agent": self.name,
                        "status": "SUCCESS",
                        "narrative": narrative,
                        "tool_evidence": tool_evidence,
                        "execution_mode": "llm_function_calling",
                        "usage": accumulated_usage,
                        "model_key": self.model_id,
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
                "usage": accumulated_usage,
                "model_key": self.model_id,
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
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Asynchronous execution loop using client.aio or non-blocking threadpool."""
        if self.client is None or not hasattr(self.client, "aio"):
            return await asyncio.to_thread(self.run, user_task, max_turns, context, history)

        contents = self._build_contents(user_task, history)
        tool_evidence: List[Dict[str, Any]] = []
        accumulated_usage = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "cached_content_token_count": 0,
            "total_token_count": 0,
        }

        try:
            for _ in range(max_turns):
                resp = await self.client.aio.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=self.config,
                )
                turn_usage = self._extract_usage(resp)
                for k in accumulated_usage:
                    accumulated_usage[k] += turn_usage[k]

                calls = self._extract_function_calls(resp)
                if not calls:
                    narrative = resp.text or "Audit analysis completed."
                    return {
                        "agent": self.name,
                        "status": "SUCCESS",
                        "narrative": narrative,
                        "tool_evidence": tool_evidence,
                        "execution_mode": "llm_async_function_calling",
                        "usage": accumulated_usage,
                        "model_key": self.model_id,
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
                "usage": accumulated_usage,
                "model_key": self.model_id,
            }

        except Exception as exc:
            logger.warning("Async LLM call failed for '%s' (%s); trying sync runner.", self.name, exc)
            try:
                return await asyncio.to_thread(self.run, user_task, max_turns, context, history)
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
            detail_lines = []
            for ev in tool_evidence:
                t = ev.get("tool", "")
                r = ev.get("result", {})
                if isinstance(r, dict):
                    if t == "get_questionnaire_summary":
                        st = "COMPLIANT" if r.get("completion_percentage", 0) == 100.0 else "IN_PROGRESS"
                        fw = r.get("framework", "ISO27001:2022")
                        detail_lines.append(
                            f"- **Questionário ({fw})**: `{st}` — Respondidos: {r.get('answered', 0)}/{r.get('total_controls', 93)} "
                            f"({r.get('completion_percentage', 0.0)}%), Conformes: {r.get('compliant', 0)}, "
                            f"Não Conformes: {r.get('non_compliant', 0)}, Pendentes: {r.get('total_controls', 93) - r.get('answered', 0)}"
                        )
                    else:
                        st = r.get("status", "UNKNOWN")
                        std = r.get("standard") or r.get("control") or t
                        detail_lines.append(f"- **{std}**: `{st}`")
                        for v in r.get("violations", []):
                            detail_lines.append(f"  * Violação: {v}")
                        for rec in r.get("recommendations", []):
                            detail_lines.append(f"  * Recomendação: {rec}")

            details_text = ("\n\n" + "\n".join(detail_lines)) if detail_lines else ""

            if any(e.get("tool") == "get_questionnaire_summary" for e in tool_evidence):
                q_ev = next(e for e in tool_evidence if e.get("tool") == "get_questionnaire_summary")
                q_res = q_ev.get("result", {})
                pct = q_res.get("completion_percentage", 0.0)
                verdict = "COMPLIANT" if pct == 100.0 else "IN_PROGRESS"
                narrative = (
                    f"Readiness Advisor '{self.name}': Questionnaire completion status evaluated for {q_res.get('framework', 'ISO27001:2022')}. "
                    f"Answered: {q_res.get('answered', 0)}/{q_res.get('total_controls', 93)} ({pct}%). "
                    f"Compliant: {q_res.get('compliant', 0)}, Non-Compliant: {q_res.get('non_compliant', 0)}, "
                    f"Pending: {q_res.get('total_controls', 93) - q_res.get('answered', 0)}.{details_text}"
                )
            elif has_violations:
                verdict = "NON_COMPLIANT"
                narrative = (
                    f"Readiness Advisor '{self.name}': Non-compliance detected across assessed controls. "
                    f"Remediations required per ISO/IEC 27001:2022 specifications.{details_text}"
                )
            elif has_undetermined:
                verdict = "UNDETERMINED"
                narrative = (
                    f"Readiness Advisor '{self.name}': Telemetry insufficient to establish definitive compliance. "
                    f"Status remains UNDETERMINED.{details_text}"
                )
            else:
                verdict = "COMPLIANT"
                narrative = (
                    f"Readiness Advisor '{self.name}': Technical evidence validates full adherence to assessed ISO 27001 requirements.{details_text}"
                )
        else:
            verdict = "UNDETERMINED"
            narrative = (
                f"Readiness Advisor '{self.name}': No verified telemetry or configuration provided by caller. "
                "User claims or free-text descriptions cannot be treated as verified audit evidence. "
                "Status remains UNDETERMINED."
            )

        return {
            "agent": self.name,
            "status": verdict,
            "narrative": narrative,
            "tool_evidence": tool_evidence,
            "execution_mode": "deterministic_fallback",
            "usage": {
                "prompt_token_count": 0,
                "candidates_token_count": 0,
                "cached_content_token_count": 0,
                "total_token_count": 0,
            },
            "model_key": self.model_id,
        }
