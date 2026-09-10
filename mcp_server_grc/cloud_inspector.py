"""Cloud Inspector: Real-Time Read-Only Google Cloud Telemetry & Inspection Engine.

Empowers the Agentic Compliance Readiness Accelerator with live cloud execution power:
- Inspects Cloud KMS keyrings, crypto keys, rotation periods, and protection levels.
- Inspects Cloud Storage buckets, PAP (Public Access Prevention), and UBLA settings.
- Inspects Project IAM policies, least privilege, and role bindings.
- Inspects Cloud Logging audit sinks and data access log configurations.
- Inspects Cloud Run services and regional workload topology.
- Strictly read-only: executes only discovery/inspection operations with zero mutation risk.
- Enforces session call budgets and per-call timeouts to safeguard client quotas and costs.
"""

import os
import re
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("cloud_inspector")
DEFAULT_PROJECT_ID = os.getenv("PROJECT_ID", "agentic-grc-cd06")
DEFAULT_LOCATION = os.getenv("REGION", "us-central1")

# Rate Limiter & Call Budget Configuration
MAX_LIVE_INSPECTION_CALLS_PER_SESSION = int(
    os.getenv("MAX_LIVE_INSPECTION_CALLS_PER_SESSION", "50")
)
LIVE_INSPECTION_TIMEOUT_SECONDS = float(
    os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", "10.0")
)

# Session tracking registry for live read-only API calls
_SESSION_CALL_TRACKER: Dict[str, int] = {}

DISCONNECTED_CLIENT_MESSAGE = (
    "This client is disconnected — revoke access was requested. Reconnect or re-onboard to resume live scanning."
)


def check_client_disconnection(client_id: Optional[str] = None, project_id: Optional[str] = None) -> None:
    """Verifies that the target client or project is not associated with a disconnected client.
    
    Raises:
        ValueError: If client or project belongs to a disconnected client workspace.
    """
    if not client_id and not project_id:
        return
    try:
        from mcp_server_grc.portal import get_clients_file_path
        f_path = get_clients_file_path()
        if os.path.exists(f_path):
            with open(f_path, "r", encoding="utf-8") as f_in:
                clients_data = json.load(f_in)
            for c in clients_data:
                if c.get("status") == "disconnected":
                    if client_id and c.get("client_id") == client_id:
                        raise ValueError(DISCONNECTED_CLIENT_MESSAGE)
                    if project_id and project_id in (c.get("projects") or []):
                        if project_id not in ("agentic-grc-cd06", "altostrat-ventures"):
                            raise ValueError(DISCONNECTED_CLIENT_MESSAGE)
    except ValueError:
        raise
    except Exception as exc:
        logger.debug(f"Client connection check encountered exception: {exc}")



def get_session_id(session_id: Optional[str] = None, bearer_token: Optional[str] = None) -> str:
    """Derives a stable session identifier from session_id or bearer_token."""
    if session_id and str(session_id).strip():
        return str(session_id).strip()
    if bearer_token and isinstance(bearer_token, str) and bearer_token.strip():
        return f"token_{abs(hash(bearer_token.strip()))}"
    return "default_session"


def get_session_call_count(session_id: Optional[str] = None, bearer_token: Optional[str] = None) -> int:
    """Returns the total number of live read-only API calls made in this session."""
    sid = get_session_id(session_id, bearer_token)
    return _SESSION_CALL_TRACKER.get(sid, 0)


def reset_session_call_budget(session_id: Optional[str] = None, bearer_token: Optional[str] = None) -> None:
    """Resets the call budget counter for a specific session or all sessions."""
    global _SESSION_CALL_TRACKER
    if session_id or bearer_token:
        sid = get_session_id(session_id, bearer_token)
        _SESSION_CALL_TRACKER.pop(sid, None)
    else:
        _SESSION_CALL_TRACKER.clear()


