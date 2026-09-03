"""Control A.8.9: Configuration Management.

Performs static analysis on Infrastructure-as-Code (IaC) configurations
(Terraform and Ansible) to detect misconfigurations, insecure defaults,
and security drift before provisioning.
"""

import re
from typing import Any, Dict, List, Optional
import yaml


def scan_iac_configuration(
    iac_type: str,
    content: str,
    filename: Optional[str] = None,
) -> Dict[str, Any]:
    """Analyzes Terraform or Ansible code against ISO/IEC 27001:2022 Control A.8.9.

    Args:
        iac_type: 'terraform' or 'ansible'
        content: Raw code content (HCL string or YAML string)
        filename: Optional name of the file being audited

    Returns:
        Structured scan results with detected misconfigurations and compliance verdict.
    """
    iac_type = iac_type.lower()
    filename = filename or f"template.{'tf' if iac_type == 'terraform' else 'yml'}"
    findings: List[Dict[str, Any]] = []

    if iac_type in ["terraform", "tf"]:
        findings.extend(_scan_terraform(content, filename))
    elif iac_type in ["ansible", "yaml", "yml"]:
        findings.extend(_scan_ansible(content, filename))
    else:
        return {
            "status": "ERROR",
            "control": "ISO/IEC 27001:2022 A.8.9",
            "filename": filename,
            "error": f"Unsupported iac_type '{iac_type}'. Supported: 'terraform', 'ansible'.",
        }

    is_compliant = len(findings) == 0
    return {
        "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
        "control": "ISO/IEC 27001:2022 A.8.9",
        "iac_type": iac_type,
        "filename": filename,
        "findings_count": len(findings),
        "findings": findings,
        "remediation": (
            "IaC code passed all baseline security checks for Control A.8.9."
            if is_compliant
            else f"Remediate {len(findings)} detected misconfiguration(s) prior to pipeline provisioning."
        ),
    }


def _scan_terraform(content: str, filename: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    # Check 1: Open CIDR 0.0.0.0/0 on ingress rules
    cidr_match = re.search(r'cidr_blocks\s*=\s*\[.*"0\.0\.0\.0/0".*\]', content, re.IGNORECASE)
    if cidr_match:
        findings.append({
            "rule_id": "TF-SEC-001",
            "severity": "HIGH",
            "title": "Unrestricted Ingress CIDR Block",
            "description": "Security group or firewall rule permits ingress traffic from 0.0.0.0/0.",
            "recommendation": "Restrict CIDR blocks to authorized subnets or private corporate IP ranges."
        })

    # Check 2: Public access prevention or public bucket acl
    if re.search(r'acl\s*=\s*"public-read"', content, re.IGNORECASE):
        findings.append({
            "rule_id": "TF-SEC-002",
            "severity": "CRITICAL",
            "title": "Public Storage Bucket ACL",
            "description": "Storage bucket is configured with public-read ACL.",
            "recommendation": "Remove public-read ACL and enforce uniform bucket-level access."
        })

    # Check 3: Disabled encryption or missing KMS
    if re.search(r'enable_shielded_nodes\s*=\s*false', content, re.IGNORECASE):
        findings.append({
            "rule_id": "TF-SEC-003",
            "severity": "MEDIUM",
            "title": "Shielded GKE Nodes Disabled",
            "description": "GKE cluster has shielded nodes disabled.",
            "recommendation": "Set enable_shielded_nodes = true to protect node integrity."
        })

    # Check 4: Primitive IAM Owner/Editor in Terraform
    if re.search(r'role\s*=\s*"roles/(owner|editor)"', content, re.IGNORECASE):
        findings.append({
            "rule_id": "TF-SEC-004",
            "severity": "HIGH",
            "title": "Overprivileged IAM Primitive Role in IaC",
            "description": "Terraform defines primitive 'roles/owner' or 'roles/editor' bindings.",
            "recommendation": "Replace primitive roles with predefined least-privilege or custom roles."
        })

    # Check 5: Hardcoded secrets or tokens
    secret_pattern = re.search(r'(api_key|secret_key|private_key|password)\s*=\s*"(?!(\$\{|\bvar\.|\benv:))[^"]+"', content, re.IGNORECASE)
    if secret_pattern:
        findings.append({
            "rule_id": "TF-SEC-005",
            "severity": "CRITICAL",
            "title": "Hardcoded Secret in Terraform",
            "description": "Potential plaintext credential or secret detected in configuration.",
            "recommendation": "Use Google Secret Manager or KMS to inject secrets at runtime."
        })

    return findings


def _scan_ansible(content: str, filename: str) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    # Check 1: Insecure file permissions (0777)
    if re.search(r'mode:\s*(["\']?(0777|777|o\+w)["\']?)', content):
        findings.append({
            "rule_id": "ANS-SEC-001",
            "severity": "HIGH",
            "title": "World-Writable File Permissions",
            "description": "Ansible task creates or modifies a file with 0777 permissions.",
            "recommendation": "Set restrictive file permissions, e.g. 0640 or 0600."
        })

    # Check 2: Disabled StrictHostKeyChecking
    if re.search(r'StrictHostKeyChecking=no', content, re.IGNORECASE):
        findings.append({
            "rule_id": "ANS-SEC-002",
            "severity": "MEDIUM",
            "title": "SSH Host Key Verification Disabled",
            "description": "Ansible task disables StrictHostKeyChecking, exposing connections to MITM attacks.",
            "recommendation": "Enforce StrictHostKeyChecking=yes with known_hosts pre-seeding."
        })

    # Check 3: Plaintext secrets in playbooks
    if re.search(r'(password|token|secret):\s*["\'](?!(\{\{|\bvault_))[^"\']{6,}["\']', content, re.IGNORECASE):
        findings.append({
            "rule_id": "ANS-SEC-003",
            "severity": "CRITICAL",
            "title": "Unencrypted Secret in Ansible Playbook",
            "description": "Plaintext secret detected in task parameters.",
            "recommendation": "Encrypt sensitive variables with Ansible Vault or fetch from Secret Manager."
        })

    return findings
