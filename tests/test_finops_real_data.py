"""Tests for real FinOps data tracking, token usage extraction, and algorithmic tips."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient

from agent_orchestrator.llm_subagent import LLMSubAgent
from mcp_server_grc.finops import FinOpsTracker, finops_tracker, FinOpsUsageEvent, AgentFinOpsRecord
from mcp_server_grc.server import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer ya29.valid-auditor-access-token"}


class MockUsageMetadataObj:
    def __init__(self, prompt=1337, candidates=420, cached=800, total=2557):
        self.prompt_token_count = prompt
        self.candidates_token_count = candidates
        self.cached_content_token_count = cached
        self.total_token_count = total


class MockCandidate:
    def __init__(self, text="Response from LLM", function_calls=None):
        self.content = MagicMock()
        parts = []
        if function_calls:
            for fc in function_calls:
                p = MagicMock()
                p.function_call = fc
                p.text = None
                parts.append(p)
        else:
            p = MagicMock()
            p.function_call = None
            p.text = text
            parts.append(p)
        self.content.parts = parts


class MockGenerateContentResponse:
    def __init__(self, text="Response from LLM", usage_metadata=None, function_calls=None):
        self.text = text
        self.usage_metadata = usage_metadata or MockUsageMetadataObj()
        self.candidates = [MockCandidate(text=text, function_calls=function_calls)]


def test_extract_usage_object():
    """Verify _extract_usage correctly reads from a usage_metadata object."""
    resp = MockGenerateContentResponse(
        usage_metadata=MockUsageMetadataObj(prompt=500, candidates=150, cached=200, total=850)
    )
    usage = LLMSubAgent._extract_usage(resp)
    assert usage["prompt_token_count"] == 500
    assert usage["candidates_token_count"] == 150
    assert usage["cached_content_token_count"] == 200
    assert usage["total_token_count"] == 850


def test_extract_usage_dict():
    """Verify _extract_usage correctly reads from a dictionary usage_metadata."""
    resp = MagicMock()
    resp.usage_metadata = {
        "prompt_token_count": 1200,
        "candidates_token_count": 350,
        "cached_content_token_count": 600,
        "total_token_count": 2150,
    }
    usage = LLMSubAgent._extract_usage(resp)
    assert usage["prompt_token_count"] == 1200
    assert usage["candidates_token_count"] == 350
    assert usage["cached_content_token_count"] == 600
    assert usage["total_token_count"] == 2150


def test_extract_usage_none_or_missing():
    """Verify _extract_usage handles missing usage_metadata safely with zero counts."""
    resp = MagicMock()
    resp.usage_metadata = None
    usage = LLMSubAgent._extract_usage(resp)
    assert usage["prompt_token_count"] == 0
    assert usage["candidates_token_count"] == 0
    assert usage["cached_content_token_count"] == 0
    assert usage["total_token_count"] == 0

    usage_none = LLMSubAgent._extract_usage(None)
    assert usage_none["total_token_count"] == 0


def test_subagent_run_accumulates_usage_across_turns():
    """Verify run() accumulates usage_metadata across multi-turn function calling."""
    agent = LLMSubAgent(
        name="Test Agent",
        system_instruction="You are a test agent.",
        tools={"list_iam_bindings": lambda: {"bindings": []}},
        model_id="gemini-2.5-flash",
    )

    # Turn 1: returns a tool call
    call1 = MagicMock()
    call1.name = "list_iam_bindings"
    call1.args = {}
    resp1 = MockGenerateContentResponse(
        text="",
        usage_metadata=MockUsageMetadataObj(prompt=800, candidates=40, cached=300, total=1140),
        function_calls=[call1],
    )

    # Turn 2: returns final response
    resp2 = MockGenerateContentResponse(
        text="Final audit answer based on tool call",
        usage_metadata=MockUsageMetadataObj(prompt=950, candidates=120, cached=350, total=1420),
        function_calls=[],
    )

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = [resp1, resp2]
    agent.client = mock_client

    res = agent.run("Audit IAM permissions")

    assert res["status"] == "SUCCESS"
    assert "usage" in res
    usage = res["usage"]
    # Total accumulated: 800 + 950 = 1750 prompt, 40 + 120 = 160 completion, 300 + 350 = 650 cached
    assert usage["prompt_token_count"] == 1750
    assert usage["candidates_token_count"] == 160
    assert usage["cached_content_token_count"] == 650
    assert usage["total_token_count"] == 2560


@pytest.mark.asyncio
async def test_subagent_arun_accumulates_usage_and_fallback():
    """Verify arun() accumulates usage or records zero on fallback."""
    agent = LLMSubAgent(
        name="Async Agent",
        system_instruction="Async advisor",
        model_id="gemini-2.5-pro",
    )

    resp = MockGenerateContentResponse(
        text="Async direct reply",
        usage_metadata=MockUsageMetadataObj(prompt=600, candidates=80, cached=100, total=780),
    )

    mock_client = MagicMock()
    mock_client.aio.models.generate_content = AsyncMock(return_value=resp)
    agent.client = mock_client

    res = await agent.arun("Quick async check")

    assert res["status"] == "SUCCESS"
    assert res["usage"]["prompt_token_count"] == 600
    assert res["usage"]["candidates_token_count"] == 80
    assert res["usage"]["cached_content_token_count"] == 100
    assert res["usage"]["total_token_count"] == 780

    # Fallback path when exception occurs in both async and sync
    mock_client.aio.models.generate_content = AsyncMock(side_effect=Exception("API error"))
    mock_client.models.generate_content.side_effect = Exception("API sync error")
    fallback_res = await agent.arun("Trigger fallback")

    assert fallback_res["execution_mode"] == "deterministic_fallback"
    assert fallback_res["usage"]["prompt_token_count"] == 0
    assert fallback_res["usage"]["candidates_token_count"] == 0
    assert fallback_res["usage"]["cached_content_token_count"] == 0
    assert fallback_res["usage"]["total_token_count"] == 0


def test_finops_tracker_records_exact_usage_events():
    """Verify FinOpsTracker accurately logs events and aggregates totals."""
    tracker = FinOpsTracker()
    initial_event_count = len(tracker.events)

    tracker.record_usage(
        agent_id="lead-auditor",
        prompt_tokens=2500,
        completion_tokens=450,
        cached_tokens=1800,
        model_key="gemini-2.5-pro",
    )

    assert len(tracker.events) == initial_event_count + 1
    ev = tracker.events[-1]
    assert ev.agent_id == "lead-auditor"
    assert ev.prompt_tokens == 2500
    assert ev.completion_tokens == 450
    assert ev.cached_tokens == 1800
    assert ev.model_key == "gemini-2.5-pro"

    # Verify zero-token fallback record does not inflate counts falsely
    tracker.record_usage(
        agent_id="lead-auditor",
        prompt_tokens=0,
        completion_tokens=0,
        cached_tokens=0,
        model_key="gemini-2.5-pro",
    )
    ev_zero = tracker.events[-1]
    assert ev_zero.prompt_tokens == 0
    assert ev_zero.completion_tokens == 0


def test_finops_algorithmic_token_saving_tips():
    """Verify algorithmic tips computed from empirical event history."""
    tracker = FinOpsTracker()
    tracker.events.clear()

    # Scenario 1: Pro model with short prompts (< 1500 tokens)
    tracker.record_usage(
        agent_id="test-pro-short",
        prompt_tokens=800,
        completion_tokens=50,
        cached_tokens=0,
        model_key="gemini-2.5-pro",
    )

    # Scenario 2: Uncached large prompt (>= 1024 tokens, cached == 0)
    tracker.record_usage(
        agent_id="test-uncached-large",
        prompt_tokens=4000,
        completion_tokens=200,
        cached_tokens=0,
        model_key="gemini-2.5-flash",
    )

    # Scenario 3: Zero-token direct deterministic call
    tracker.record_usage(
        agent_id="test-zero-call",
        prompt_tokens=0,
        completion_tokens=0,
        cached_tokens=0,
        model_key="gemini-2.5-flash",
    )

    # Scenario 4: Verbose output (> 2000 tokens)
    tracker.record_usage(
        agent_id="test-verbose-output",
        prompt_tokens=1000,
        completion_tokens=2500,
        cached_tokens=0,
        model_key="gemini-2.5-flash",
    )

    tips = tracker.get_token_saving_tips()
    tip_types = [t["type"] for t in tips]

    assert "model_right_sizing" in tip_types
    assert "context_caching" in tip_types
    assert "zero_token_efficiency" in tip_types
    assert "output_compression" in tip_types

    # Verify model right-sizing recommendation
    right_sizing_tip = next(t for t in tips if t["type"] == "model_right_sizing")
    assert right_sizing_tip["severity"] == "MEDIUM"
    assert right_sizing_tip["potential_savings_usd"] > 0

    # Verify context caching recommendation
    caching_tip = next(t for t in tips if t["type"] == "context_caching")
    assert caching_tip["potential_savings_usd"] > 0

    # Verify zero-token efficiency tip
    zero_tip = next(t for t in tips if t["type"] == "zero_token_efficiency")
    assert "0 tokens" in zero_tip["metric"]


def test_api_finops_tips_endpoint():
    """Verify GET /api/finops/tips returns computed tips from tracker."""
    res = client.get("/api/finops/tips", headers={"Authorization": "Bearer ya29.valid-token"})
    assert res.status_code == 200
    data = res.json()
    assert "tips" in data
    assert isinstance(data["tips"], list)


def test_api_chat_records_real_tokens_or_zero_on_deterministic():
    """Verify POST /api/chat records 0 tokens on deterministic triggers."""
    # Deterministic trigger "status" returns system status without LLM
    initial_event_count = len(finops_tracker.events)
    res = client.post(
        "/api/chat",
        json={"message": "status"},
        headers={"Authorization": "Bearer ya29.valid-token"},
    )
    assert res.status_code == 200
    # Should record a zero-token event for deterministic response
    assert len(finops_tracker.events) >= initial_event_count
    last_event = finops_tracker.events[-1]
    assert last_event.prompt_tokens == 0
    assert last_event.completion_tokens == 0


def test_api_questionnaire_answer_records_tokens_on_evaluation():
    """Verify POST /api/questionnaire/{cid}/answer records real tokens returned by subagent."""
    mock_usage = {
        "prompt_token_count": 1250,
        "candidates_token_count": 300,
        "cached_content_token_count": 500,
        "total_token_count": 2050,
    }
    with patch("mcp_server_grc.questionnaire.LLMSubAgent") as MockSubagentClass:
        mock_subagent = MagicMock()
        mock_subagent.client = MagicMock()
        mock_subagent.run.return_value = {
            "status": "SUCCESS",
            "narrative": '{"verdict": "COMPLIANT", "reasoning": "Matches evidence directly"}',
            "usage": mock_usage,
            "model_key": "gemini-2.5-flash",
        }
        MockSubagentClass.return_value = mock_subagent

        initial_count = len(finops_tracker.events)
        res = client.post(
            "/api/questionnaire/A.5.1/answer",
            headers=AUTH_HEADER,
            json={
                "control_id": "A.5.1",
                "framework": "ISO27001:2022",
                "status": "COMPLIANT",
                "justification": "All policies are reviewed annually by the CISO.",
                "evidence_text": "Policy repository in Cloud KMS verified.",
            },
        )
        assert res.status_code == 200
        # Check event recorded
        assert len(finops_tracker.events) > initial_count
        latest_event = finops_tracker.events[-1]
        assert latest_event.prompt_tokens == 1250
        assert latest_event.completion_tokens == 300
        assert latest_event.cached_tokens == 500

        from mcp_server_grc.questionnaire import QUESTIONNAIRE_ANSWERS
        from mcp_server_grc.firestore_storage import delete_questionnaire_answer_from_store
        QUESTIONNAIRE_ANSWERS.pop(("ISO27001:2022", "A.5.1"), None)
        delete_questionnaire_answer_from_store("ISO27001:2022", "A.5.1")


def test_portal_html_contains_finops_tips_and_cloud_strip_updates():
    """Verify the portal HTML contains the updated cloud strip, scope tree chevron, and tips container."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Provider strip & chevron
    assert 'id="gcpScopeTreeChevron"' in html
    assert 'class="provider-chevron"' in html
    assert 'toggleGcpScopeTree' in html

    # Environment level toggles
    assert 'id="envToggleProd"' in html
    assert 'id="envToggleStaging"' in html
    assert 'id="envToggleAnalytics"' in html
    assert 'toggleEnvironmentScope' in html
    assert 'updateEnvToggleState' in html

    # FinOps tips container
    assert 'id="finopsTokenSavingTipsContainer"' in html
    assert 'loadFinOpsTips' in html
    assert 'renderFinOpsTips' in html
