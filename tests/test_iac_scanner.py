"""Unit tests for ISO/IEC 27001:2022 Control A.8.9 IaC Scanning."""

import pytest
from mcp_server_grc.tools.iac_scanner import scan_iac_configuration


def test_terraform_compliant():
    tf_content = """
    resource "google_compute_firewall" "internal_only" {
      name    = "allow-internal-traffic"
      network = "default"
      allow {
        protocol = "tcp"
        ports    = ["8080"]
      }
      source_ranges = ["10.0.0.0/8"]
    }
    """
    result = scan_iac_configuration("terraform", tf_content)
    assert result["status"] == "COMPLIANT"
    assert result["findings_count"] == 0


def test_terraform_violations_detected():
    tf_content = """
    resource "google_compute_firewall" "insecure_ssh" {
      name    = "allow-ssh"
      network = "default"
      allow {
        protocol = "tcp"
        ports    = ["22"]
      }
      cidr_blocks = ["0.0.0.0/0"]
    }

    resource "google_storage_bucket" "public_bucket" {
      name = "public-assets"
      acl  = "public-read"
    }

    resource "google_project_iam_binding" "owner_binding" {
      project = "my-project"
      role    = "roles/owner"
      members = ["user:admin@company.com"]
    }

    variable "api_key" {
      default = "AIzaSyDummyKeyForTestingPurposesOnly12345"
    }
    """
    result = scan_iac_configuration("terraform", tf_content)
    assert result["status"] == "NON_COMPLIANT"
    rule_ids = [f["rule_id"] for f in result["findings"]]
    assert "TF-SEC-001" in rule_ids  # Open CIDR
    assert "TF-SEC-002" in rule_ids  # Public ACL
    assert "TF-SEC-004" in rule_ids  # Primitive Owner role


def test_ansible_violations_detected():
    playbook = """
    - name: Configure Web Server
      hosts: all
      tasks:
        - name: Deploy insecure permissions
          file:
            path: /var/www/secret.txt
            mode: "0777"
        - name: Run SSH without host check
          command: ssh -o StrictHostKeyChecking=no user@remote
        - name: Plaintext token
          vars:
            password: "supersecretpassword123"
    """
    result = scan_iac_configuration("ansible", playbook)
    assert result["status"] == "NON_COMPLIANT"
    rule_ids = [f["rule_id"] for f in result["findings"]]
    assert "ANS-SEC-001" in rule_ids  # 0777 mode
    assert "ANS-SEC-002" in rule_ids  # StrictHostKeyChecking=no
    assert "ANS-SEC-003" in rule_ids  # Plaintext password


def test_unsupported_iac_type():
    result = scan_iac_configuration("puppet", "node default {}")
    assert result["status"] == "ERROR"
    assert "Unsupported iac_type" in result["error"]
