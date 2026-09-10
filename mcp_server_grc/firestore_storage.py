"""Cloud Firestore persistence layer for Client Registry and Questionnaire Tokens.

Provides high-durability storage in Google Cloud Firestore (Native mode) with
concurrency protection across multiple operators and container instances.
Guarantees state survival across Cloud Run container redeployments.
Keeps local file storage (data/clients.json) ONLY as an explicit fallback for
offline local development without Google Cloud credentials.
"""

import os
import json
import logging
import datetime
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger("mcp_server_grc.firestore_storage")

# Global client cache / mock override for unit testing
_FIRESTORE_CLIENT = None
_FIRESTORE_INIT_FAILED = False

# Local memory fallback for questionnaire tokens when running offline
_LOCAL_QUESTIONNAIRE_TOKENS: Dict[str, Dict[str, Any]] = {}

CORE_DEFAULT_CLIENTS = [
    {
        "client_id": "altostrat-ventures",
        "name": "Altostrat Ventures",
        "avatar": "AV",
        "projects": [
            "agentic-grc-cd06",
            "fnlab-apps-8fa913",
            "fnlab-sec-mgmt-8fa913",
            "fnlab-ai-data-8fa913",
            "cspr-nubank",
            "cspr-nubank-poc",
            "cspr-poc-nubank",
        ],
        "org_id": "31564119954",
        "org_name": "jsaccomani.altostrat.com",
        "contact_email": "jsaccomani@google.com",
        "drive_folder_id": "1A2B3C4D5E6F7G8H9I0J-altostrat-evidence",
        "created_at": "2026-09-01T12:00:00Z",
        "read_only_access_expires_at": "2026-09-23T16:00:00Z",
        "read_only_access_days_remaining": 14,
        "status": "active",
        "is_shared": True,
    }
]


def set_firestore_client(client: Any) -> None:
    """Sets a mocked or explicit Firestore client (useful for unit tests)."""
    global _FIRESTORE_CLIENT, _FIRESTORE_INIT_FAILED
    _FIRESTORE_CLIENT = client
    _FIRESTORE_INIT_FAILED = False


def reset_firestore_client() -> None:
    """Resets the cached Firestore client."""
    global _FIRESTORE_CLIENT, _FIRESTORE_INIT_FAILED
    _FIRESTORE_CLIENT = None
    _FIRESTORE_INIT_FAILED = False


def get_clients_file_path() -> str:
    """Returns absolute path to data/clients.json for local fallback."""
    p1 = os.path.join(os.getcwd(), "data", "clients.json")
    if os.path.exists(p1):
        return p1
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p2 = os.path.join(repo_root, "data", "clients.json")
    if os.path.exists(p2):
        return p2
    return p1


def is_firestore_enabled() -> bool:
    """Returns True if Firestore is active and configured; False if falling back to local file."""
    if os.environ.get("FORCE_LOCAL_STORAGE", "").lower() in ("true", "1", "yes"):
        return False
    client = get_firestore_client()
    return client is not None


