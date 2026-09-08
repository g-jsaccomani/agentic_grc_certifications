import json
import subprocess
from mcp_server_grc.cloud_inspector import (
    inspect_cloud_storage_bucket,
    inspect_cloud_kms_key,
    inspect_project_iam_policy,
)
from mcp_server_grc.tools.cloud_security import audit_cloud_security

token = subprocess.check_output(["gcloud", "auth", "application-default", "print-access-token"]).decode().strip()

results = []

# 1. Buckets
buckets = [
    ("poc-bucket-payments-sec-8fa913", "fnlab-sec-mgmt-8fa913", True),
    ("poc-bucket-analytics-ai-8fa913", "fnlab-ai-data-8fa913", True),
    ("poc-bucket-logs-core-1cab11", "aispr-core-1cab11", True),
    ("poc-bucket-app-apps-8fa913", "fnlab-apps-8fa913", False),
    ("poc-bucket-backup-apps-8fa913", "fnlab-apps-8fa913", False),
    ("poc-bucket-reports-ai-8fa913", "fnlab-ai-data-8fa913", False),
    ("poc-bucket-staging-ai-8fa913", "fnlab-ai-data-8fa913", False),
    ("poc-bucket-app-sec-8fa913", "fnlab-sec-mgmt-8fa913", False),
    ("poc-bucket-backup-core-1cab11", "aispr-core-1cab11", False),
    ("poc-bucket-staging-core-1cab11", "aispr-core-1cab11", False),
]

print("=== 1. GCS BUCKETS AUDIT (ISO 27001 Control A.5.23) ===")
for bname, proj, expected_comp in buckets:
    res = inspect_cloud_storage_bucket(bname, project_id=proj, bearer_token=token)
    comp = res["compliance"]["status"]
    violations = res["compliance"]["violations"]
    results.append(("GCS", bname, comp, expected_comp))
    print(f"[{comp:13}] {bname:<35} | Proj: {proj:<20} | Violations: {violations}")

# 2. KMS Keys
kms_keys = [
    ("poc-key-payments-hsm", "fnlab-sec-mgmt-8fa913", "poc-keyring-sec", True),
    ("poc-key-database-hsm", "fnlab-sec-mgmt-8fa913", "poc-keyring-sec", True),
    ("poc-key-audit-software", "fnlab-sec-mgmt-8fa913", "poc-keyring-sec", False),
    ("poc-key-app-data", "fnlab-apps-8fa913", "poc-keyring-apps", False),
    ("poc-key-backup-long", "fnlab-apps-8fa913", "poc-keyring-apps", False),
    ("poc-key-tokens-stale", "fnlab-apps-8fa913", "poc-keyring-apps", False),
]

print("\n=== 2. KMS KEYS AUDIT (ISO 27001 Control A.8.24) ===")
for kname, proj, kr, expected_comp in kms_keys:
    res = inspect_cloud_kms_key(kname, project_id=proj, location="us-central1", keyring_name=kr, bearer_token=token)
    comp = res["compliance"]["status"]
    violations = res["compliance"]["violations"]
    results.append(("KMS", kname, comp, expected_comp))
    print(f"[{comp:13}] {kname:<25} | Keyring: {kr:<18} | Proj: {proj:<20} | Violations: {violations}")

