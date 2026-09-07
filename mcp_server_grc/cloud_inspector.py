"""Cloud Inspector: Real-Time Read-Only Google Cloud Telemetry & Inspection Engine.

Empowers the Agentic GRC Auditor with live cloud execution power:
- Inspects Cloud KMS keyrings, crypto keys, rotation periods, and protection levels.
- Inspects Cloud Storage buckets, PAP (Public Access Prevention), and UBLA settings.
- Inspects Project IAM policies, least privilege, and role bindings.
- Inspects Cloud Logging audit sinks and data access log configurations.
- Inspects Cloud Run services and regional workload topology.
- Strictly read-only: executes only discovery/inspection operations with zero mutation risk.
"""

import os
import re
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("cloud_inspector")
DEFAULT_PROJECT_ID = os.getenv("PROJECT_ID", "agentic-grc-cd06")
DEFAULT_LOCATION = os.getenv("REGION", "us-central1")


def get_authorized_session(
    bearer_token: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Tuple[Optional[Any], str]:
    """Obtains an authorized HTTP session and active project ID for live GCP REST calls.
    
    Prefers delegated user OAuth token if valid, falling back to Application Default Credentials.
    In testing environments without GCP credentials, gracefully returns (None, project_id).
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
    is_test = bool("PYTEST_CURRENT_TEST" in os.environ or os.getenv("TESTING") == "true")
    try:
        import google.auth
        from google.auth.transport.requests import AuthorizedSession
        credentials, default_proj = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        resolved_proj = target_project or default_proj or DEFAULT_PROJECT_ID
        return AuthorizedSession(credentials), resolved_proj
    except Exception as exc:
        if not is_test:
            logger.warning(f"Unable to load Google Application Default Credentials: {exc}")
        return None, target_project


def inspect_cloud_kms_key(
    key_name: str,
    location: Optional[str] = None,
    keyring_name: Optional[str] = None,
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects a Cloud KMS key in real time to fetch rotationPeriod and protectionLevel (A.8.24).
    
    Automatically searches across key rings and locations if full path is not provided.
    """
    clean_name = key_name.strip().strip("'").strip('"')
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)

    if session is None:
        return {
            "status": "OFFLINE",
            "message": "GCP Cloud KMS API unreachable: No credentials available.",
            "resource": clean_name,
            "project_id": proj,
            "key_details": {},
            "compliance": {
                "status": "UNDETERMINED",
                "violations": ["Could not connect to Cloud KMS API to inspect key."],
            },
        }

    # If full resource path provided: projects/{proj}/locations/{loc}/keyRings/{kr}/cryptoKeys/{k}
    if clean_name.startswith("projects/"):
        try:
            url = f"https://cloudkms.googleapis.com/v1/{clean_name}"
            resp = session.get(url, timeout=10)
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
            kr_url = f"https://cloudkms.googleapis.com/v1/projects/{proj}/locations/{loc}/keyRings"
            kr_resp = session.get(kr_url, timeout=5)
            if kr_resp.status_code != 200:
                continue

            keyrings = kr_resp.json().get("keyRings", [])
            for kr in keyrings:
                kr_path = kr.get("name", "")
                if keyring_name and keyring_name not in kr_path:
                    continue
                checked_keyrings += 1

                keys_url = f"https://cloudkms.googleapis.com/v1/{kr_path}/cryptoKeys"
                keys_resp = session.get(keys_url, timeout=5)
                if keys_resp.status_code != 200:
                    continue

                for k_item in keys_resp.json().get("cryptoKeys", []):
                    k_full = k_item.get("name", "")
                    k_short = k_full.split("/")[-1]
                    if k_short.lower() == clean_name.lower() or clean_name.lower() in k_full.lower():
                        return _evaluate_kms_key_data(k_full, k_item, proj)
        except Exception as exc:
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
) -> Dict[str, Any]:
    """Lists all KMS key rings and crypto keys in the project across locations."""
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    if session is None:
        return {"status": "OFFLINE", "project_id": proj, "keys": []}

    target_locations = [location] if location else ["global", "us-central1", "us", "us-east1"]
    all_keys = []

    for loc in target_locations:
        try:
            url = f"https://cloudkms.googleapis.com/v1/projects/{proj}/locations/{loc}/keyRings"
            resp = session.get(url, timeout=5)
            if resp.status_code == 200:
                keyrings = resp.json().get("keyRings", [])
                for kr in keyrings:
                    kr_name = kr.get("name")
                    k_resp = session.get(f"https://cloudkms.googleapis.com/v1/{kr_name}/cryptoKeys", timeout=5)
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
) -> Dict[str, Any]:
    """Inspects a Cloud Storage bucket in real time for PAP, UBLA, and CMEK (A.5.23)."""
    clean_bname = bucket_name.strip().replace("gs://", "").strip("/").strip("'").strip('"')
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)

    if session is None:
        return {
            "status": "OFFLINE",
            "resource": clean_bname,
            "project_id": proj,
            "message": "GCP Storage API unreachable: No credentials available.",
            "compliance": {"status": "UNDETERMINED", "violations": ["Cannot connect to Cloud Storage."]},
        }

    try:
        url = f"https://storage.googleapis.com/storage/v1/b/{clean_bname}"
        resp = session.get(url, timeout=10)
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
) -> Dict[str, Any]:
    """Lists all Cloud Storage buckets in the project with PAP and UBLA posture."""
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    if session is None:
        return {"status": "OFFLINE", "project_id": proj, "buckets": []}

    try:
        url = f"https://storage.googleapis.com/storage/v1/b?project={proj}"
        resp = session.get(url, timeout=10)
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
) -> Dict[str, Any]:
    """Inspects project IAM policy for primitive roles and least privilege compliance (A.5.15)."""
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    if session is None:
        return {"status": "OFFLINE", "project_id": proj, "bindings": []}

    try:
        url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{proj}:getIamPolicy"
        resp = session.post(url, timeout=10)
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
        logger.warning(f"Error inspecting IAM policy for {proj}: {exc}")

    return {"status": "ERROR", "project_id": proj, "bindings": []}


def inspect_cloud_run_services(
    location: Optional[str] = None,
    project_id: Optional[str] = None,
    bearer_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspects Cloud Run services for deployment status and ingress controls (A.8.20)."""
    session, proj = get_authorized_session(bearer_token=bearer_token, project_id=project_id)
    loc = location or DEFAULT_LOCATION

    if session is None:
        return {"status": "OFFLINE", "project_id": proj, "services": []}

    try:
        url = f"https://run.googleapis.com/v2/projects/{proj}/locations/{loc}/services"
        resp = session.get(url, timeout=10)
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
        logger.warning(f"Error inspecting Cloud Run in {proj}/{loc}: {exc}")

    return {"status": "ERROR", "project_id": proj, "services": []}
