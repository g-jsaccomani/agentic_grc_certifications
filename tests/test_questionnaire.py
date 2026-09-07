"""Comprehensive unit tests for Questionnaire, Evidence Upload, Magic Byte Sniffing & Multi-Framework Support."""

import io
import os
import zipfile
import pytest
from fastapi.testclient import TestClient

from mcp_server_grc.server import app
from mcp_server_grc.auth import create_mock_id_token
from mcp_server_grc.portal import ci_engine
from agent_orchestrator.evidence_graph import EvidenceNode, ComplianceLink, EvidenceVerificationTier
from mcp_server_grc.questionnaire import QuestionnaireAnswer, sniff_and_validate_evidence_file

client = TestClient(app)

AUTH_HEADER = {"Authorization": "Bearer ya29.valid-auditor-access-token"}
MOCK_ID_TOKEN = create_mock_id_token(email="auditor@client.corp")
ID_TOKEN_HEADER = {"X-Goog-Id-Token": MOCK_ID_TOKEN}


# ---------------------------------------------------------------------------
# 1. Multi-Framework Data Model Unit Tests
# ---------------------------------------------------------------------------

def test_data_model_framework_fields():
    """Verifies that framework field exists with default ISO27001:2022 on all structures."""
    # QuestionnaireAnswer
    ans = QuestionnaireAnswer(
        control_id="A.5.1",
        status="COMPLIANT",
        justification="Information security policy approved and published.",
    )
    assert ans.framework == "ISO27001:2022"

    ans_soc2 = QuestionnaireAnswer(
        control_id="CC6.1",
        framework="SOC2",
        status="COMPLIANT",
        justification="Logical access controls enforced.",
    )
    assert ans_soc2.framework == "SOC2"

    # EvidenceNode
    node = EvidenceNode(
        node_id="ev-123",
        resource_type="questionnaire_response",
        resource_id="questionnaire-A.5.1",
        control_id="A.5.1",
        verification_tier=EvidenceVerificationTier.VERIFIED,
        raw_payload={"test": "val"},
    )
    assert node.framework == "ISO27001:2022"
    assert "ISO27001:2022:questionnaire-A.5.1:A.5.1:" in node.evidence_hash or len(node.evidence_hash) == 64

    # ComplianceLink
    link = ComplianceLink(
        source_node_id="ev-node-A.5.1",
        control_id="A.5.1",
        status="COMPLIANT",
        justification="Policy active.",
    )
    assert link.framework == "ISO27001:2022"


# ---------------------------------------------------------------------------
# 2. Authentication Enforcement Tests
# ---------------------------------------------------------------------------

def test_unauthenticated_upload_rejected(monkeypatch):
    """Ensures unauthenticated requests return 401."""
    monkeypatch.setenv("ALLOW_DEV_AUTH_BYPASS", "false")
    png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30
    files = {"file": ("audit_evidence.png", io.BytesIO(png_data), "image/png")}

    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files)
    assert res.status_code == 401
    assert "Authentication required" in res.json().get("detail", "")


def test_unauthenticated_download_rejected(monkeypatch):
    """Ensures unauthenticated download requests return 401."""
    monkeypatch.setenv("ALLOW_DEV_AUTH_BYPASS", "false")
    res = client.get("/api/questionnaire/A.5.1/evidence-file/some-file-id")
    assert res.status_code == 401
    assert "Authentication required" in res.json().get("detail", "")


def test_unauthenticated_answer_rejected(monkeypatch):
    """Ensures unauthenticated questionnaire answer submissions return 401."""
    monkeypatch.setenv("ALLOW_DEV_AUTH_BYPASS", "false")
    payload = {
        "control_id": "A.5.1",
        "framework": "ISO27001:2022",
        "status": "COMPLIANT",
        "justification": "Approved policies.",
    }
    res = client.post("/api/questionnaire/A.5.1/answer", json=payload)
    assert res.status_code == 401
    assert "Authentication required" in res.json().get("detail", "")


# ---------------------------------------------------------------------------
# 3. Magic Byte Sniffing & Rejection Tests
# ---------------------------------------------------------------------------