# 3. Firewalls
fws = [
    ("poc-fw-internal-mgmt", "fnlab-sec-mgmt-8fa913", True, {"direction": "INGRESS", "allowed": [{"ip_protocol": "tcp", "ports": [8080]}], "source_ranges": ["10.10.0.0/16"], "log_config": {"enable": True}}),
    ("poc-fw-ai-worker-sync", "fnlab-ai-data-8fa913", True, {"direction": "INGRESS", "allowed": [{"ip_protocol": "tcp", "ports": [9090]}], "source_ranges": ["10.30.0.0/16"], "log_config": {"enable": True}}),
    ("poc-fw-open-ssh-demo", "fnlab-apps-8fa913", False, {"direction": "INGRESS", "allowed": [{"ip_protocol": "tcp", "ports": [22]}], "source_ranges": ["0.0.0.0/0"], "log_config": {"enable": False}}),
    ("poc-fw-open-rdp-demo", "aispr-core-1cab11", False, {"direction": "INGRESS", "allowed": [{"ip_protocol": "tcp", "ports": [3389]}], "source_ranges": ["0.0.0.0/0"], "log_config": {"enable": False}}),
    ("poc-fw-db-nologging", "fnlab-apps-8fa913", False, {"direction": "INGRESS", "allowed": [{"ip_protocol": "tcp", "ports": [5432]}], "source_ranges": ["10.20.0.0/16"], "log_config": {"enable": False}}),
    ("poc-fw-analytics-wide", "fnlab-ai-data-8fa913", False, {"direction": "INGRESS", "allowed": [{"ip_protocol": "tcp", "ports": [8000]}], "source_ranges": ["0.0.0.0/0"], "log_config": {"enable": False}}),
]

print("\n=== 3. FIREWALL RULES AUDIT (ISO 27001 Controls A.5.23 & A.8.20) ===")
for fw_name, proj, expected_comp, cfg in fws:
    res = audit_cloud_security("firewall_rule", fw_name, config=cfg)
    comp = res["status"]
    violations = res["violations"]
    results.append(("FW", fw_name, comp, expected_comp))
    print(f"[{comp:13}] {fw_name:<25} | Proj: {proj:<20} | Violations: {violations}")

# 4. IAM Bindings
iam_checks = [
    ("poc-sa-reader", "roles/storage.objectViewer", "fnlab-apps-8fa913", True, [{"role": "roles/storage.objectViewer", "members": ["serviceAccount:poc-sa-reader@fnlab-apps-8fa913.iam.gserviceaccount.com"]}]),
    ("poc-sa-auditor", "roles/viewer", "aispr-core-1cab11", True, [{"role": "roles/viewer", "members": ["serviceAccount:poc-sa-auditor@aispr-core-1cab11.iam.gserviceaccount.com"]}]),
    ("user:admin", "roles/owner", "fnlab-apps-8fa913", False, [{"role": "roles/owner", "members": ["user:admin@jsaccomani.altostrat.com"]}]),
    ("user:admin", "roles/owner", "fnlab-ai-data-8fa913", False, [{"role": "roles/owner", "members": ["user:admin@jsaccomani.altostrat.com"]}]),
    ("user:admin", "roles/editor", "fnlab-sec-mgmt-8fa913", False, [{"role": "roles/editor", "members": ["user:admin@jsaccomani.altostrat.com"]}]),
    ("user:admin", "roles/owner", "aispr-core-1cab11", False, [{"role": "roles/owner", "members": ["user:admin@jsaccomani.altostrat.com"]}]),
]

print("\n=== 4. IAM BINDINGS AUDIT (ISO 27001 Control A.5.15 Least Privilege) ===")
for target, role, proj, expected_comp, bindings in iam_checks:
    res = audit_cloud_security("iam_binding", f"{target}:{role}", config={"bindings": bindings})
    comp = res["status"]
    violations = res["violations"]
    results.append(("IAM", f"{target}:{role}", comp, expected_comp))
    print(f"[{comp:13}] {target}:{role:<28} | Proj: {proj:<20} | Violations: {violations}")

total = len(results)
compliant_count = sum(1 for r in results if r[2] == "COMPLIANT")
non_compliant_count = sum(1 for r in results if r[2] == "NON_COMPLIANT")

print("\n" + "="*70)
print(f"TOTAL RESOURCES AUDITED: {total}")
print(f"COMPLIANT:     {compliant_count:>2} ({compliant_count/total*100:5.1f}%) [Target ~30%]")
print(f"NON-COMPLIANT: {non_compliant_count:>2} ({non_compliant_count/total*100:5.1f}%) [Target ~70%]")
print("="*70)
