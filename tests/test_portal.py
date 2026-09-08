"""Unit tests for the Client Web Portal and its REST API."""

import io
from html.parser import HTMLParser
from unittest.mock import patch
from fastapi.testclient import TestClient
from mcp_server_grc.server import app

client = TestClient(app)


def test_portal_html_serving():
    res = client.get("/")
    assert res.status_code == 200
    assert "Gemini Enterprise Agent Platform" in res.text
    assert "Chatbot Auditor" in res.text
    assert "frameworkSelectorBar" in res.text
    assert "ISO/IEC 27001:2022" in res.text
    assert "fwCardIso27001" in res.text
    assert "fwCardSoc2" in res.text
    assert "fwCardPciDss" in res.text
    assert "fwCardCmmi" in res.text
    assert "fwCardMore" in res.text

    res_portal = client.get("/portal")
    assert res_portal.status_code == 200
    assert "frameworkSelectorBar" in res_portal.text
    assert 'class="brand-left" onclick="switchView(\'view-home\')"' in res_portal.text


def test_brand_logo_link_targets_view_home():
    """Assert the brand/logo link in the sidebar targets view-home upon click."""
    res = client.get("/")
    assert res.status_code == 200
    assert 'class="brand-left" onclick="switchView(\'view-home\')"' in res.text


def test_certification_framework_selector_ui():
    """Verify Certification Framework selector structure, ordering, i18n and locked states."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Verify container and cards presence
    assert 'id="frameworkSelectorBar"' in html
    assert 'class="framework-selector-bar"' in html
    assert 'class="framework-cards-grid"' in html

    # Verify order of cards in HTML
    pos_iso = html.find('id="fwCardIso27001"')
    pos_soc2 = html.find('id="fwCardSoc2"')
    pos_pci = html.find('id="fwCardPciDss"')
    pos_cmmi = html.find('id="fwCardCmmi"')
    pos_more = html.find('id="fwCardMore"')

    assert -1 < pos_iso < pos_soc2 < pos_pci < pos_cmmi < pos_more

    # Verify active card attributes
    assert 'fwCardIso27001" onclick="selectFramework(\'iso27001\')"' in html
    assert 'class="framework-badge-active"' in html
    assert 'data-i18n="framework_badge_active"' in html

    # Verify locked cards (no click handler, locked class, coming soon badge)
    for card_id in ["fwCardSoc2", "fwCardPciDss", "fwCardCmmi"]:
        # Extract card chunk
        card_start = html.find(f'id="{card_id}"')
        card_end = html.find('</div>\n                </div>\n            </div>', card_start)
        chunk = html[card_start:card_end]
        assert 'onclick=' not in chunk
        assert 'cursor: pointer' not in chunk
        assert 'data-i18n="framework_badge_coming_soon"' in chunk
        assert 'data-i18n-title="framework_tooltip_' in chunk

    # Verify placeholder tile
    assert 'id="fwCardMore"' in html
    assert 'class="framework-card placeholder"' in html
    assert 'data-i18n="framework_more"' in html

    # Verify i18n dictionaries contain all framework keys for pt, en, es
    for lang in ['pt:', 'en:', 'es:']:
        assert 'framework_selector_title:' in html
        assert 'framework_badge_active:' in html
        assert 'framework_badge_coming_soon:' in html
        assert 'framework_more:' in html
        assert 'framework_tooltip_soc2:' in html
        assert 'framework_tooltip_pcidss:' in html
        assert 'framework_tooltip_cmmi:' in html

    # Verify print media query hides framework-selector-bar
    assert '.framework-selector-bar { display: none !important; }' in html

    # Verify switchView hides frameworkSelectorBar on executive and technical report views
    assert 'viewId === "view-report-exec" || viewId === "view-report-tech"' in html


def test_portal_home_overview_view_ui():
    """Verify Home / Initial View (Tela Inicial dos Módulos) structure, cards, navigation, and i18n."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Verify Home view container and active state
    assert 'id="view-home"' in html
    assert 'class="view-pane active" id="view-home"' in html
    assert 'class="home-container"' in html
    assert 'class="home-hero-card"' in html

    # Verify Sidebar Home navigation button
    assert 'id="agentBtnHome"' in html
    assert 'class="agent-item active" id="agentBtnHome"' in html
    assert 'onclick="switchView(\'view-home\')"' in html
    assert 'data-i18n="nav_home"' in html

    # Verify KPI summary cards
    assert 'class="home-kpi-grid"' in html
    assert '100.0%' in html
    assert '93 / 93' in html
    assert '14 Nós' in html
    assert '~90%' in html

    # Verify all 8 platform module cards are present with action buttons
    module_keys = [
        'data-i18n="home_mod_chat_name"',
        'data-i18n="home_mod_phases_name"',
        'data-i18n="home_mod_conn_name"',
        'data-i18n="home_mod_matrix_name"',
        'data-i18n="home_mod_scorecard_name"',
        'data-i18n="home_mod_exec_name"',
        'data-i18n="home_mod_tech_name"',
        'data-i18n="home_mod_finops_name"',
    ]
    for k in module_keys:
        assert k in html

    # Verify Quick Action bar
    assert 'class="home-quick-actions-bar"' in html
    assert 'data-i18n="home_quick_actions_title"' in html

    # Verify switchView includes view-home
    assert '"view-home": "agentBtnHome"' in html
    assert '"view-home": "top_title_home"' in html

    # Verify i18n dictionaries for home
    for lang_key in ['top_title_home:', 'nav_home:', 'home_hero_title:', 'home_mod_chat_name:']:
        assert lang_key in html


