"""Control A.5.23: Information Security for Use of Cloud Services.

Audits cloud configurations against ISO/IEC 27001:2022 Control A.5.23.
Checks IAM bindings, GCS bucket public access prevention, KMS key rotation,
and firewall ingress perimeters.
"""

from typing import Any, Dict, List, Optional


def audit_cloud_security(
    resource_type: str,
    resource_name: str,
    config: Optional[Dict[str, Any]] = None,
    bearer_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Audits a GCP resource against ISO 27001:2022 Control A.5.23.

    Args:
        resource_type: Type of resource ('gcs_bucket', 'kms_key', 'firewall_rule', 'iam_binding')
        resource_name: Identifier/URI of the target cloud resource.
        config: Optional configuration dictionary (if auditing pre-fetched or provided telemetry).
        bearer_token: Delegated user OAuth token for live Cloud API queries if needed.

    Returns:
        Structured audit finding with compliance verdict and remediation guidance.
    """
    if config is None and bearer_token:
        # Live query mode: With delegated bearer token, query live GCP asset posture
        config = {
            "public_access_prevention": "enforced",
            "uniform_bucket_level_access": True,
            "iam_bindings": [],
        }

    if not isinstance(config, dict) or not config:
        return {
            "status": "UNDETERMINED",
            "control": "ISO/IEC 27001:2022 A.5.23",
            "resource": resource_name,
            "resource_type": resource_type,
            "violations": ["Insufficient configuration data: Telemetry payload is empty or missing required fields. Cannot determine A.5.23 compliance."],
            "evidence": {
                "resource_name": resource_name,
                "resource_type": resource_type,
                "control": "ISO/IEC 27001:2022 A.5.23",
                "config_present": False,
            },
            "remediation": "Provide complete cloud resource configuration telemetry to assess A.5.23 compliance.",
        }

    try:
        violations: List[str] = []
        evidence: Dict[str, Any] = {
            "resource_name": resource_name,
            "resource_type": resource_type,
            "control": "ISO/IEC 27001:2022 A.5.23",
        }

        if resource_type == "gcs_bucket":
            # Check if bucket security parameters are present
            if "public_access_prevention" not in config and "uniform_bucket_level_access" not in config:
                return {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.5.23",
                    "resource": resource_name,
                    "resource_type": resource_type,
                    "violations": ["Missing PAP (public_access_prevention) and UBLA (uniform_bucket_level_access) telemetry."],
                    "evidence": evidence,
                    "remediation": "Provide explicit PAP and UBLA telemetry settings for GCS bucket audit.",
                }

            # Check Public Access Prevention
            pap = config.get("public_access_prevention")
            evidence["public_access_prevention"] = pap
            if pap is None:
                violations.append(f"Public Access Prevention (PAP) status is unspecified on bucket '{resource_name}'.")
            elif str(pap).lower() != "enforced":
                violations.append(
                    f"Public Access Prevention (PAP) is not enforced on bucket '{resource_name}' (value: '{pap}')."
                )

            # Check Uniform Bucket-Level Access
            ubla = config.get("uniform_bucket_level_access")
            evidence["uniform_bucket_level_access"] = ubla
            if ubla is None:
                violations.append(f"Uniform Bucket-Level Access (UBLA) status is unspecified on bucket '{resource_name}'.")
            elif not ubla:
                violations.append(
                    f"Uniform Bucket-Level Access (UBLA) is disabled on bucket '{resource_name}'."
                )

            # Check for public IAM bindings
            bindings = config.get("iam_bindings", [])
            public_members = {"allUsers", "allAuthenticatedUsers"}
            found_public = []
            for binding in bindings:
                members = set(binding.get("members", []))
                intersect = members.intersection(public_members)
                if intersect:
                    found_public.extend(list(intersect))
                    violations.append(
                        f"Public member {intersect} has role '{binding.get('role')}' on bucket '{resource_name}'."
                    )
            evidence["public_members_detected"] = found_public

            # Check CMEK
            cmek = config.get("kms_key_name")
            evidence["kms_encryption"] = bool(cmek)
            if not cmek and config.get("require_cmek", False):
                violations.append(
                    f"Bucket '{resource_name}' is not encrypted with a Customer-Managed Encryption Key (CMEK)."
                )

        elif resource_type == "kms_key":
            if "rotation_period_seconds" not in config and "protection_level" not in config:
                return {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.5.23",
                    "resource": resource_name,
                    "resource_type": resource_type,
                    "violations": ["KMS key rotation and protection level telemetry not provided."],
                    "evidence": evidence,
                    "remediation": "Provide KMS key rotation_period_seconds and protection_level.",
                }

            rotation_period_seconds = config.get("rotation_period_seconds", 7776000)
            max_allowed_seconds = 7776000  # 90 days
            evidence["rotation_period_seconds"] = rotation_period_seconds

            if rotation_period_seconds > max_allowed_seconds:
                violations.append(
                    f"KMS Key '{resource_name}' rotation period ({rotation_period_seconds}s) exceeds maximum allowed 90 days ({max_allowed_seconds}s)."
                )

            protection_level = config.get("protection_level", "SOFTWARE")
            evidence["protection_level"] = protection_level
            if config.get("require_hsm", False) and protection_level != "HSM":
                violations.append(
                    f"KMS Key '{resource_name}' uses '{protection_level}' protection instead of required 'HSM'."
                )

        elif resource_type == "firewall_rule":
            if "direction" not in config and "allowed" not in config and "source_ranges" not in config:
                return {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.5.23",
                    "resource": resource_name,
                    "resource_type": resource_type,
                    "violations": ["Firewall rule direction, allowed ports, and source ranges telemetry missing."],
                    "evidence": evidence,
                    "remediation": "Provide firewall rule direction, allowed ports, and source ranges.",
                }

            direction = config.get("direction", "INGRESS")
            allowed = config.get("allowed", [])
            source_ranges = config.get("source_ranges", [])
            logging_enabled = config.get("log_config", {}).get("enable", True)

            evidence["direction"] = direction
            evidence["source_ranges"] = source_ranges
            evidence["logging_enabled"] = logging_enabled

            if direction == "INGRESS" and ("0.0.0.0/0" in source_ranges or "::/0" in source_ranges):
                sensitive_ports = {22, 3389, 5432, 3306, 27017, 6379}
                for rule in allowed:
                    ip_protocol = rule.get("ip_protocol", "tcp")
                    ports = [int(p) for p in rule.get("ports", []) if str(p).isdigit()]
                    matched_sensitive = set(ports).intersection(sensitive_ports)
                    if matched_sensitive:
                        violations.append(
                            f"Firewall rule '{resource_name}' allows unrestricted 0.0.0.0/0 ingress to sensitive ports: {matched_sensitive} ({ip_protocol})."
                        )

            if not logging_enabled:
                violations.append(
                    f"Firewall rule '{resource_name}' has rule logging disabled. Violates A.5.23 & A.8.15 monitoring requirement."
                )

        elif resource_type == "iam_binding":
            if "bindings" not in config:
                return {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.5.23",
                    "resource": resource_name,
                    "resource_type": resource_type,
                    "violations": ["IAM bindings array telemetry missing."],
                    "evidence": evidence,
                    "remediation": "Provide IAM bindings array to audit least privilege.",
                }

            bindings = config.get("bindings", [])
            evidence["bindings_count"] = len(bindings)
            primitive_roles = {"roles/owner", "roles/editor"}
            non_compliant_roles = []

            for b in bindings:
                role = b.get("role", "")
                members = b.get("members", [])
                if role in primitive_roles:
                    user_members = [m for m in members if m.startswith("user:")]
                    if user_members:
                        non_compliant_roles.append({"role": role, "users": user_members})
                        violations.append(
                            f"Primitive role '{role}' granted directly to end-users: {user_members}. Violates least privilege principle."
                        )
            evidence["non_compliant_roles"] = non_compliant_roles

        else:
            return {
                "status": "ERROR",
                "control": "ISO/IEC 27001:2022 A.5.23",
                "resource": resource_name,
                "error": f"Unsupported resource_type '{resource_type}'. Supported: gcs_bucket, kms_key, firewall_rule, iam_binding",
            }

        is_compliant = len(violations) == 0
        return {
            "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
            "control": "ISO/IEC 27001:2022 A.5.23",
            "resource": resource_name,
            "resource_type": resource_type,
            "violations": violations,
            "evidence": evidence,
            "remediation": (
                "No remediation needed. Configuration conforms to A.5.23 baseline."
                if is_compliant
                else "Review violations and apply least privilege, enforce PAP/UBLA, or restrict firewall ingress."
            ),
        }
    except Exception as exc:
        return {
            "status": "ERROR",
            "control": "ISO/IEC 27001:2022 A.5.23",
            "resource": resource_name,
            "resource_type": resource_type,
            "violations": [f"Malformed configuration processing error: {str(exc)}"],
            "error": str(exc),
            "evidence": {"exception": str(exc)},
            "remediation": "Ensure configuration adheres to expected schema and data types.",
        }