def test_reject_renamed_executable():
    """Windows PE (.exe/.dll) renamed as .png is rejected by magic bytes."""
    fake_png = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff" + b"\x00" * 50
    files = {"file": ("malware.png", io.BytesIO(fake_png), "image/png")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Disallowed binary format: Windows PE" in res.json()["detail"]


def test_reject_linux_elf():
    """Linux ELF executable renamed as .jpg is rejected by magic bytes."""
    elf_data = b"\x7fELF\x02\x01\x01\x00" + b"\x00" * 40
    files = {"file": ("payload.jpg", io.BytesIO(elf_data), "image/jpeg")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Disallowed binary format: Linux ELF" in res.json()["detail"]


def test_reject_mach_o():
    """Mach-O binary is rejected by magic bytes."""
    macho_data = b"\xfe\xed\xfa\xcf" + b"\x00" * 40
    files = {"file": ("tool.png", io.BytesIO(macho_data), "image/png")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Disallowed binary format: Mach-O" in res.json()["detail"]


def test_reject_executable_script_shebang():
    """Script with shebang line is rejected outright."""
    script_data = b"#!/usr/bin/env bash\necho 'dangerous script'\n"
    files = {"file": ("setup.sh", io.BytesIO(script_data), "text/plain")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Executable scripts (shebang #!) are strictly prohibited" in res.json()["detail"]


def test_reject_svg_files():
    """SVG files are strictly rejected due to embedded JavaScript risk."""
    svg_data = b"<svg xmlns=\"http://www.w3.org/2000/svg\"><script>alert(1)</script></svg>"
    files = {"file": ("diagram.svg", io.BytesIO(svg_data), "image/svg+xml")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "SVG files are strictly prohibited" in res.json()["detail"]


def test_reject_svg_renamed_as_png():
    """SVG content masquerading as .png is rejected."""
    svg_data = b"<svg viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"40\"/></svg>"
    files = {"file": ("icon.png", io.BytesIO(svg_data), "image/png")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "SVG files are strictly prohibited" in res.json()["detail"]


def test_reject_html_active_content():
    """HTML active content is rejected."""
    html_data = b"<!DOCTYPE html><html><head><title>Phish</title></head><body>Login</body></html>"
    files = {"file": ("page.html", io.BytesIO(html_data), "text/html")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "HTML active content" in res.json()["detail"]


def test_reject_generic_zip_archive():
    """Generic zip archive is rejected."""
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zf:
        zf.writestr("test.txt", "hello")
    files = {"file": ("archive.zip", io.BytesIO(zip_buf.getvalue()), "application/zip")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Disallowed archive format" in res.json()["detail"]


def test_reject_office_with_macros():
    """Office document with macros (vbaProject.bin) is rejected."""
    doc_buf = io.BytesIO()
    with zipfile.ZipFile(doc_buf, "w") as zf:
        zf.writestr("word/document.xml", "<w:document><w:body><w:p><w:t>Macro test</w:t></w:p></w:body></w:document>")
        zf.writestr("word/vbaProject.bin", b"VBA MACRO PAYLOAD")
    files = {"file": ("policy.docm", io.BytesIO(doc_buf.getvalue()), "application/vnd.ms-word.document.macroEnabled.12")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Macros (.docm, .xlsm, .pptm, VBA) detected" in res.json()["detail"]


def test_reject_empty_file():
    """Empty 0-byte file is rejected."""
    files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Empty file uploaded" in res.json()["detail"]


def test_reject_oversized_file_header():
    """Files exceeding 8MB are rejected by Content-Length header before reading."""
    huge_header = {**AUTH_HEADER, "Content-Length": str(9 * 1024 * 1024)}
    files = {"file": ("huge.png", io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 10), "image/png")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=huge_header)
    assert res.status_code == 400
    assert "exceeds maximum allowed limit of 8MB" in res.json()["detail"]


def test_reject_oversized_file_streaming():
    """Files exceeding 8MB are aborted during stream reading without buffering into memory."""
    stream_data = b"\x89PNG\r\n\x1a\n" + b"A" * (8 * 1024 * 1024 + 1024)
    files = {"file": ("large.png", io.BytesIO(stream_data), "image/png")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "exceeds maximum allowed limit of 8MB" in res.json()["detail"]


# ---------------------------------------------------------------------------
# 4. Valid Uploads, Safe Storage & Download Tests
# ---------------------------------------------------------------------------

def test_valid_png_upload_and_download():
    """Legitimate PNG uploads successfully, stores binary, and serves with safe attachment headers."""
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
    files = {"file": ("architecture_diagram.png", io.BytesIO(png_bytes), "image/png")}

    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "binary"
    assert data["content_type"] == "image/png"
    assert data["control_id"] == "A.5.1"
    file_id = data["file_id"]

    # Now download via safe serving endpoint
    dl_res = client.get(f"/api/questionnaire/A.5.1/evidence-file/{file_id}", headers=AUTH_HEADER)
    assert dl_res.status_code == 200
    assert dl_res.content == png_bytes
    assert dl_res.headers["content-type"] == "image/png"
    assert "attachment; filename=" in dl_res.headers["content-disposition"]
    assert "architecture_diagram.png" in dl_res.headers["content-disposition"]
    assert dl_res.headers["x-content-type-options"] == "nosniff"


def test_valid_jpeg_upload():
    """Legitimate JPEG uploads successfully."""
    jpeg_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb"
    files = {"file": ("datacenter_badge.jpg", io.BytesIO(jpeg_bytes), "image/jpeg")}
    res = client.post("/api/questionnaire/A.7.2/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "binary"
    assert data["content_type"] == "image/jpeg"


def test_valid_webp_upload():
    """Legitimate WEBP uploads successfully."""
    webp_bytes = b"RIFF\x1a\x00\x00\x00WEBPVP8 \x0e\x00\x00\x00" + b"\x00" * 14
    files = {"file": ("badge.webp", io.BytesIO(webp_bytes), "image/webp")}
    res = client.post("/api/questionnaire/A.7.2/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "binary"
    assert data["content_type"] == "image/webp"


def test_valid_plain_text_upload():
    """Legitimate TXT, CSV, MD files upload successfully."""
    txt_bytes = b"Control A.8.16: Log review conducted by SOC on 2026-09-01. No anomalies found."
    files = {"file": ("soc_audit_log.txt", io.BytesIO(txt_bytes), "text/plain")}
    res = client.post("/api/questionnaire/A.8.16/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    assert res.json()["content_type"] == "text/plain"

    csv_bytes = b"timestamp,event,severity\n2026-09-01,login_success,LOW\n"
    files_csv = {"file": ("audit_export.csv", io.BytesIO(csv_bytes), "text/csv")}
    res_csv = client.post("/api/questionnaire/A.8.16/evidence-file", files=files_csv, headers=AUTH_HEADER)
    assert res_csv.status_code == 200
    assert res_csv.json()["content_type"] == "text/csv"


# ---------------------------------------------------------------------------
# 5. Zero-Retention Text Extraction for PDF & Office Documents
# ---------------------------------------------------------------------------

def test_pdf_text_extraction_and_zero_retention():
    """PDF uploads extract text server-side and discard the binary."""
    pdf_bytes = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\nBT (Annual Security Policy 2026 Approved) Tj ET\n%%EOF"
    files = {"file": ("Information_Security_Policy.pdf", io.BytesIO(pdf_bytes), "application/pdf")}

    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "text_extracted"
    assert "Annual Security Policy 2026 Approved" in data["extracted_text"]
    file_id = data["file_id"]

    # Attempting to download the PDF binary must return 404 per zero-retention policy
    dl_res = client.get(f"/api/questionnaire/A.5.1/evidence-file/{file_id}", headers=AUTH_HEADER)
    assert dl_res.status_code == 404
    assert "Document binary was discarded per security policy" in dl_res.json()["detail"]


def test_docx_text_extraction_and_zero_retention():
    """DOCX uploads extract XML text content and discard the binary."""
    doc_buf = io.BytesIO()
    with zipfile.ZipFile(doc_buf, "w") as zf:
        zf.writestr(
            "word/document.xml",
            "<w:document><w:body><w:p><w:t>Access Control Matrix Verified for FY26</w:t></w:p></w:body></w:document>",
        )
    files = {
        "file": (
            "Access_Control_Policy.docx",
            io.BytesIO(doc_buf.getvalue()),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }

    res = client.post("/api/questionnaire/A.5.15/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "text_extracted"
    assert "Access Control Matrix Verified for FY26" in data["extracted_text"]


def test_xlsx_text_extraction_and_zero_retention():
    """XLSX uploads extract shared strings and discard the binary."""
    xl_buf = io.BytesIO()
    with zipfile.ZipFile(xl_buf, "w") as zf:
        zf.writestr("xl/workbook.xml", "<workbook/>")
        zf.writestr(
            "xl/sharedStrings.xml",
            "<sst><si><t>Asset Tag 1042</t></si><si><t>Critical Asset Server</t></si></sst>",
        )
    files = {
        "file": (
            "Asset_Inventory.xlsx",
            io.BytesIO(xl_buf.getvalue()),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }

    res = client.post("/api/questionnaire/A.5.9/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "text_extracted"
    assert "Asset Tag 1042" in data["extracted_text"]


def test_pptx_text_extraction_and_zero_retention():
    """PPTX uploads extract slide text and discard the binary."""
    ppt_buf = io.BytesIO()
    with zipfile.ZipFile(ppt_buf, "w") as zf:
        zf.writestr("ppt/presentation.xml", "<presentation/>")
        zf.writestr("ppt/slides/slide1.xml", "<p:sld><a:t>Quarterly Security Awareness Training</a:t></p:sld>")
    files = {
        "file": (
            "Awareness_Training.pptx",
            io.BytesIO(ppt_buf.getvalue()),
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    }

    res = client.post("/api/questionnaire/A.6.3/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["stored_as"] == "text_extracted"
    assert "Quarterly Security Awareness Training" in data["extracted_text"]


# ---------------------------------------------------------------------------
# 6. Questionnaire Answer Submission & Evidence Graph Anchoring
# ---------------------------------------------------------------------------

def test_submit_questionnaire_answer_with_attached_file():
    """Submit questionnaire answer linking uploaded file and anchors into EvidenceGraph."""
    # First, upload a text evidence file
    txt_bytes = b"Firewall rule check: port 22 blocked to public internet."
    files = {"file": ("firewall_check.txt", io.BytesIO(txt_bytes), "text/plain")}
    up_res = client.post("/api/questionnaire/A.8.20/evidence-file", files=files, headers=AUTH_HEADER)
    assert up_res.status_code == 200
    file_id = up_res.json()["file_id"]

    # Now submit the answer
    answer_payload = {
        "control_id": "A.8.20",
        "framework": "ISO27001:2022",
        "status": "COMPLIANT",
        "justification": "Network security controls and VPC firewall rules tested and verified.",
        "file_id": file_id,
    }
    ans_res = client.post("/api/questionnaire/A.8.20/answer", json=answer_payload, headers=AUTH_HEADER)
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["control_id"] == "A.8.20"
    assert ans_data["framework"] == "ISO27001:2022"
    assert ans_data["status"] == "COMPLIANT"
    assert ans_data["original_filename"] == "firewall_check.txt"

    # Verify anchor in EvidenceGraph
    matched_nodes = [
        n for n in ci_engine.evidence_graph.nodes.values()
        if n.control_id == "A.8.20" and n.resource_type == "questionnaire_response"
    ]
    assert len(matched_nodes) > 0
    ev_node = matched_nodes[-1]
    assert ev_node.framework == "ISO27001:2022"
    assert ev_node.raw_payload["file_id"] == file_id

    # Verify link in EvidenceGraph
    matched_links = [
        l for l in ci_engine.evidence_graph.links
        if l.control_id == "A.8.20" and l.source_node_id.startswith("ev-questionnaire_response-")
    ]
    assert len(matched_links) > 0
    ev_link = matched_links[-1]
    assert ev_link.framework == "ISO27001:2022"
    assert ev_link.status == "COMPLIANT"


def test_multi_framework_soc2_answer():
    """Submit SOC2 framework answer and verify segregation from ISO27001:2022."""
    soc2_payload = {
        "control_id": "CC6.1",
        "framework": "SOC2",
        "status": "COMPLIANT",
        "justification": "MFA enforced across Google Workspace identity federation.",
    }
    res = client.post("/api/questionnaire/CC6.1/answer", json=soc2_payload, headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()
    assert data["control_id"] == "CC6.1"
    assert data["framework"] == "SOC2"

    # Verify anchor in EvidenceGraph has framework SOC2
    matched_nodes = [
        n for n in ci_engine.evidence_graph.nodes.values()
        if n.control_id == "CC6.1" and n.framework == "SOC2"
    ]
    assert len(matched_nodes) > 0
    assert matched_nodes[-1].framework == "SOC2"


# ---------------------------------------------------------------------------
# 7. Questionnaire List & Summary Endpoints
# ---------------------------------------------------------------------------

def test_get_questionnaire_iso27001():
    """GET /api/questionnaire returns ISO27001:2022 controls and answered status."""
    res = client.get("/api/questionnaire?framework=ISO27001:2022")
    assert res.status_code == 200
    data = res.json()
    assert data["framework"] == "ISO27001:2022"
    assert data["total_controls"] == 93
    assert data["answered_controls"] >= 1  # From previous test

    # Verify structure of controls
    ctrl_a820 = next((c for c in data["controls"] if c["id"] == "A.8.20"), None)
    assert ctrl_a820 is not None
    assert ctrl_a820["answer"] is not None
    assert ctrl_a820["answer"]["status"] == "COMPLIANT"


def test_get_questionnaire_soc2():
    """GET /api/questionnaire returns SOC2 controls."""
    res = client.get("/api/questionnaire?framework=SOC2")
    assert res.status_code == 200
    data = res.json()
    assert data["framework"] == "SOC2"
    assert data["total_controls"] == 5
    assert data["answered_controls"] >= 1

    ctrl_cc61 = next((c for c in data["controls"] if c["id"] == "CC6.1"), None)
    assert ctrl_cc61 is not None
    assert ctrl_cc61["answer"] is not None
    assert ctrl_cc61["answer"]["status"] == "COMPLIANT"


def test_get_questionnaire_multilingual_pt_en_es():
    """GET /api/questionnaire returns localized titles, questions, evidence, and themes."""
    # 1. Portuguese (default)
    res_pt = client.get("/api/questionnaire?framework=ISO27001:2022&lang=pt")
    assert res_pt.status_code == 200
    data_pt = res_pt.json()
    assert data_pt["lang"] == "pt"
    assert len(data_pt["themes"]) == 4
    c_a51_pt = next(c for c in data_pt["controls"] if c["id"] == "A.5.1")
    assert "Políticas para segurança da informação" in c_a51_pt["name"]
    assert c_a51_pt["question"].startswith("A organização garante que")
    assert "Política Geral de Segurança" in c_a51_pt["recommended_evidence"]
    assert "translations" in c_a51_pt
    assert "pt" in c_a51_pt["translations"] and "en" in c_a51_pt["translations"]

    # 2. English
    res_en = client.get("/api/questionnaire?framework=ISO27001:2022&lang=en")
    assert res_en.status_code == 200
    data_en = res_en.json()
    assert data_en["lang"] == "en"
    c_a51_en = next(c for c in data_en["controls"] if c["id"] == "A.5.1")
    assert "Policies for information security" in c_a51_en["name"]
    assert c_a51_en["question"].startswith("Does the organization ensure that")
    assert "Information Security Policy" in c_a51_en["recommended_evidence"]

    # 3. Spanish
    res_es = client.get("/api/questionnaire?framework=ISO27001:2022&lang=es")
    assert res_es.status_code == 200
    data_es = res_es.json()
    assert data_es["lang"] == "es"
    c_a51_es = next(c for c in data_es["controls"] if c["id"] == "A.5.1")
    assert "Políticas para la seguridad de la información" in c_a51_es["name"]
    assert c_a51_es["question"].startswith("¿Garantiza la organización que")
    assert "Política General de Seguridad" in c_a51_es["recommended_evidence"]


def test_get_questionnaire_summary():
    """GET /api/questionnaire/summary computes accurate counts and completion percentage."""
    res = client.get("/api/questionnaire/summary?framework=ISO27001:2022")
    assert res.status_code == 200
    data = res.json()
    assert data["framework"] == "ISO27001:2022"
    assert data["total_controls"] == 93
    assert data["answered"] >= 1
    assert data["compliant"] >= 1
    assert data["completion_percentage"] > 0.0

    res_soc2 = client.get("/api/questionnaire/summary?framework=SOC2")
    assert res_soc2.status_code == 200
    data_soc2 = res_soc2.json()
    assert data_soc2["framework"] == "SOC2"
    assert data_soc2["total_controls"] == 5
    assert data_soc2["answered"] >= 1
    assert data_soc2["completion_percentage"] == 20.0  # 1 of 5


# ---------------------------------------------------------------------------
# 8. Additional Coverage and Edge Cases
# ---------------------------------------------------------------------------

def test_markdown_file_upload():
    """Markdown evidence files upload as text/markdown."""
    md_content = b"# Compliance Evidence\\n- All password rotation policies verified."
    files = {"file": ("evidence.md", io.BytesIO(md_content), "text/markdown")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 200
    assert res.json()["content_type"] == "text/markdown"


def test_reject_tar_archive():
    """TAR archive with ustar magic header at offset 257 is rejected."""
    tar_data = bytes(257) + b"ustar" + bytes(100)
    files = {"file": ("backup.tar", io.BytesIO(tar_data), "application/x-tar")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "TAR archive" in res.json()["detail"]


def test_reject_null_bytes_in_text():
    """Disallowed binary disguised as text with null byte is rejected."""
    bad_bytes = b"Hello world\x00hidden binary code"
    files = {"file": ("notes.txt", io.BytesIO(bad_bytes), "text/plain")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "containing NULL bytes" in res.json()["detail"]


def test_reject_invalid_utf8_text():
    """Non-UTF-8 bytes without known header are rejected."""
    bad_utf8 = bytes([0x80, 0x81, 0x82, 0x83, 0xff, 0xfe])
    files = {"file": ("random.txt", io.BytesIO(bad_utf8), "text/plain")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "not valid UTF-8" in res.json()["detail"]


def test_reject_corrupted_zip_archive():
    """Corrupted ZIP archive starting with PK\x03\x04 is rejected."""
    corrupt_zip = b"PK\x03\x04corrupted-archive-garbage-bytes"
    files = {"file": ("corrupt.docx", io.BytesIO(corrupt_zip), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    assert res.status_code == 400
    assert "Corrupted or invalid ZIP" in res.json()["detail"]


def test_download_nonexistent_and_wrong_control():
    """GET /api/questionnaire/{control_id}/evidence-file/{file_id} returns 404 for missing or mismatched control."""
    res_missing = client.get("/api/questionnaire/A.5.1/evidence-file/missing-uuid-1234", headers=AUTH_HEADER)
    assert res_missing.status_code == 404
    assert "Evidence file not found" in res_missing.json()["detail"]

    # Upload for A.5.1
    png_bytes = b"\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x06\\x00\\x00\\x00"
    files = {"file": ("test.png", io.BytesIO(png_bytes), "image/png")}
    up = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=AUTH_HEADER)
    file_id = up.json()["file_id"]

    # Request under A.5.2 (wrong control_id)
    res_wrong = client.get(f"/api/questionnaire/A.5.2/evidence-file/{file_id}", headers=AUTH_HEADER)
    assert res_wrong.status_code == 404


def test_custom_framework_and_non_compliant_na_statuses():
    """Test custom framework querying and non-compliant / N/A answer metrics."""
    # Submit non-compliant answer
    ans_nc = {
        "control_id": "PR.AC-1",
        "framework": "NIST_CSF",
        "status": "NON_COMPLIANT",
        "justification": "Identities are not strictly managed centrally.",
    }
    res_nc = client.post("/api/questionnaire/PR.AC-1/answer", json=ans_nc, headers=AUTH_HEADER)
    assert res_nc.status_code == 200

    # Submit not applicable answer
    ans_na = {
        "control_id": "PR.DS-5",
        "framework": "NIST_CSF",
        "status": "NOT_APPLICABLE",
        "justification": "Physical data transfer not utilized.",
    }
    res_na = client.post("/api/questionnaire/PR.DS-5/answer", json=ans_na, headers=AUTH_HEADER)
    assert res_na.status_code == 200

    # Query custom framework
    q_res = client.get("/api/questionnaire?framework=NIST_CSF")
    assert q_res.status_code == 200
    q_data = q_res.json()
    assert q_data["framework"] == "NIST_CSF"
    assert q_data["total_controls"] == 2
    assert q_data["answered_controls"] == 2

    # Query custom framework summary
    s_res = client.get("/api/questionnaire/summary?framework=NIST_CSF")
    assert s_res.status_code == 200
    s_data = s_res.json()
    assert s_data["framework"] == "NIST_CSF"
    assert s_data["total_controls"] == 2
    assert s_data["answered"] == 2
    assert s_data["compliant"] == 0
    assert s_data["non_compliant"] == 1
    assert s_data["not_applicable"] == 1
    assert s_data["completion_percentage"] == 100.0


def test_upload_with_workspace_id_token(monkeypatch):
    """Test upload authenticating via X-Goog-Id-Token with test signature verification bypass."""
    monkeypatch.setenv("PYTEST_SKIP_VERIFY_SIGNATURE", "true")
    valid_id_token = create_mock_id_token(email="lead-auditor@client.corp")
    id_header = {"X-Goog-Id-Token": valid_id_token}

    png_bytes = b"\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x06\\x00\\x00\\x00"
    files = {"file": ("token_test.png", io.BytesIO(png_bytes), "image/png")}
    res = client.post("/api/questionnaire/A.5.1/evidence-file", files=files, headers=id_header)
    assert res.status_code == 200
    assert res.json()["stored_as"] == "binary"