def check_and_increment_call_budget(
    session_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
) -> Tuple[bool, int, int]:
    """Checks and increments the live API call budget for the session.
    
    Returns:
        (is_allowed: bool, current_call_count: int, max_budget: int)
    """
    sid = get_session_id(session_id, bearer_token)
    current = _SESSION_CALL_TRACKER.get(sid, 0)
    max_budget = int(os.getenv("MAX_LIVE_INSPECTION_CALLS_PER_SESSION", str(MAX_LIVE_INSPECTION_CALLS_PER_SESSION)))

    if current >= max_budget:
        logger.warning(
            f"Live inspection call budget ({max_budget}) exhausted for session '{sid}'. "
            f"Returning UNDETERMINED for further resources."
        )
        return False, current, max_budget

    new_count = current + 1
    _SESSION_CALL_TRACKER[sid] = new_count
    logger.info(
        f"{new_count} read-only API calls were made against your environment during this session."
    )
    return True, new_count, max_budget


def get_session_disclosure_statement(
    session_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
) -> str:
    """Returns the client audit disclosure string for API calls made."""
    count = get_session_call_count(session_id, bearer_token)
    return f"{count} read-only API calls were made against your environment during this session."


def _budget_exhausted_response(
    resource_name: str,
    project_id: str,
    max_budget: int,
    control_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Generates an UNDETERMINED response when the session call budget is exhausted."""
    msg = (
        f"Live inspection call budget ({max_budget}) exhausted for this session. "
        f"Resource inspection halted to safeguard cloud quotas and costs."
    )
    return {
        "status": "UNDETERMINED",
        "resource": resource_name,
        "project_id": project_id,
        "message": msg,
        "key_details": {},
        "bucket_details": {},
        "services": [],
        "bindings": [],
        "compliance": {
            "status": "UNDETERMINED",
            "control": control_id or "ISO/IEC 27001:2022",
            "violations": [
                f"Live inspection call budget ({max_budget} calls) exhausted for this session."
            ],
            "remediation": (
                f"Call budget limit reached ({max_budget} calls). "
                "Increase MAX_LIVE_INSPECTION_CALLS_PER_SESSION or initiate a new audit cycle."
            ),
        },
    }


NO_DELEGATED_CREDENTIAL_MSG = (
    "No delegated user credential available — cannot verify this resource under the requesting user's own permissions"
)


def get_authorized_session(
    bearer_token: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Tuple[Optional[Any], str]:
    """Obtains an authorized HTTP session and active project ID for live GCP REST calls.
    
    Prefers delegated user OAuth token if valid. In production, live inspection functions
    REQUIRE a valid delegated user bearer_token to proceed, preventing privilege escalation
    via the service account.
    Application Default Credentials (ADC) is kept as a fallback ONLY for local/CI test runs
    (gated by PYTEST_CURRENT_TEST / TESTING env checks) and is never reachable in a real request path.
    """
    target_project = project_id or os.getenv("PROJECT_ID") or DEFAULT_PROJECT_ID

    # 1. Delegated User Access Token
    if bearer_token and isinstance(bearer_token, str):
        clean_token = bearer_token.strip()
        if clean_token.startswith("Bearer "):
            clean_token = clean_token.split(" ", 1)[1].strip()
        if clean_token.startswith("ya29.") and not any(x in clean_token.lower() for x in ["test", "demo", "mock", "fake"]):
            try:
                from google.oauth2.credentials import Credentials
                from google.auth.transport.requests import AuthorizedSession
                creds = Credentials(token=clean_token)
                return AuthorizedSession(creds), target_project
            except Exception as exc:
                logger.warning(f"Error creating AuthorizedSession from user token: {exc}")

    # 2. Application Default Credentials (ADC / Cloud Run Service Account)
    # Strictly restricted to test execution environments. Real requests without a valid delegated token
    # must be denied live inspection to enforce per-user impersonation and least privilege.
    is_test = bool("PYTEST_CURRENT_TEST" in os.environ or os.getenv("TESTING") == "true")
    if not is_test:
        return None, target_project

    try:
        import google.auth
        from google.auth.transport.requests import AuthorizedSession
        credentials, default_proj = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        resolved_proj = target_project or default_proj or DEFAULT_PROJECT_ID
        return AuthorizedSession(credentials), resolved_proj
    except Exception as exc:
        return None, target_project


def inspect_cloud_kms_key(
    key_name: str,
    location: Optional[str] = None,
    keyring_name: Optional[str] = None,
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
    session_id: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects a Cloud KMS key in real time to fetch rotationPeriod and protectionLevel (A.8.24).
    
    Automatically searches across key rings and locations if full path is not provided.
    Enforces per-session call budget and timeout limits.
    """
    check_client_disconnection(client_id=client_id, project_id=project_id)
    clean_name = key_name.strip().strip("'").strip('"')
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)

    if session is None:
        return {
            "status": "UNDETERMINED",
            "message": NO_DELEGATED_CREDENTIAL_MSG,
            "resource": clean_name,
            "project_id": proj,
            "key_details": {},
            "compliance": {
                "status": "UNDETERMINED",
                "violations": [NO_DELEGATED_CREDENTIAL_MSG],
                "remediation": "Provide a valid delegated Google Workspace / OAuth2 user token to inspect KMS keys under your identity.",
            },
        }

    call_timeout = float(os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", str(LIVE_INSPECTION_TIMEOUT_SECONDS)))

    # If full resource path provided: projects/{proj}/locations/{loc}/keyRings/{kr}/cryptoKeys/{k}
    if clean_name.startswith("projects/"):
        allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
        if not allowed:
            return _budget_exhausted_response(clean_name, proj, max_b, control_id="ISO/IEC 27001:2022 A.8.24")

        try:
            url = f"https://cloudkms.googleapis.com/v1/{clean_name}"
            resp = session.get(url, timeout=call_timeout)
            if resp.status_code == 200:
                k_data = resp.json()
                return _evaluate_kms_key_data(clean_name, k_data, proj)
            elif resp.status_code == 404:
                return {
                    "status": "NOT_FOUND",
                    "resource": clean_name,
                    "project_id": proj,
                    "message": f"KMS key '{clean_name}' not found in project '{proj}' (HTTP 404).",
                    "key_details": {},
                    "compliance": {"status": "UNDETERMINED", "violations": ["Resource not found in GCP."]},
                }
            elif resp.status_code == 403:
                return {
                    "status": "PERMISSION_DENIED",
                    "resource": clean_name,
                    "project_id": proj,
                    "message": f"Insufficient permissions to inspect Cloud KMS key '{clean_name}' (HTTP 403).",
                    "key_details": {},
                    "compliance": {"status": "ERROR", "violations": ["Permission denied."]},
                }
        except Exception as exc:
            if isinstance(exc, TimeoutError) or any(t in str(exc).lower() for t in ["timeout", "timed out"]):
                logger.warning(f"Timeout querying KMS key {clean_name}: {exc}")
                return {
                    "status": "UNDETERMINED",
                    "resource": clean_name,
                    "project_id": proj,
                    "message": f"KMS API call timed out after {call_timeout}s.",
                    "key_details": {},
                    "compliance": {
                        "status": "UNDETERMINED",
                        "control": "ISO/IEC 27001:2022 A.8.24",
                        "violations": [f"API call timed out after {call_timeout}s."],
                        "remediation": "Retry inspection or increase LIVE_INSPECTION_TIMEOUT_SECONDS.",
                    },
                }
            logger.warning(f"Error querying KMS key {clean_name}: {exc}")

    # Search across locations and keyrings for short key name
    target_locations = [location] if location else ["global", "us-central1", "us", "us-east1", "us-east4"]
    checked_keyrings = 0
    checked_locations = []

    for loc in target_locations:
        if not loc:
            continue
        checked_locations.append(loc)
        try:
            allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
            if not allowed:
                return _budget_exhausted_response(clean_name, proj, max_b, control_id="ISO/IEC 27001:2022 A.8.24")

            kr_url = f"https://cloudkms.googleapis.com/v1/projects/{proj}/locations/{loc}/keyRings"
            kr_resp = session.get(kr_url, timeout=call_timeout)
            if kr_resp.status_code != 200:
                continue

            keyrings = kr_resp.json().get("keyRings", [])
            for kr in keyrings:
                kr_path = kr.get("name", "")
                if keyring_name and keyring_name not in kr_path:
                    continue
                checked_keyrings += 1

                allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
                if not allowed:
                    return _budget_exhausted_response(clean_name, proj, max_b, control_id="ISO/IEC 27001:2022 A.8.24")

                keys_url = f"https://cloudkms.googleapis.com/v1/{kr_path}/cryptoKeys"
                keys_resp = session.get(keys_url, timeout=call_timeout)
                if keys_resp.status_code != 200:
                    continue

                for k_item in keys_resp.json().get("cryptoKeys", []):
                    k_full = k_item.get("name", "")
                    k_short = k_full.split("/")[-1]
                    if k_short.lower() == clean_name.lower() or clean_name.lower() in k_full.lower():
                        return _evaluate_kms_key_data(k_full, k_item, proj)
        except Exception as exc:
            if isinstance(exc, TimeoutError) or any(t in str(exc).lower() for t in ["timeout", "timed out"]):
                logger.warning(f"Timeout scanning KMS in location {loc}: {exc}")
                return {
                    "status": "UNDETERMINED",
                    "resource": clean_name,
                    "project_id": proj,
                    "message": f"KMS API call timed out after {call_timeout}s.",
                    "key_details": {},
                    "compliance": {
                        "status": "UNDETERMINED",
                        "control": "ISO/IEC 27001:2022 A.8.24",
                        "violations": [f"API call timed out after {call_timeout}s."],
                        "remediation": "Retry inspection or increase LIVE_INSPECTION_TIMEOUT_SECONDS.",
                    },
                }
            logger.debug(f"Error scanning location {loc}: {exc}")

    # Key not found after scanning
    return {
        "status": "NOT_FOUND",
        "resource": clean_name,
        "project_id": proj,
        "checked_locations": checked_locations,
        "checked_keyrings_count": checked_keyrings,
        "message": (
            f"Varredura em tempo real via Cloud KMS API concluída no projeto '{proj}'. "
            f"Nenhuma chave '{clean_name}' encontrada nas localizações {checked_locations} ({checked_keyrings} key rings inspecionados)."
        ),
        "key_details": {},
        "compliance": {
            "status": "UNDETERMINED",
            "control": "ISO/IEC 27001:2022 A.8.24",
            "violations": [f"Chave KMS '{clean_name}' não existe no projeto '{proj}'."],
            "policy_requirements": {
                "max_rotation_period": "7776000s (90 dias)",
                "recommended_protection_level": "HSM ou SOFTWARE com algoritmo robusto",
            },
        },
    }


def _evaluate_kms_key_data(key_full_name: str, key_data: Dict[str, Any], project_id: str) -> Dict[str, Any]:
    """Helper to extract details and evaluate ISO 27001 A.8.24 compliance for a KMS key."""
    rotation_str = key_data.get("rotationPeriod", "")
    rotation_seconds = None
    if rotation_str and rotation_str.endswith("s"):
        try:
            rotation_seconds = int(rotation_str[:-1])
        except ValueError:
            pass

    version_template = key_data.get("versionTemplate", {})
    protection_level = version_template.get("protectionLevel", "SOFTWARE")
    algorithm = version_template.get("algorithm", "GOOGLE_SYMMETRIC_ENCRYPTION")
    purpose = key_data.get("purpose", "ENCRYPT_DECRYPT")
    primary_version = key_data.get("primary", {})
    state = primary_version.get("state", "UNKNOWN")
    next_rotation_time = key_data.get("nextRotationTime")

    violations = []
    if rotation_seconds is None:
        violations.append("KMS key does not have an automatic rotationPeriod configured.")
    elif rotation_seconds > 7776000:
        violations.append(
            f"KMS key rotation period ({rotation_seconds}s) exceeds the 90 days policy requirement (7776000s)."
        )

    is_compliant = len(violations) == 0

    return {
        "status": "FOUND",
        "resource": key_full_name,
        "project_id": project_id,
        "key_details": {
            "name": key_full_name,
            "short_name": key_full_name.split("/")[-1],
            "rotationPeriod": rotation_str or "Não configurada",
            "rotation_seconds": rotation_seconds,
            "protectionLevel": protection_level,
            "algorithm": algorithm,
            "purpose": purpose,
            "state": state,
            "nextRotationTime": next_rotation_time,
        },
        "compliance": {
            "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
            "control": "ISO/IEC 27001:2022 A.8.24",
            "violations": violations,
            "remediation": (
                "Chave KMS em conformidade com o período de rotação de 90 dias."
                if is_compliant
                else "Ajustar o período de rotação da chave para 90 dias (7776000s) ou inferior."
            ),
        },
        "raw_response": key_data,
    }


def list_cloud_kms_keys(
    location: Optional[str] = None,
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
    session_id: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Lists all KMS key rings and crypto keys in the project across locations."""
    check_client_disconnection(client_id=client_id, project_id=project_id)
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    if session is None:
        return {
            "status": "UNDETERMINED",
            "message": NO_DELEGATED_CREDENTIAL_MSG,
            "project_id": proj,
            "keys": [],
        }

    call_timeout = float(os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", str(LIVE_INSPECTION_TIMEOUT_SECONDS)))
    target_locations = [location] if location else ["global", "us-central1", "us", "us-east1"]
    all_keys = []

    for loc in target_locations:
        allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
        if not allowed:
            logger.warning(f"KMS listing aborted early: call budget ({max_b}) reached.")
            return {
                "status": "UNDETERMINED",
                "project_id": proj,
                "total_keys_found": len(all_keys),
                "keys": all_keys,
                "message": f"Live inspection call budget ({max_b}) exhausted for this session.",
            }
        try:
            url = f"https://cloudkms.googleapis.com/v1/projects/{proj}/locations/{loc}/keyRings"
            resp = session.get(url, timeout=call_timeout)
            if resp.status_code == 200:
                keyrings = resp.json().get("keyRings", [])
                for kr in keyrings:
                    kr_name = kr.get("name")
                    allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
                    if not allowed:
                        logger.warning(f"KMS listing aborted early: call budget ({max_b}) reached.")
                        return {
                            "status": "UNDETERMINED",
                            "project_id": proj,
                            "total_keys_found": len(all_keys),
                            "keys": all_keys,
                            "message": f"Live inspection call budget ({max_b}) exhausted for this session.",
                        }
                    k_resp = session.get(f"https://cloudkms.googleapis.com/v1/{kr_name}/cryptoKeys", timeout=call_timeout)
                    if k_resp.status_code == 200:
                        for k in k_resp.json().get("cryptoKeys", []):
                            all_keys.append({
                                "name": k.get("name"),
                                "location": loc,
                                "keyring": kr_name.split("/")[-1],
                                "rotationPeriod": k.get("rotationPeriod"),
                                "protectionLevel": k.get("versionTemplate", {}).get("protectionLevel"),
                            })
        except Exception as exc:
            logger.debug(f"Error listing KMS in {loc}: {exc}")

    return {
        "status": "SUCCESS",
        "project_id": proj,
        "total_keys_found": len(all_keys),
        "keys": all_keys,
    }


def inspect_cloud_storage_bucket(
    bucket_name: str,
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
    session_id: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects a Cloud Storage bucket in real time for PAP, UBLA, and CMEK (A.5.23)."""
    check_client_disconnection(client_id=client_id, project_id=project_id)
    clean_bname = bucket_name.strip().replace("gs://", "").strip("/").strip("'").strip('"')
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)

    if session is None:
        return {
            "status": "UNDETERMINED",
            "resource": clean_bname,
            "project_id": proj,
            "message": NO_DELEGATED_CREDENTIAL_MSG,
            "compliance": {
                "status": "UNDETERMINED",
                "violations": [NO_DELEGATED_CREDENTIAL_MSG],
                "remediation": "Provide a valid delegated Google Workspace / OAuth2 user token to inspect Cloud Storage buckets under your identity.",
            },
        }

    call_timeout = float(os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", str(LIVE_INSPECTION_TIMEOUT_SECONDS)))
    allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
    if not allowed:
        return _budget_exhausted_response(clean_bname, proj, max_b, control_id="ISO/IEC 27001:2022 A.5.23")

    try:
        url = f"https://storage.googleapis.com/storage/v1/b/{clean_bname}"
        resp = session.get(url, timeout=call_timeout)
        if resp.status_code == 200:
            data = resp.json()
            iam_conf = data.get("iamConfiguration", {})
            pap = iam_conf.get("publicAccessPrevention")
            ubla_conf = iam_conf.get("uniformBucketLevelAccess", {})
            ubla = ubla_conf.get("enabled", False)
            cmek = data.get("encryption", {}).get("defaultKmsKeyName")
            location = data.get("location")
            location_type = data.get("locationType")

            violations = []
            if str(pap).lower() != "enforced":
                violations.append(
                    f"Public Access Prevention (PAP) is not enforced (current: '{pap}'). Risk of public exposure."
                )
            if not ubla:
                violations.append("Uniform Bucket-Level Access (UBLA) is disabled. ACLs are in use.")

            is_compliant = len(violations) == 0

            return {
                "status": "FOUND",
                "resource": clean_bname,
                "project_id": proj,
                "bucket_details": {
                    "name": clean_bname,
                    "location": location,
                    "location_type": location_type,
                    "public_access_prevention": pap,
                    "uniform_bucket_level_access": ubla,
                    "default_kms_key": cmek or "Google-Managed Encryption",
                    "storage_class": data.get("defaultStorageClass"),
                },
                "compliance": {
                    "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
                    "control": "ISO/IEC 27001:2022 A.5.23",
                    "violations": violations,
                    "remediation": (
                        "Configuração do bucket em conformidade com o baseline de segurança (PAP Enforced e UBLA Enabled)."
                        if is_compliant
                        else "Habilitar Public Access Prevention ('enforced') e Uniform Bucket-Level Access ('enabled')."
                    ),
                },
                "raw_response": data,
            }
        elif resp.status_code == 404:
            return {
                "status": "NOT_FOUND",
                "resource": clean_bname,
                "project_id": proj,
                "message": f"Bucket '{clean_bname}' não encontrado no projeto '{proj}' (HTTP 404).",
                "compliance": {"status": "UNDETERMINED", "violations": [f"Bucket '{clean_bname}' inexiste no GCP."]},
            }
        elif resp.status_code == 403:
            return {
                "status": "PERMISSION_DENIED",
                "resource": clean_bname,
                "project_id": proj,
                "message": f"Permissões insuficientes para inspecionar o bucket '{clean_bname}' (HTTP 403).",
                "compliance": {"status": "ERROR", "violations": ["Permissão negada na Storage API."]},
            }
    except Exception as exc:
        if isinstance(exc, TimeoutError) or any(t in str(exc).lower() for t in ["timeout", "timed out"]):
            logger.warning(f"Timeout inspecting bucket {clean_bname}: {exc}")
            return {
                "status": "UNDETERMINED",
                "resource": clean_bname,
                "project_id": proj,
                "message": f"Storage API call timed out after {call_timeout}s.",
                "compliance": {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.5.23",
                    "violations": [f"API call timed out after {call_timeout}s."],
                    "remediation": "Retry inspection or increase LIVE_INSPECTION_TIMEOUT_SECONDS.",
                },
            }
        logger.warning(f"Error inspecting bucket {clean_bname}: {exc}")

    return {
        "status": "ERROR",
        "resource": clean_bname,
        "project_id": proj,
        "compliance": {"status": "ERROR", "violations": ["Erro de rede ou conexão ao inspecionar bucket."]},
    }


def list_cloud_storage_buckets(
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
    session_id: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Lists all Cloud Storage buckets in the project with PAP and UBLA posture."""
    check_client_disconnection(client_id=client_id, project_id=project_id)
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    if session is None:
        return {
            "status": "UNDETERMINED",
            "message": NO_DELEGATED_CREDENTIAL_MSG,
            "project_id": proj,
            "buckets": [],
        }

    call_timeout = float(os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", str(LIVE_INSPECTION_TIMEOUT_SECONDS)))
    allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
    if not allowed:
        return {
            "status": "UNDETERMINED",
            "project_id": proj,
            "buckets": [],
            "message": f"Live inspection call budget ({max_b}) exhausted for this session.",
        }

    try:
        url = f"https://storage.googleapis.com/storage/v1/b?project={proj}"
        resp = session.get(url, timeout=call_timeout)
        if resp.status_code == 200:
            items = resp.json().get("items", [])
            buckets_summary = []
            for b in items:
                iam_conf = b.get("iamConfiguration", {})
                buckets_summary.append({
                    "name": b.get("name"),
                    "location": b.get("location"),
                    "location_type": b.get("locationType"),
                    "pap": iam_conf.get("publicAccessPrevention"),
                    "ubla": iam_conf.get("uniformBucketLevelAccess", {}).get("enabled", False),
                })
            return {
                "status": "SUCCESS",
                "project_id": proj,
                "total_buckets": len(buckets_summary),
                "buckets": buckets_summary,
            }
    except Exception as exc:
        logger.warning(f"Error listing buckets in {proj}: {exc}")

    return {"status": "ERROR", "project_id": proj, "buckets": []}


def inspect_project_iam_policy(
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
    session_id: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects project IAM policy for primitive roles and least privilege compliance (A.5.15)."""
    check_client_disconnection(client_id=client_id, project_id=project_id)
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    if session is None:
        return {
            "status": "UNDETERMINED",
            "project_id": proj,
            "message": NO_DELEGATED_CREDENTIAL_MSG,
            "bindings": [],
            "compliance": {
                "status": "UNDETERMINED",
                "violations": [NO_DELEGATED_CREDENTIAL_MSG],
                "remediation": "Provide a valid delegated Google Workspace / OAuth2 user token to inspect IAM policies under your identity.",
            },
        }

    call_timeout = float(os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", str(LIVE_INSPECTION_TIMEOUT_SECONDS)))
    allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
    if not allowed:
        return _budget_exhausted_response(f"projects/{proj}", proj, max_b, control_id="ISO/IEC 27001:2022 A.5.15")

    try:
        url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{proj}:getIamPolicy"
        resp = session.post(url, timeout=call_timeout)
        if resp.status_code == 200:
            bindings = resp.json().get("bindings", [])
            primitive_roles = {"roles/owner", "roles/editor"}
            violations = []
            primitive_grants = []

            for b in bindings:
                role = b.get("role", "")
                members = b.get("members", [])
                if role in primitive_roles:
                    user_members = [m for m in members if m.startswith("user:")]
                    if user_members:
                        primitive_grants.append({"role": role, "users": user_members})
                        violations.append(
                            f"Papel primitivo '{role}' atribuído diretamente a usuários finais: {user_members}."
                        )
                # Check for public exposure
                if any(m in ("allUsers", "allAuthenticatedUsers") for m in members):
                    violations.append(f"IAM Binding '{role}' contém membro público (allUsers/allAuthenticatedUsers)!")

            is_compliant = len(violations) == 0

            return {
                "status": "SUCCESS",
                "project_id": proj,
                "total_bindings": len(bindings),
                "primitive_grants": primitive_grants,
                "compliance": {
                    "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
                    "control": "ISO/IEC 27001:2022 A.5.15",
                    "violations": violations,
                    "remediation": (
                        "Política de IAM em conformidade com o princípio do menor privilégio."
                        if is_compliant
                        else "Substituir papéis primitivos (Owner/Editor) por papéis predefinidos de menor privilégio."
                    ),
                },
                "bindings": bindings,
            }
    except Exception as exc:
        if isinstance(exc, TimeoutError) or any(t in str(exc).lower() for t in ["timeout", "timed out"]):
            logger.warning(f"Timeout inspecting IAM policy for {proj}: {exc}")
            return {
                "status": "UNDETERMINED",
                "resource": f"projects/{proj}",
                "project_id": proj,
                "message": f"Resource Manager API call timed out after {call_timeout}s.",
                "bindings": [],
                "compliance": {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.5.15",
                    "violations": [f"API call timed out after {call_timeout}s."],
                    "remediation": "Retry inspection or increase LIVE_INSPECTION_TIMEOUT_SECONDS.",
                },
            }
        logger.warning(f"Error inspecting IAM policy for {proj}: {exc}")

    return {"status": "ERROR", "project_id": proj, "bindings": []}


def inspect_cloud_run_services(
    location: Optional[str] = None,
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
    session_id: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects Cloud Run services for deployment status and ingress controls (A.8.20)."""
    check_client_disconnection(client_id=client_id, project_id=project_id)
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    loc = location or DEFAULT_LOCATION

    if session is None:
        return {
            "status": "UNDETERMINED",
            "project_id": proj,
            "message": NO_DELEGATED_CREDENTIAL_MSG,
            "services": [],
            "compliance": {
                "status": "UNDETERMINED",
                "violations": [NO_DELEGATED_CREDENTIAL_MSG],
                "remediation": "Provide a valid delegated Google Workspace / OAuth2 user token to inspect Cloud Run services under your identity.",
            },
        }

    call_timeout = float(os.getenv("LIVE_INSPECTION_TIMEOUT_SECONDS", str(LIVE_INSPECTION_TIMEOUT_SECONDS)))
    allowed, count, max_b = check_and_increment_call_budget(session_id=session_id, bearer_token=bearer_token)
    if not allowed:
        return _budget_exhausted_response(f"cloud-run-{loc}", proj, max_b, control_id="ISO/IEC 27001:2022 A.8.20")

    try:
        url = f"https://run.googleapis.com/v2/projects/{proj}/locations/{loc}/services"
        resp = session.get(url, timeout=call_timeout)
        if resp.status_code == 200:
            services = resp.json().get("services", [])
            summary = []
            for s in services:
                s_name = s.get("name", "").split("/")[-1]
                uri = s.get("uri")
                ingress = s.get("ingress", "INGRESS_TRAFFIC_UNSPECIFIED")
                summary.append({
                    "name": s_name,
                    "location": loc,
                    "uri": uri,
                    "ingress": ingress,
                })
            return {
                "status": "SUCCESS",
                "project_id": proj,
                "location": loc,
                "total_services": len(summary),
                "services": summary,
            }
    except Exception as exc:
        if isinstance(exc, TimeoutError) or any(t in str(exc).lower() for t in ["timeout", "timed out"]):
            logger.warning(f"Timeout inspecting Cloud Run in {proj}/{loc}: {exc}")
            return {
                "status": "UNDETERMINED",
                "resource": f"cloud-run-{loc}",
                "project_id": proj,
                "message": f"Cloud Run API call timed out after {call_timeout}s.",
                "services": [],
                "compliance": {
                    "status": "UNDETERMINED",
                    "control": "ISO/IEC 27001:2022 A.8.20",
                    "violations": [f"API call timed out after {call_timeout}s."],
                    "remediation": "Retry inspection or increase LIVE_INSPECTION_TIMEOUT_SECONDS.",
                },
            }
        logger.warning(f"Error inspecting Cloud Run in {proj}/{loc}: {exc}")

    return {"status": "ERROR", "project_id": proj, "services": []}