def get_firestore_client() -> Any:
    """Initializes and returns a Google Cloud Firestore client if credentials/environment permit.
    
    Checks environment for Cloud Run (K_SERVICE), FIRESTORE_DATABASE, or GOOGLE_CLOUD_PROJECT.
    If initialization fails (e.g. no credentials in local dev), returns None and logs fallback.
    """
    global _FIRESTORE_CLIENT, _FIRESTORE_INIT_FAILED

    if _FIRESTORE_CLIENT is not None:
        return _FIRESTORE_CLIENT

    if _FIRESTORE_INIT_FAILED:
        return None

    if os.environ.get("FORCE_LOCAL_STORAGE", "").lower() in ("true", "1", "yes"):
        return None

    # Check if in Cloud Run or explicitly enabled or emulator host is present
    is_cloud_run = bool(os.environ.get("K_SERVICE"))
    explicit_enable = os.environ.get("ENABLE_FIRESTORE", "").lower() in ("true", "1", "yes")
    has_emulator = bool(os.environ.get("FIRESTORE_EMULATOR_HOST"))
    has_project = bool(os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT"))

    if not (is_cloud_run or explicit_enable or has_emulator or has_project):
        # Local development without Firestore environment
        return None

    try:
        from google.cloud import firestore
        project = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
        database = os.environ.get("FIRESTORE_DATABASE", "(default)")
        if database == "(default)":
            _FIRESTORE_CLIENT = firestore.Client(project=project)
        else:
            _FIRESTORE_CLIENT = firestore.Client(project=project, database=database)
        logger.info("Connected to Google Cloud Firestore (database=%s, project=%s)", database, project)
        return _FIRESTORE_CLIENT
    except Exception as exc:
        _FIRESTORE_INIT_FAILED = True
        logger.warning(
            "Firestore client unavailable (%s). Falling back to local data/clients.json storage.",
            exc,
        )
        return None


# ---------------------------------------------------------------------------
# Client Registry CRUD
# ---------------------------------------------------------------------------

def load_clients_from_store() -> List[Dict[str, Any]]:
    """Loads onboarded client workspace records from Firestore with fallback to data/clients.json."""
    client = get_firestore_client()
    if client is not None:
        try:
            coll_ref = client.collection("clients")
            docs = list(coll_ref.stream())
            if docs:
                clients = [doc.to_dict() for doc in docs]
                # Ensure client_id is set
                for idx, doc in enumerate(docs):
                    if "client_id" not in clients[idx]:
                        clients[idx]["client_id"] = doc.id
                return clients
            else:
                # Firestore collection is empty - seed initial core client into Firestore
                for core_client in CORE_DEFAULT_CLIENTS:
                    cid = core_client["client_id"]
                    coll_ref.document(cid).set(core_client)
                return [dict(c) for c in CORE_DEFAULT_CLIENTS]
        except Exception as e:
            logger.warning("Error reading clients from Firestore: %s. Falling back to local file.", e)

    # Fallback to local data/clients.json
    file_path = get_clients_file_path()
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    return data
        except Exception as e:
            logger.warning("Failed to read clients.json fallback: %s", e)

    return [dict(c) for c in CORE_DEFAULT_CLIENTS]


def save_clients_to_store(clients: List[Dict[str, Any]]) -> None:
    """Persists onboarded client list to Firestore and local clients.json."""
    client = get_firestore_client()
    if client is not None:
        try:
            coll_ref = client.collection("clients")
            # Upsert each client doc
            existing_cids = {doc.id for doc in coll_ref.stream()}
            new_cids = set()
            for c in clients:
                cid = c.get("client_id")
                if cid:
                    new_cids.add(cid)
                    coll_ref.document(cid).set(c)
            # Remove deleted clients from Firestore
            for stale_cid in (existing_cids - new_cids):
                if stale_cid != "altostrat-ventures":
                    coll_ref.document(stale_cid).delete()
        except Exception as e:
            logger.warning("Error saving clients to Firestore: %s", e)

    # Also persist to local file as backup / local dev cache
    try:
        path = get_clients_file_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(clients, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning("Error saving to local clients.json: %s", e)


def save_single_client_to_store(client_data: Dict[str, Any]) -> None:
    """Saves or updates a single client record."""
    cid = client_data.get("client_id")
    if not cid:
        raise ValueError("client_data missing 'client_id'")

    client = get_firestore_client()
    if client is not None:
        try:
            coll_ref = client.collection("clients")
            coll_ref.document(cid).set(client_data)
        except Exception as e:
            logger.warning("Error saving client '%s' to Firestore: %s", cid, e)

    # Update local file cache
    all_clients = load_clients_from_store()
    replaced = False
    for i, c in enumerate(all_clients):
        if c.get("client_id") == cid:
            all_clients[i] = client_data
            replaced = True
            break
    if not replaced:
        all_clients.append(client_data)

    try:
        path = get_clients_file_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(all_clients, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning("Error writing to local clients.json cache: %s", e)


def delete_client_from_store(client_id: str) -> None:
    """Deletes a client workspace record from Firestore and local cache."""
    if client_id == "altostrat-ventures":
        raise ValueError("Cannot delete core client 'altostrat-ventures'")

    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("clients").document(client_id).delete()
        except Exception as e:
            logger.warning("Error deleting client '%s' from Firestore: %s", client_id, e)

    # Remove from local file
    try:
        path = get_clients_file_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                all_clients = json.load(f)
            new_list = [c for c in all_clients if c.get("client_id") != client_id]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(new_list, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning("Error updating local clients.json on deletion: %s", e)


# ---------------------------------------------------------------------------
# Questionnaire Link Tokens CRUD
# ---------------------------------------------------------------------------

def save_questionnaire_token(token_record: Dict[str, Any]) -> None:
    """Stores a scoped questionnaire access token in Firestore with local memory fallback."""
    token = token_record.get("token")
    if not token:
        raise ValueError("token_record must contain 'token'")

    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("questionnaire_tokens").document(token).set(token_record)
        except Exception as e:
            logger.warning("Error saving questionnaire token to Firestore: %s", e)

    _LOCAL_QUESTIONNAIRE_TOKENS[token] = dict(token_record)


def get_questionnaire_token(token: str) -> Optional[Dict[str, Any]]:
    """Retrieves questionnaire access token from Firestore or local fallback."""
    if not token:
        return None

    client = get_firestore_client()
    if client is not None:
        try:
            doc = client.collection("questionnaire_tokens").document(token).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            logger.warning("Error retrieving questionnaire token from Firestore: %s", e)

    return _LOCAL_QUESTIONNAIRE_TOKENS.get(token)


def revoke_questionnaire_token(token: str) -> bool:
    """Revokes a questionnaire access token."""
    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("questionnaire_tokens").document(token).update({"status": "revoked"})
        except Exception:
            pass

    if token in _LOCAL_QUESTIONNAIRE_TOKENS:
        _LOCAL_QUESTIONNAIRE_TOKENS[token]["status"] = "revoked"
        return True
    return False


# Aliases for client operations
save_client_to_store = save_single_client_to_store
load_onboarded_clients_from_store = load_clients_from_store

def get_data_dir() -> str:
    """Returns directory path to data/ directory."""
    d = os.path.join(os.getcwd(), "data")
    if os.path.exists(d):
        return d
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d2 = os.path.join(repo_root, "data")
    os.makedirs(d2, exist_ok=True)
    return d2

# Local questionnaire answers and evidence nodes paths
_ANSWERS_FILE_PATH = os.path.join(get_data_dir(), "questionnaire_answers.json")
_EVIDENCE_NODES_FILE_PATH = os.path.join(get_data_dir(), "evidence_graph_nodes.json")


def save_questionnaire_answer_to_store(framework: str, control_id: str, answer_data: Dict[str, Any]) -> None:
    """Persists a questionnaire answer to Firestore with fallback to data/questionnaire_answers.json."""
    client = get_firestore_client()
    doc_id = f"{framework}_{control_id}".replace(":", "_").replace(".", "_")
    if client is not None:
        try:
            client.collection("questionnaire_answers").document(doc_id).set(answer_data)
        except Exception as e:
            logger.warning("Error saving questionnaire answer to Firestore: %s", e)

    # Local file fallback
    try:
        data = {}
        if os.path.exists(_ANSWERS_FILE_PATH):
            with open(_ANSWERS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        key = f"{framework}:{control_id}"
        data[key] = answer_data
        with open(_ANSWERS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.warning("Error persisting questionnaire answer to local JSON: %s", e)


def load_questionnaire_answers_from_store() -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Loads questionnaire answers from Firestore with fallback to data/questionnaire_answers.json."""
    answers = {}
    client = get_firestore_client()
    if client is not None:
        try:
            docs = client.collection("questionnaire_answers").stream()
            for d in docs:
                data = d.to_dict()
                fw = data.get("framework", "ISO27001:2022")
                cid = data.get("control_id")
                if cid:
                    answers[(fw, cid)] = data
            if answers:
                return answers
        except Exception as e:
            logger.warning("Error loading questionnaire answers from Firestore: %s", e)

    # Local fallback
    if os.path.exists(_ANSWERS_FILE_PATH):
        try:
            with open(_ANSWERS_FILE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for k, val in raw.items():
                if ":" in k:
                    fw, cid = k.rsplit(":", 1)
                    answers[(fw, cid)] = val
        except Exception as e:
            logger.warning("Error loading questionnaire answers from local JSON: %s", e)

    return answers


def save_evidence_node_to_store(node_data: Dict[str, Any]) -> None:
    """Persists an evidence graph node to Firestore with fallback to data/evidence_graph_nodes.json."""
    node_id = node_data.get("node_id")
    if not node_id:
        return
    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("evidence_nodes").document(node_id).set(node_data)
        except Exception as e:
            logger.warning("Error saving evidence node to Firestore: %s", e)

    # Local file fallback
    try:
        nodes = []
        if os.path.exists(_EVIDENCE_NODES_FILE_PATH):
            with open(_EVIDENCE_NODES_FILE_PATH, "r", encoding="utf-8") as f:
                nodes = json.load(f)
        nodes = [n for n in nodes if n.get("node_id") != node_id]
        nodes.append(node_data)
        with open(_EVIDENCE_NODES_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(nodes, f, indent=2)
    except Exception as e:
        logger.warning("Error persisting evidence node to local JSON: %s", e)


def load_evidence_nodes_from_store() -> List[Dict[str, Any]]:
    """Loads evidence graph nodes from Firestore with fallback to data/evidence_graph_nodes.json."""
    client = get_firestore_client()
    if client is not None:
        try:
            docs = client.collection("evidence_nodes").stream()
            nodes = [d.to_dict() for d in docs]
            if nodes:
                return nodes
        except Exception as e:
            logger.warning("Error loading evidence nodes from Firestore: %s", e)

    if os.path.exists(_EVIDENCE_NODES_FILE_PATH):
        try:
            with open(_EVIDENCE_NODES_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Error reading evidence nodes from local JSON: %s", e)

    return []