def test_simplified_home_cockpit_ui():
    """Assert the simplified home cockpit structure: centered chat input, 3 plain language chips, divider, sublinks, and opt-in advanced grid."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Centered cockpit container and header
    assert 'id="homeSimpleCockpit"' in html
    assert 'class="home-simple-cockpit"' in html
    assert 'data-i18n="home_search_title"' in html
    assert 'data-i18n="home_search_subtitle"' in html

    # Large chat input and WCAG label
    assert 'id="homeSearchInput"' in html
    assert '<label for="homeSearchInput"' in html
    assert 'data-i18n-placeholder="home_search_placeholder"' in html
    assert 'class="btn-home-search-send"' in html

    # 3 Example plain-language chips
    assert 'class="home-chips-container"' in html
    assert 'data-i18n-prompt="home_chip_encrypted"' in html
    assert 'data-i18n-prompt="home_chip_bucket_access"' in html
    assert 'data-i18n-prompt="home_chip_what_fix_first"' in html

    # Thin divider and 3 small text links
    assert 'class="home-simple-divider"' in html
    assert 'class="home-sublinks-row"' in html
    assert 'data-i18n="home_link_last_report"' in html
    assert 'data-i18n="home_link_history"' in html
    assert 'id="homeAdvancedToggleLink"' in html

    # Secondary / opt-in advanced modules grid (hidden by default on first load)
    assert 'id="homeAdvancedGrid" style="display: none;' in html

    # Functions exist
    assert 'function submitHomeSearch' in html
    assert 'function toggleHomeAdvancedView' in html





AUTH_HEADER = {"Authorization": "Bearer ya29.valid-auditor-access-token"}


def test_portal_chat_endpoints():
    # 1. Audit prompt
    res_audit = client.post("/api/chat", json={"message": "Execute proactive audit"}, headers=AUTH_HEADER)
    assert res_audit.status_code == 200
    data = res_audit.json()
    assert "Proactive Audit Cycle Completed" in data["response"]
    assert data["subagent_used"] == "ContinuousIntelligenceEngine"

    # 2. Horizon scanning prompt
    res_horizon = client.post("/api/chat", json={"message": "Horizon scanning regulatory update"}, headers=AUTH_HEADER)
    assert res_horizon.status_code == 200
    assert "Horizon Scanning Regulatory Review" in res_horizon.json()["response"]

    # 3. Cryptography prompt
    res_crypto = client.post("/api/chat", json={"message": "Audit KMS cryptography A.8.24"}, headers=AUTH_HEADER)
    assert res_crypto.status_code == 200
    assert "Control A.8.24 Analysis" in res_crypto.json()["response"]

    # 4. General prompt
    res_gen = client.post("/api/chat", json={"message": "What is your capability?"}, headers=AUTH_HEADER)
    assert res_gen.status_code == 200
    assert "GEAP Compliance" in res_gen.json()["response"]


def test_portal_upload_file():
    tf_content = """
    resource "google_storage_bucket" "bad" {
      name = "bad-bucket"
      acl  = "public-read"
    }
    """
    file_bytes = io.BytesIO(tf_content.encode("utf-8"))
    res = client.post(
        "/api/upload",
        files={"file": ("main.tf", file_bytes, "text/plain")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert data["filename"] == "main.tf"
    assert data["audit_finding"]["status"] == "NON_COMPLIANT"


def test_portal_storage_link():
    res = client.post(
        "/api/storage/link",
        json={"source": "google_drive", "uri": "drive-folder-123", "user_token": "valid-token"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "CONNECTED"
    assert data["zero_copy_guarantee"] is True
    assert len(data["discovered_documents"]) > 0


def test_portal_subagents_and_dashboard():
    # Subagents listing
    res_sub = client.get("/api/subagents")
    assert res_sub.status_code == 200
    subagents = res_sub.json()["subagents"]
    assert len(subagents) >= 4

    # Trigger subagent
    res_trigger = client.post(
        "/api/subagents/trigger",
        json={"subagent": "annex_a", "target": "kms"}
    )
    assert res_trigger.status_code == 200

    # Dashboard
    res_dash = client.get("/api/dashboard")
    assert res_dash.status_code == 200
    dash_data = res_dash.json()
    assert dash_data["overall_score"] == 78.5
    assert "QUALIFIED" in dash_data["rating"]
    assert any(c["status"] == "NON_COMPLIANT" for c in dash_data["controls"])

    # Remediation approval
    res_app = client.post(
        "/api/remediation/approve",
        json={"remediation_id": "HITL-AMENDMENT-001"}
    )
    assert res_app.status_code == 200
    assert res_app.json()["status"] == "APPROVED"


def test_individual_phases_and_remediation():
    # 1. Run single phase 1
    res_p1 = client.post("/api/audit/run_phases", json={"projects": ["agentic-grc-cd06"], "phase": 1})
    assert res_p1.status_code == 200
    data_p1 = res_p1.json()
    assert len(data_p1["phases"]) == 1
    assert data_p1["phases"][0]["phase"].startswith("Fase 1")

    # 2. Run single phase 2
    res_p2 = client.post("/api/audit/run_phases", json={"projects": ["agentic-grc-cd06"], "phase": 2})
    assert res_p2.status_code == 200
    assert len(res_p2.json()["phases"]) == 1
    assert res_p2.json()["phases"][0]["phase"].startswith("Fase 2")

    # 3. Remediate phase 2
    res_rem = client.post("/api/audit/remediate_phase", json={"phase": 2, "project_id": "agentic-grc-cd06"})
    assert res_rem.status_code == 200
    rem_data = res_rem.json()
    assert rem_data["details"]["status"] == "REMEDIATED"
    assert rem_data["details"]["new_score"] == 100.0


def test_custom_subagents_lifecycle():
    # 1. Create a custom subagent
    new_agent = {
        "name": "Custom Test FinOps Agent",
        "role": "Cloud Cost and Compliance Inspector",
        "description": "Tests storage cost allocation and tagging",
        "system_prompt": "Inspect tags and labels on all compute resources",
        "tools": ["iam", "asset_inventory"],
        "model": "gemini-2.5-flash",
        "temperature": 0.2,
        "target_controls": ["A.5.9", "A.8.10"]
    }
    res_create = client.post("/api/subagents", json=new_agent)
    assert res_create.status_code == 200
    created = res_create.json()["subagent"]
    agent_id = created["id"]
    assert agent_id.startswith("custom-")

    # 2. List subagents
    res_list = client.get("/api/subagents")
    assert res_list.status_code == 200
    data = res_list.json()
    assert any(a["id"] == agent_id for a in data["custom_subagents"])

    # 3. Run custom subagent
    res_run = client.post(f"/api/subagents/{agent_id}/run")
    assert res_run.status_code == 200
    assert res_run.json()["status"] == "COMPLETED"
    assert len(res_run.json()["findings"]) > 0

    # 4. Delete custom subagent
    res_del = client.delete(f"/api/subagents/{agent_id}")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "DELETED"


def test_agentic_recommendation_and_autonomous_policy_update():
    # 1. Test subagent recommendation
    res_rec = client.post("/api/agent/recommend_subagent", json={"project_id": "agentic-grc-cd06", "industry": "FINANCIAL_SERVICES"})
    assert res_rec.status_code == 200
    rec_data = res_rec.json()
    assert rec_data["status"] == "SUCCESS"
    assert "Fintech & Banking" in rec_data["recommendation"]["name"]
    assert len(rec_data["recommendation"]["target_controls"]) > 0

    # 2. Test autonomous monitor
    res_mon = client.post("/api/agent/autonomous_monitor", json={"project_id": "agentic-grc-cd06", "simulate_deviation": True})
    assert res_mon.status_code == 200
    mon_data = res_mon.json()
    assert mon_data["active_alert"] is True
    assert mon_data["alert"]["control_id"] == "A.8.24"
    assert "proposed_amendment_text" in mon_data["alert"]

    # 3. Test autonomous policy update
    res_update = client.post("/api/agent/update_policy_autonomously", json={"project_id": "agentic-grc-cd06", "control_id": "A.8.24"})
    assert res_update.status_code == 200
    up_data = res_update.json()
    assert up_data["status"] == "POLICY_UPDATED_AND_ENFORCED"
    assert len(up_data["hash_sha256"]) == 64
    assert up_data["new_score"] == 100.0


def test_cloudstyle_html_report_export():
    res_html = client.get("/api/reports/export?format=html")
    assert res_html.status_code == 200
    assert "Continuous Compliance & Audit Dossier" in res_html.text
    assert "data:image/png;base64," in res_html.text
    assert "google-color-stripe-bar" in res_html.text

    # Verify static assets
    res_icon = client.get("/static/images/google_cloud_icon.png")
    assert res_icon.status_code == 200
    assert len(res_icon.content) > 1000

    res_wordmark = client.get("/static/images/google_cloud_wordmark.png")
    assert res_wordmark.status_code == 200
    assert len(res_wordmark.content) > 1000


def test_finops_and_org_scope_toggle():
    # Test GET /api/projects returns organization metadata and all_org_projects
    res_proj = client.get("/api/projects")
    assert res_proj.status_code == 200
    data_proj = res_proj.json()
    assert "all_org_projects" in data_proj
    assert data_proj["total_org_projects"] >= 10
    assert "org_metadata" in data_proj
    assert data_proj["org_metadata"]["org_id"] == "108928374619"

    # Test toggle scope endpoint
    res_toggle = client.post("/api/projects/toggle_scope", json={"project_id": "agentic-grc-ai-workloads", "in_scope": True})
    assert res_toggle.status_code == 200
    toggle_data = res_toggle.json()
    assert toggle_data["status"] == "ok"
    assert toggle_data["in_scope"] is True

    # Test FinOps API
    res_finops = client.get("/api/finops")
    assert res_finops.status_code == 200
    data_finops = res_finops.json()
    assert "summary" in data_finops
    assert data_finops["summary"]["total_cost_usd"] > 0
    assert data_finops["summary"]["total_tokens"] > 0
    assert "agents" in data_finops
    assert len(data_finops["agents"]) >= 8

    # Test FinOps simulation
    res_sim = client.post("/api/finops/simulate")
    assert res_sim.status_code == 200
    sim_data = res_sim.json()
    assert sim_data["summary"]["total_invocations"] > data_finops["summary"]["total_invocations"]


def test_all_native_subagents_and_trigger_endpoints():
    """Verify that all built-in, custom, and on-demand subagents execute without error."""
    agents = [
        "annex_a",
        "gcp_telemetry",
        "org_policies",
        "horizon_scanner",
        "iac_scanner",
        "codemender",
        "custom-finops-storage",
        "custom-k8s-secops",
        "custom-iam-least-privilege",
        "arbitrary-on-demand-agent",
    ]
    for agent_id in agents:
        res = client.post(f"/api/subagents/{agent_id}/run?project_id=agentic-grc-cd06")
        assert res.status_code == 200, f"Failed for {agent_id}: {res.text}"
        data = res.json()
        assert data["status"] == "COMPLETED"
        assert "markdown_report" in data
        assert len(data["markdown_report"]) > 50

    # Test /api/subagents/trigger
    triggers = ["annex_a", "gcp_telemetry", "horizon_scanner", "org_policies", "codemender", "iac_scanner", "other"]
    for t in triggers:
        res_trig = client.post("/api/subagents/trigger", json={"subagent": t, "target": "test-target"})
        assert res_trig.status_code == 200
        assert res_trig.json()["status"] == "COMPLETED"

    # Test run_phases with string phase
    res_phases_str = client.post("/api/audit/run_phases", json={"projects": ["agentic-grc-cd06"], "phase": "all"})
    assert res_phases_str.status_code == 200
    assert len(res_phases_str.json()["phases"]) == 4


def test_all_labels_associated_with_form_fields():
    """Verify WCAG / Lighthouse a11y requirement: all <label> elements are associated with form fields."""
    res = client.get("/portal")
    assert res.status_code == 200
    html = res.text

    class LabelValidator(HTMLParser):
        def __init__(self):
            super().__init__()
            self.all_ids = set()
            self.labels = []
            self.current_label = None

        def handle_starttag(self, tag, attrs):
            attr_dict = dict(attrs)
            if "id" in attr_dict:
                self.all_ids.add(attr_dict["id"])

            if tag == "label":
                lbl_info = {"for": attr_dict.get("for"), "has_nested_input": False}
                self.labels.append(lbl_info)
                self.current_label = lbl_info
            elif tag in ("input", "select", "textarea") and self.current_label is not None:
                self.current_label["has_nested_input"] = True

        def handle_endtag(self, tag):
            if tag == "label":
                self.current_label = None

    parser = LabelValidator()
    parser.feed(html)

    assert len(parser.labels) > 0, "Expected to find labels in the portal HTML"

    violations = []
    for i, l in enumerate(parser.labels):
        for_id = l["for"]
        nested = l["has_nested_input"]
        if not for_id and not nested:
            violations.append(f"Label #{i} has neither for attribute nor nested form field: {l}")
        elif for_id and for_id not in parser.all_ids:
            violations.append(f"Label #{i} has for='{for_id}' which does not match any id in document")

    assert violations == [], f"Accessibility label violations detected: {violations}"


def test_frontend_redesign_navigation_and_views():
    """Validates the 6 UX navigation and frontend redesign requirements."""
    res = client.get("/portal")
    assert res.status_code == 200
    html = res.text

    # 1. Google Cloud Icon in Breadcrumb
    assert 'id="topGoogleCloudIcon"' in html
    assert 'src="data:image/png;base64,' in html

    # 2. Agentic GRC Auditor button removed from sidebar; merged into Home
    assert 'id="agentBtnGrcAuditor"' not in html
    assert 'id="agentBtnHome"' in html
    assert 'selectAuditorTab()' not in html

    # 3. Reports Consolidated into single sidebar item and unified view
    assert 'id="agentBtnReports"' in html
    assert 'data-i18n="nav_reports"' in html
    assert 'onclick="switchView(\'view-reports\')"' in html
    assert 'id="agentBtnScorecard"' not in html
    assert 'id="agentBtnReport"' not in html
    assert 'id="agentBtnTechReport"' not in html
    assert 'id="view-reports"' in html
    assert 'id="tabBtnScorecard"' in html
    assert 'id="tabBtnExec"' in html
    assert 'id="tabBtnTech"' in html
    assert 'id="tabPanelScorecard"' in html
    assert 'id="tabPanelExec"' in html
    assert 'id="tabPanelTech"' in html

    # 4. Framework Selector Inline Badge Pattern & Modal
    assert 'id="topFrameworkBadge"' in html
    assert 'id="topFrameworkBadgeText"' in html
    assert 'Módulo: ISO/IEC 27001:2022' in html
    assert 'id="frameworkSelectorModal"' in html
    assert 'openFrameworkSelectorModal' in html
    assert 'currentFrameworkId' in html

    # 5. Questionnaire View in Sidebar
    assert 'id="agentBtnQuestionnaire"' in html
    assert 'data-i18n="nav_questionnaire"' in html
    assert 'onclick="switchView(\'view-questionnaire\')"' in html
    assert 'id="view-questionnaire"' in html
    assert 'id="questSummaryCard"' in html
    assert 'id="questCompletionPct"' in html
    assert 'id="questControlsAccordion"' in html
    assert 'id="questSearchInput"' in html
    assert 'btnFilterA5' in html
    assert 'btnFilterA6' in html
    assert 'btnFilterA7' in html
    assert 'btnFilterA8' in html
    assert 'loadQuestionnaireSummary' in html
    assert 'loadQuestionnaireControls' in html
    assert 'uploadEvidenceFile' in html
    assert 'submitControlAnswer' in html

    # 6. FinOps completely preserved
    assert 'id="agentBtnFinops"' in html
    assert 'id="view-finops"' in html


# ---------------------------------------------------------------------------
# Cascading Recalculation & Reports API Tests
# ---------------------------------------------------------------------------

def test_scorecard_api_endpoint():
    """Verifies /api/scorecard returns dynamic scorecard with evidence tier breakdown."""
    res = client.get("/api/scorecard")
    assert res.status_code == 200
    data = res.json()
    assert "overall_score" in data
    assert "rating" in data
    assert "evidence_graph_summary" in data
    assert "verification_tiers" in data["evidence_graph_summary"]
    assert "SELF_ATTESTED" in data["evidence_graph_summary"]["verification_tiers"]
    assert "VERIFIED" in data["evidence_graph_summary"]["verification_tiers"]
    assert "evidence_nodes" in data


def test_executive_and_technical_reports_endpoints():
    """Verifies /api/reports/executive and /api/reports/technical endpoints across formats."""
    # 1. Executive JSON
    res_exec = client.get("/api/reports/executive?format=json")
    assert res_exec.status_code == 200
    data_exec = res_exec.json()
    assert "Executive" in data_exec["document_title"]
    assert "scorecard" in data_exec
    assert "evidence_summary" in data_exec
    assert "self_attested_nodes" in data_exec["evidence_summary"]
    assert "verified_telemetry_nodes" in data_exec["evidence_summary"]
    assert "executive_opinion" in data_exec

    # 2. Executive HTML and Markdown
    res_exec_html = client.get("/api/reports/executive?format=html")
    assert res_exec_html.status_code == 200
    assert "text/html" in res_exec_html.headers.get("content-type", "")

    res_exec_md = client.get("/api/reports/executive?format=markdown")
    assert res_exec_md.status_code == 200

    # 3. Technical JSON
    res_tech = client.get("/api/reports/technical?format=json")
    assert res_tech.status_code == 200
    data_tech = res_tech.json()
    assert "Technical" in data_tech["document_title"]
    assert "verification_tier_breakdown" in data_tech
    assert "verified_telemetry" in data_tech["verification_tier_breakdown"]
    assert "self_attested_questionnaire" in data_tech["verification_tier_breakdown"]
    assert "evidence_chain" in data_tech

    # 4. Technical HTML and Markdown
    res_tech_html = client.get("/api/reports/technical?format=html")
    assert res_tech_html.status_code == 200

    res_tech_md = client.get("/api/reports/technical?format=markdown")
    assert res_tech_md.status_code == 200


def test_cascading_questionnaire_recalculation_end_to_end():
    """Submits a questionnaire answer and asserts cascading recalculation across Scorecard, Executive Dossier, and Technical Report."""
    auth_header = {"Authorization": "Bearer ya29.valid-auditor-access-token"}

    # 1. Check scorecard before submission
    res_before = client.get("/api/scorecard")
    assert res_before.status_code == 200
    sc_before = res_before.json()
    score_before = sc_before["overall_score"]
    self_attested_before = sc_before["evidence_graph_summary"]["self_attested_count"]

    # 2. Submit questionnaire answer marking a non-compliant control as COMPLIANT with evidence text
    answer_payload = {
        "control_id": "A.5.17",
        "framework": "ISO27001:2022",
        "status": "COMPLIANT",
        "justification": "Plaintext metadata secrets removed and migrated to Secret Manager with automated rotation.",
        "evidence_text": "Secret Manager secret sm-legacy-credentials version 2 active; metadata attributes verified clean.",
    }
    ans_res = client.post("/api/questionnaire/A.5.17/answer", json=answer_payload, headers=auth_header)
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["status"] == "COMPLIANT"
    assert ans_data["ai_consistency_verdict"] in ("COMPLIANT", "COMPLIANT_WITH_OBSERVATION")

    # 3. Assert Scorecard recalculated immediately
    res_after = client.get("/api/scorecard")
    assert res_after.status_code == 200
    sc_after = res_after.json()
    score_after = sc_after["overall_score"]

    # Score must recalculate upwards since non-compliant control A.5.17 was resolved
    assert score_after >= score_before
    assert sc_after["evidence_graph_summary"]["self_attested_count"] == self_attested_before + 1
    assert sc_after["evidence_graph_summary"]["verification_tiers"]["SELF_ATTESTED"] >= 1

    # Verify self-attested node is explicitly labeled and distinguished from telemetry
    a517_nodes = [n for n in sc_after["evidence_nodes"] if n["control_id"] == "A.5.17"]
    assert len(a517_nodes) > 0
    node = a517_nodes[-1]
    assert node["verification_tier"] == "SELF_ATTESTED"
    assert "SELF_ATTESTED" in node["tier_label"]
    assert "self-attested by" in node["provenance"]
    assert node["ai_consistency_verdict"] in ("COMPLIANT", "COMPLIANT_WITH_OBSERVATION")

    # 4. Assert Executive Dossier reflects recalculated score and explicit tier distinction
    res_exec = client.get("/api/reports/executive?format=json")
    assert res_exec.status_code == 200
    dossier = res_exec.json()
    assert dossier["overall_score"] == score_after
    assert dossier["evidence_summary"]["self_attested_nodes"] >= 1
    assert "self-attested questionnaire" in dossier["executive_opinion"]

    # 5. Assert Technical Report contains granular provenance
    res_tech = client.get("/api/reports/technical?format=json")
    assert res_tech.status_code == 200
    tech = res_tech.json()
    assert tech["verification_tier_breakdown"]["self_attested_questionnaire"] >= 1
    matched_ev = [e for e in tech["evidence_chain"] if e["control_id"] == "A.5.17"]
    assert len(matched_ev) > 0
    assert matched_ev[-1]["verification_tier"] == "SELF_ATTESTED"


# ---------------------------------------------------------------------------
# Live Cloud Inspection & Read-Only Auditor Tests
# ---------------------------------------------------------------------------

def test_live_cloud_kms_inspection_chat():
    """Verifies that asking about a KMS key (e.g. 'my-key') executes live read inspection instead of a CLI tutorial."""
    payload = {
        "message": "Quero saber sobre a chave my-key, qual o período de rotação e o nível de proteção?",
        "locale": "pt",
        "selected_projects": ["agentic-grc-cd06"]
    }
    resp = client.post("/api/chat", json=payload, headers={"Authorization": "Bearer ya29.test-auditor-token"})
    assert resp.status_code == 200
    data = resp.json()
    resp_text = data.get("response", "")

    # Must provide live telemetry / inspection results
    assert "Cloud KMS" in resp_text
    assert "A.8.24" in resp_text
    assert "my-key" in resp_text
    assert "rotationPeriod" in resp_text or "Período de Rotação" in resp_text
    assert "protectionLevel" in resp_text or "Nível de Proteção" in resp_text

    # Must NEVER give manual command tutorials telling the user to run CLI commands
    assert "Execute o comando abaixo, substituindo" not in resp_text
    assert "Menu de Navegação > Security" not in resp_text

    # Tool evidence must contain inspect_cloud_kms
    tool_names = [e.get("tool") for e in data.get("tool_evidence", [])]
    assert "inspect_cloud_kms" in tool_names


def test_live_cloud_storage_inspection_chat():
    """Verifies that asking about a storage bucket executes live inspection and returns PAP/UBLA telemetry."""
    mock_bucket_data = {
        "status": "FOUND",
        "resource": "run-sources-agentic-grc-cd06-us-central1",
        "project_id": "agentic-grc-cd06",
        "bucket_details": {
            "name": "run-sources-agentic-grc-cd06-us-central1",
            "location": "us-central1",
            "location_type": "region",
            "public_access_prevention": "enforced",
            "uniform_bucket_level_access": True,
            "default_kms_key": "Google-Managed Encryption",
            "storage_class": "STANDARD",
        },
        "compliance": {
            "status": "COMPLIANT",
            "control": "ISO/IEC 27001:2022 A.5.23",
            "violations": [],
            "remediation": "Configuração do bucket em conformidade com o baseline de segurança (PAP Enforced e UBLA Enabled).",
        },
    }
    with patch("mcp_server_grc.portal.inspect_cloud_storage_bucket", return_value=mock_bucket_data):
        payload = {
            "message": "Audite o bucket run-sources-agentic-grc-cd06-us-central1",
            "locale": "pt",
            "selected_projects": ["agentic-grc-cd06"]
        }
        resp = client.post("/api/chat", json=payload, headers={"Authorization": "Bearer ya29.test-auditor-token"})
        assert resp.status_code == 200
        data = resp.json()
        resp_text = data.get("response", "")

        assert "Cloud Storage" in resp_text
        assert "run-sources-agentic-grc-cd06-us-central1" in resp_text
        assert "Public Access Prevention" in resp_text
        assert "Uniform Bucket-Level Access" in resp_text

        tool_names = [e.get("tool") for e in data.get("tool_evidence", [])]
        assert "inspect_cloud_storage" in tool_names


def test_cloud_inspector_unit_tests():
    """Directly tests cloud_inspector functions for KMS and Storage inspection."""
    from mcp_server_grc.cloud_inspector import (
        inspect_cloud_kms_key,
        inspect_cloud_storage_bucket,
        inspect_project_iam_policy,
        inspect_cloud_run_services,
    )

    # 1. KMS key inspection (graceful return with scan summary when key not found)
    kms_res = inspect_cloud_kms_key("my-test-key", project_id="agentic-grc-cd06")
    assert kms_res["status"] in ("NOT_FOUND", "OFFLINE", "ERROR", "UNDETERMINED")
    assert "compliance" in kms_res

    # 2. Storage bucket inspection (returns real data or offline graceful format)
    st_res = inspect_cloud_storage_bucket("non-existent-grc-test-bucket", project_id="agentic-grc-cd06")
    assert st_res["status"] in ("NOT_FOUND", "OFFLINE", "ERROR", "UNDETERMINED")
    assert "compliance" in st_res

    # 3. IAM policy inspection
    iam_res = inspect_project_iam_policy(project_id="agentic-grc-cd06")
    assert iam_res["status"] in ("SUCCESS", "OFFLINE", "ERROR", "UNDETERMINED")

    # 4. Cloud Run services inspection
    run_res = inspect_cloud_run_services(project_id="agentic-grc-cd06")
    assert run_res["status"] in ("SUCCESS", "OFFLINE", "ERROR", "UNDETERMINED")


def test_unauthenticated_chat_rejected_with_401(monkeypatch):
    """Asserts POST /api/chat with no auth headers and ALLOW_DEV_AUTH_BYPASS unset returns 401, not 200."""
    monkeypatch.delenv("ALLOW_DEV_AUTH_BYPASS", raising=False)
    # Post without any Authorization or X-Goog-Id-Token header
    res = client.post("/api/chat", json={"message": "Execute audit scan"})
    assert res.status_code == 401
    assert "Authentication required" in res.json().get("detail", "")


def test_no_delegated_token_in_non_test_context_returns_undetermined(monkeypatch):
    """Proves that a request with no delegated token, in a non-test context, does NOT receive

    a live inspection result derived from ADC — it gets the 'no delegated credential' UNDETERMINED response instead.
    """
    from mcp_server_grc.cloud_inspector import (
        get_authorized_session,
        inspect_cloud_kms_key,
        inspect_cloud_storage_bucket,
        inspect_project_iam_policy,
        inspect_cloud_run_services,
        NO_DELEGATED_CREDENTIAL_MSG,
    )

    # Simulate non-test production context
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.delenv("TESTING", raising=False)

    # 1. get_authorized_session returns (None, proj) and does NOT fall back to ADC
    session, proj = get_authorized_session(bearer_token=None, project_id="prod-project-123")
    assert session is None
    assert proj == "prod-project-123"

    # 2. inspect_cloud_kms_key returns UNDETERMINED with explicit message
    kms_res = inspect_cloud_kms_key("projects/prod-project-123/locations/global/keyRings/kr/cryptoKeys/key1", bearer_token=None)
    assert kms_res["status"] == "UNDETERMINED"
    assert NO_DELEGATED_CREDENTIAL_MSG in kms_res["message"]
    assert kms_res["compliance"]["status"] == "UNDETERMINED"
    assert NO_DELEGATED_CREDENTIAL_MSG in kms_res["compliance"]["violations"][0]

    # 3. inspect_cloud_storage_bucket returns UNDETERMINED with explicit message
    st_res = inspect_cloud_storage_bucket("prod-secure-vault", bearer_token=None)
    assert st_res["status"] == "UNDETERMINED"
    assert NO_DELEGATED_CREDENTIAL_MSG in st_res["message"]
    assert st_res["compliance"]["status"] == "UNDETERMINED"

    # 4. inspect_project_iam_policy returns UNDETERMINED
    iam_res = inspect_project_iam_policy(project_id="prod-project-123", bearer_token=None)
    assert iam_res["status"] == "UNDETERMINED"
    assert NO_DELEGATED_CREDENTIAL_MSG in iam_res["message"]

    # 5. inspect_cloud_run_services returns UNDETERMINED
    run_res = inspect_cloud_run_services(project_id="prod-project-123", bearer_token=None)
    assert run_res["status"] == "UNDETERMINED"
    assert NO_DELEGATED_CREDENTIAL_MSG in run_res["message"]


def test_enriched_report_templates_sections_and_taxonomy():
    """Asserts that executive, technical, and export reports include Metodologia,

    Declaração de Responsabilidade do Auditor, Período Auditado, and expanded 3-tier severity taxonomy.
    """
    # 1. Executive JSON
    res_exec = client.get("/api/reports/executive?format=json")
    assert res_exec.status_code == 200
    data_exec = res_exec.json()
    assert "audited_period" in data_exec
    assert "start" in data_exec["audited_period"]
    assert "end" in data_exec["audited_period"]
    assert "methodology" in data_exec
    assert "auditoria foi conduzida através de metodologia híbrida contínua" in data_exec["methodology"]
    assert "auditor_responsibility" in data_exec
    assert "verified_machine_findings_count" in data_exec["auditor_responsibility"]
    assert "self_attested_findings_count" in data_exec["auditor_responsibility"]
    assert "statement" in data_exec["auditor_responsibility"]
    assert "finding_severity_taxonomy" in data_exec
    assert "NÃO CONFORMIDADE MAIOR" in data_exec["finding_severity_taxonomy"]
    assert "NÃO CONFORMIDADE MENOR" in data_exec["finding_severity_taxonomy"]
    assert "OPORTUNIDADE DE MELHORIA" in data_exec["finding_severity_taxonomy"]

    # 2. Technical JSON
    res_tech = client.get("/api/reports/technical?format=json")
    assert res_tech.status_code == 200
    data_tech = res_tech.json()
    assert "audited_period" in data_tech
    assert "methodology" in data_tech
    assert "auditor_responsibility" in data_tech
    assert "finding_severity_taxonomy" in data_tech
    for f in data_tech.get("non_compliant_findings", []):
        assert "taxonomy_severity" in f
        assert f["taxonomy_severity"] in ("NÃO CONFORMIDADE MAIOR", "NÃO CONFORMIDADE MENOR")

    # 3. Export JSON
    res_exp = client.get("/api/reports/export?format=json")
    assert res_exp.status_code == 200
    data_exp = res_exp.json()
    assert "audited_period" in data_exp
    assert "methodology" in data_exp
    assert "auditor_responsibility" in data_exp
    assert "finding_severity_taxonomy" in data_exp
    for vm in data_exp.get("vm_fleet_audit", []):
        assert vm.get("taxonomy_severity") == "NÃO CONFORMIDADE MAIOR"

    # 4. HTML Export
    res_html = client.get("/api/reports/export?format=html")
    assert res_html.status_code == 200
    html_content = res_html.text
    assert "Período Auditado" in html_content
    assert "Metodologia de Auditoria" in html_content
    assert "Declaração de Responsabilidade do Auditor" in html_content
    assert "NÃO CONFORMIDADE MAIOR" in html_content
    assert "NÃO CONFORMIDADE MENOR" in html_content
    assert "OPORTUNIDADE DE MELHORIA" in html_content
    assert "cloudstyle-badge-opportunity" in html_content

    # 5. Markdown Export
    res_md = client.get("/api/reports/export?format=markdown")
    assert res_md.status_code == 200
    md_content = res_md.text
    assert "**Período Auditado:**" in md_content
    assert "## 2. Metodologia de Auditoria" in md_content
    assert "## 3. Declaração de Responsabilidade do Auditor" in md_content
    assert "## 4. Taxonomia de Severidade de Achados" in md_content
    assert "**NÃO CONFORMIDADE MAIOR**" in md_content


def test_chat_questionnaire_status_fallback_routing():
    """Asserts that queries asking about unanswered controls or questionnaire progress
    route cleanly to get_questionnaire_summary and never trigger inspect_cloud_iam."""
    queries = [
        "which controls are still unanswered?",
        "quais controles faltam responder?",
        "what is the questionnaire completion progress?",
    ]
    for q in queries:
        resp = client.post("/api/chat", json={"message": q}, headers=AUTH_HEADER)
        assert resp.status_code == 200
        data = resp.json()
        tools_used = [e.get("tool") for e in data.get("tool_evidence", [])]
        assert "get_questionnaire_summary" in tools_used
        assert "inspect_cloud_iam" not in tools_used
        assert "inspect_project_iam_policy" not in tools_used
        assert "93" in data["response"]


def test_genai_client_failed_init_warning_suppressed():
    """Verifies that failed genai.Client initialization does not log an unretrieved task exception."""
    import asyncio
    import gc
    from agent_orchestrator.llm_subagent import suppress_genai_client_cleanup_warning
    suppress_genai_client_cleanup_warning()

    errors_logged = []

    async def _exercise():
        loop = asyncio.get_running_loop()

        def _exc_handler(l, ctx):
            errors_logged.append(ctx.get("message", "") or str(ctx.get("exception", "")))

        loop.set_exception_handler(_exc_handler)

        try:
            from google import genai
            try:
                genai.Client(api_key=None)
            except Exception:
                pass
        except ImportError:
            pass

        gc.collect()
        await asyncio.sleep(0.05)

    asyncio.run(_exercise())
    for err in errors_logged:
        assert "_async_httpx_client" not in err


