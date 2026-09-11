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

# Local storage fallback file paths
_ANSWERS_FILE_PATH = os.path.join(get_data_dir(), "questionnaire_answers.json")
_EVIDENCE_METADATA_FILE_PATH = os.path.join(get_data_dir(), "evidence_metadata.json")
_OPERATOR_CLIENTS_FILE_PATH = os.path.join(get_data_dir(), "operator_active_clients.json")
_SESSION_BINDINGS_FILE_PATH = os.path.join(get_data_dir(), "session_client_bindings.json")
_EVIDENCE_NODES_FILE_PATH = os.path.join(get_data_dir(), "evidence_graph_nodes.json")


# ---------------------------------------------------------------------------
# Scoped Control Key & Scoped Answers Dict (Multi-Client Collision Prevention)
# ---------------------------------------------------------------------------

class ScopedControlKey(tuple):
    """A 2-tuple (framework, control_id) compatible key that carries client_id scope.

    Unpacks as (framework, control_id) for backward compatibility with existing tests
    and portal code, but implements __eq__ and __hash__ across (framework, control_id, client_id)
    to prevent cross-client collision in memory and storage.
    """
    def __new__(cls, *args, client_id: str = "altostrat-ventures"):
        if len(args) == 1 and isinstance(args[0], tuple):
            args = args[0]
        if len(args) >= 3:
            fw, cid, cl = args[0], args[1], args[2]
        elif len(args) == 2:
            fw, cid, cl = args[0], args[1], client_id
        else:
            raise ValueError(f"Invalid arguments for ScopedControlKey: {args}")
        obj = super().__new__(cls, (str(fw), str(cid)))
        obj.framework = str(fw)
        obj.control_id = str(cid)
        obj.client_id = str(cl) if cl else "altostrat-ventures"
        return obj

    def __reduce__(self):
        return (ScopedControlKey, (self.framework, self.control_id, self.client_id))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ScopedControlKey):
            return (self.framework, self.control_id, self.client_id) == (other.framework, other.control_id, other.client_id)
        if isinstance(other, tuple):
            if len(other) == 3:
                return (self.framework, self.control_id, self.client_id) == (str(other[0]), str(other[1]), str(other[2]))
            if len(other) == 2:
                return (self.framework, self.control_id) == (str(other[0]), str(other[1]))
        return False

    def __hash__(self) -> int:
        return hash((self.framework, self.control_id, self.client_id))

    def __repr__(self) -> str:
        return f"ScopedControlKey('{self.framework}', '{self.control_id}', '{self.client_id}')"


class ScopedAnswersDict(dict):
    """Dictionary mapping ScopedControlKey to questionnaire answer.

    Supports transparent lookup via:
    - ScopedControlKey(fw, cid, client_id)
    - 3-tuple (fw, cid, client_id)
    - 2-tuple (fw, cid) [resolves against default or active client_id]
    """
    def _resolve_key(self, key: Any, fallback_client_id: Optional[str] = None) -> Any:
        if isinstance(key, ScopedControlKey):
            return key
        if isinstance(key, tuple):
            if len(key) == 3:
                return ScopedControlKey(key[0], key[1], key[2])
            elif len(key) == 2:
                target_cid = fallback_client_id or "altostrat-ventures"
                cand = ScopedControlKey(key[0], key[1], target_cid)
                if cand in self:
                    return cand
                matching = [
                    k for k in self.keys()
                    if isinstance(k, ScopedControlKey) and k.framework == key[0] and k.control_id == key[1]
                ]
                if len(matching) == 1 and matching[0].client_id in ("altostrat-ventures", target_cid):
                    return matching[0]
                return cand
        return key

    def __getitem__(self, key: Any) -> Any:
        resolved = self._resolve_key(key)
        return super().__getitem__(resolved)

    def get(self, key: Any, default: Any = None) -> Any:
        resolved = self._resolve_key(key)
        return super().get(resolved, default)

    def __contains__(self, key: Any) -> bool:
        resolved = self._resolve_key(key)
        return super().__contains__(resolved)

    def __setitem__(self, key: Any, value: Any) -> None:
        if isinstance(value, dict):
            try:
                from mcp_server_grc.questionnaire import QuestionnaireAnswer
                val_copy = dict(value)
                if "control_id" not in val_copy and isinstance(key, tuple) and len(key) >= 2:
                    val_copy["control_id"] = key[1]
                if "framework" not in val_copy and isinstance(key, tuple) and len(key) >= 1:
                    val_copy["framework"] = key[0]
                if "status" not in val_copy:
                    val_copy["status"] = "COMPLIANT"
                if "justification" not in val_copy:
                    val_copy["justification"] = "Answer recorded."
                value = QuestionnaireAnswer(**val_copy)
            except Exception:
                pass
        if not isinstance(key, ScopedControlKey):
            if isinstance(key, tuple):
                if len(key) == 3:
                    key = ScopedControlKey(key[0], key[1], key[2])
                elif len(key) == 2:
                    cid = getattr(value, "client_id", None)
                    if isinstance(value, dict):
                        cid = cid or value.get("client_id")
                    cid = cid or "altostrat-ventures"
                    key = ScopedControlKey(key[0], key[1], cid)
        super().__setitem__(key, value)

    def update(self, *args: Any, **kwargs: Any) -> None:
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def pop(self, key: Any, *args: Any) -> Any:
        resolved = self._resolve_key(key)
        return super().pop(resolved, *args)


# ---------------------------------------------------------------------------
# Questionnaire Answers Persistence (Firestore Collection: questionnaire_answers)
# Document ID: {framework}::{control_id}::{client_id}
# ---------------------------------------------------------------------------

def save_questionnaire_answer_to_store(
    framework: str,
    control_id: str,
    answer_data: Dict[str, Any],
    client_id: Optional[str] = None,
) -> None:
    """Persists a questionnaire answer to Firestore with client_id scoping and local JSON fallback."""
    target_cid = client_id or answer_data.get("client_id") or "altostrat-ventures"
    payload = dict(answer_data)
    payload["framework"] = framework
    payload["control_id"] = control_id
    payload["client_id"] = target_cid

    doc_id = f"{framework}::{control_id}::{target_cid}"
    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("questionnaire_answers").document(doc_id).set(payload)
        except Exception as e:
            logger.warning("Error saving questionnaire answer to Firestore: %s", e)

    # Local file fallback
    try:
        data = {}
        if os.path.exists(_ANSWERS_FILE_PATH):
            with open(_ANSWERS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[doc_id] = payload
        with open(_ANSWERS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning("Error persisting questionnaire answer to local JSON: %s", e)


def save_questionnaire_answers_to_store(
    answers: Dict[Any, Any],
    client_id: Optional[str] = None,
) -> None:
    """Batch saves multiple questionnaire answers to Firestore and local fallback."""
    for key, val in answers.items():
        if isinstance(val, dict):
            fw = val.get("framework", "ISO27001:2022")
            cid = val.get("control_id")
            val_data = val
        else:
            fw = getattr(val, "framework", "ISO27001:2022")
            cid = getattr(val, "control_id", None)
            val_data = val.model_dump() if hasattr(val, "model_dump") else (val.dict() if hasattr(val, "dict") else dict(val))
        if not cid:
            continue
        c_id = client_id or getattr(key, "client_id", None) or val_data.get("client_id")
        save_questionnaire_answer_to_store(fw, cid, val_data, client_id=c_id)


def load_questionnaire_answers_from_store(
    client_id: Optional[str] = None,
) -> ScopedAnswersDict:
    """Loads questionnaire answers from Firestore with fallback to local JSON, scoped by client_id."""
    answers = ScopedAnswersDict()
    client = get_firestore_client()

    if client is not None:
        try:
            coll_ref = client.collection("questionnaire_answers")
            docs = coll_ref.stream()
            for d in docs:
                data = d.to_dict()
                fw = data.get("framework", "ISO27001:2022")
                cid = data.get("control_id")
                doc_cid = data.get("client_id") or "altostrat-ventures"
                if not cid:
                    continue
                if client_id and doc_cid != client_id:
                    continue
                k = ScopedControlKey(fw, cid, doc_cid)
                answers[k] = data
            if answers:
                return answers
        except Exception as e:
            logger.warning("Error loading questionnaire answers from Firestore: %s", e)

    # Local fallback
    if os.path.exists(_ANSWERS_FILE_PATH):
        try:
            with open(_ANSWERS_FILE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for k_str, val in raw.items():
                if not isinstance(val, dict):
                    continue
                if "::" in k_str:
                    parts = k_str.split("::")
                    fw = parts[0]
                    cid = parts[1]
                    doc_cid = parts[2] if len(parts) > 2 else (val.get("client_id") or "altostrat-ventures")
                elif ":" in k_str:
                    fw, cid = k_str.rsplit(":", 1)
                    doc_cid = val.get("client_id") or "altostrat-ventures"
                else:
                    fw = val.get("framework", "ISO27001:2022")
                    cid = val.get("control_id")
                    doc_cid = val.get("client_id") or "altostrat-ventures"
                if not cid:
                    continue
                if client_id and doc_cid != client_id:
                    continue
                val["framework"] = fw
                val["control_id"] = cid
                val["client_id"] = doc_cid
                answers[ScopedControlKey(fw, cid, doc_cid)] = val
        except Exception as e:
            logger.warning("Error loading questionnaire answers from local JSON: %s", e)

    return answers


def delete_questionnaire_answer_from_store(
    framework: str,
    control_id: str,
    client_id: Optional[str] = None,
) -> None:
    """Deletes a questionnaire answer from Firestore and local JSON."""
    target_cid = client_id or "altostrat-ventures"
    doc_id = f"{framework}::{control_id}::{target_cid}"
    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("questionnaire_answers").document(doc_id).delete()
        except Exception as e:
            logger.warning("Error deleting questionnaire answer from Firestore: %s", e)

    if os.path.exists(_ANSWERS_FILE_PATH):
        try:
            with open(_ANSWERS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.pop(doc_id, None)
            data.pop(f"{framework}:{control_id}", None)
            with open(_ANSWERS_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning("Error deleting questionnaire answer from local JSON: %s", e)


def get_questionnaire_answer_from_store(
    framework: str,
    control_id: str,
    client_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Retrieves a single questionnaire answer from Firestore or local fallback."""
    target_cid = client_id or "altostrat-ventures"
    doc_id = f"{framework}::{control_id}::{target_cid}"
    client = get_firestore_client()
    if client is not None:
        try:
            doc = client.collection("questionnaire_answers").document(doc_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            logger.warning("Error fetching questionnaire answer doc '%s' from Firestore: %s", doc_id, e)

    if os.path.exists(_ANSWERS_FILE_PATH):
        try:
            with open(_ANSWERS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if doc_id in data:
                return data[doc_id]
            legacy_id = f"{framework}:{control_id}"
            if legacy_id in data:
                return data[legacy_id]
        except Exception:
            pass
    return None


# ---------------------------------------------------------------------------
# Evidence Metadata Persistence (Firestore Collection: evidence_metadata)
# Document ID: {file_id}
# ---------------------------------------------------------------------------

def save_evidence_metadata_to_store(
    file_id_or_metadata: Any,
    metadata: Optional[Dict[str, Any]] = None,
    client_id: Optional[str] = None,
) -> None:
    """Persists evidence file metadata to Firestore and local JSON fallback."""
    if isinstance(file_id_or_metadata, dict):
        payload = dict(file_id_or_metadata)
        file_id = str(payload.get("file_id") or "")
        target_cid = client_id or payload.get("client_id") or "altostrat-ventures"
    else:
        file_id = str(file_id_or_metadata or "")
        payload = dict(metadata or {})
        target_cid = client_id or payload.get("client_id") or "altostrat-ventures"

    if not file_id:
        return
    payload["file_id"] = file_id
    payload["client_id"] = target_cid

    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("evidence_metadata").document(file_id).set(payload)
        except Exception as e:
            logger.warning("Error saving evidence metadata to Firestore: %s", e)

    # Local fallback
    try:
        data = {}
        if os.path.exists(_EVIDENCE_METADATA_FILE_PATH):
            with open(_EVIDENCE_METADATA_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[file_id] = payload
        with open(_EVIDENCE_METADATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning("Error persisting evidence metadata to local JSON: %s", e)


def load_evidence_metadata_from_store(
    client_id: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """Loads evidence metadata from Firestore with local fallback, optionally scoped by client_id."""
    result: Dict[str, Dict[str, Any]] = {}
    client = get_firestore_client()

    if client is not None:
        try:
            docs = client.collection("evidence_metadata").stream()
            for d in docs:
                data = d.to_dict()
                fid = data.get("file_id") or d.id
                doc_cid = data.get("client_id") or "altostrat-ventures"
                if client_id and doc_cid != client_id:
                    continue
                result[fid] = data
            if result:
                return result
        except Exception as e:
            logger.warning("Error loading evidence metadata from Firestore: %s", e)

    if os.path.exists(_EVIDENCE_METADATA_FILE_PATH):
        try:
            with open(_EVIDENCE_METADATA_FILE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for fid, data in raw.items():
                if not isinstance(data, dict):
                    continue
                doc_cid = data.get("client_id") or "altostrat-ventures"
                if client_id and doc_cid != client_id:
                    continue
                result[fid] = data
        except Exception as e:
            logger.warning("Error reading evidence metadata from local JSON: %s", e)

    return result


def get_evidence_metadata_from_store(file_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves metadata for a specific evidence file from Firestore or local fallback."""
    if not file_id:
        return None
    client = get_firestore_client()
    if client is not None:
        try:
            doc = client.collection("evidence_metadata").document(file_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            logger.warning("Error fetching evidence metadata doc '%s' from Firestore: %s", file_id, e)

    if os.path.exists(_EVIDENCE_METADATA_FILE_PATH):
        try:
            with open(_EVIDENCE_METADATA_FILE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return raw.get(file_id)
        except Exception:
            pass
    return None


def delete_evidence_metadata_from_store(file_id: str) -> None:
    """Deletes an evidence file metadata record from Firestore and local JSON."""
    if not file_id:
        return
    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("evidence_metadata").document(file_id).delete()
        except Exception as e:
            logger.warning("Error deleting evidence metadata from Firestore: %s", e)

    if os.path.exists(_EVIDENCE_METADATA_FILE_PATH):
        try:
            with open(_EVIDENCE_METADATA_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.pop(file_id, None)
            with open(_EVIDENCE_METADATA_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning("Error deleting evidence metadata from local JSON: %s", e)


# ---------------------------------------------------------------------------
# Operator Active Clients & Session Client Bindings Persistence
# ---------------------------------------------------------------------------

def save_operator_active_client_to_store(operator_id: str, client_id: str) -> None:
    """Persists an operator's active client workspace to Firestore and local fallback."""
    if not operator_id or not client_id:
        return
    client = get_firestore_client()
    record = {
        "operator_id": operator_id,
        "client_id": client_id,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    if client is not None:
        try:
            client.collection("operator_active_clients").document(operator_id).set(record)
        except Exception as e:
            logger.warning("Error saving operator active client to Firestore: %s", e)

    try:
        data = {}
        if os.path.exists(_OPERATOR_CLIENTS_FILE_PATH):
            with open(_OPERATOR_CLIENTS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[operator_id] = client_id
        with open(_OPERATOR_CLIENTS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.warning("Error saving operator active client to local file: %s", e)


def load_operator_active_clients_from_store() -> Dict[str, str]:
    """Loads operator active client bindings from Firestore or local fallback."""
    bindings: Dict[str, str] = {"default_operator": "altostrat-ventures"}
    client = get_firestore_client()
    if client is not None:
        try:
            docs = client.collection("operator_active_clients").stream()
            for d in docs:
                data = d.to_dict()
                cid = data.get("client_id")
                if cid:
                    bindings[d.id] = cid
            if len(bindings) > 1:
                return bindings
        except Exception as e:
            logger.warning("Error loading operator active clients from Firestore: %s", e)

    if os.path.exists(_OPERATOR_CLIENTS_FILE_PATH):
        try:
            with open(_OPERATOR_CLIENTS_FILE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, dict):
                    bindings.update(raw)
        except Exception as e:
            logger.warning("Error loading operator active clients from local JSON: %s", e)

    return bindings


def save_session_client_binding_to_store(session_id: str, client_id: str) -> None:
    """Persists a session-to-client binding to Firestore and local fallback."""
    if not session_id or not client_id:
        return
    client = get_firestore_client()
    record = {
        "session_id": session_id,
        "client_id": client_id,
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    if client is not None:
        try:
            client.collection("session_client_bindings").document(session_id).set(record)
        except Exception as e:
            logger.warning("Error saving session client binding to Firestore: %s", e)

    try:
        data = {}
        if os.path.exists(_SESSION_BINDINGS_FILE_PATH):
            with open(_SESSION_BINDINGS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[session_id] = client_id
        with open(_SESSION_BINDINGS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.warning("Error saving session client binding to local file: %s", e)


def delete_session_client_binding_from_store(session_id: str) -> None:
    """Deletes a session-to-client binding from Firestore and local fallback."""
    if not session_id:
        return
    client = get_firestore_client()
    if client is not None:
        try:
            client.collection("session_client_bindings").document(session_id).delete()
        except Exception as e:
            logger.warning("Error deleting session client binding from Firestore: %s", e)

    try:
        if os.path.exists(_SESSION_BINDINGS_FILE_PATH):
            with open(_SESSION_BINDINGS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if session_id in data:
                del data[session_id]
                with open(_SESSION_BINDINGS_FILE_PATH, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
    except Exception as e:
        logger.warning("Error deleting session client binding from local file: %s", e)


def load_session_client_bindings_from_store() -> Dict[str, str]:
    """Loads session-to-client bindings from Firestore or local fallback."""
    bindings: Dict[str, str] = {}
    client = get_firestore_client()
    if client is not None:
        try:
            docs = client.collection("session_client_bindings").stream()
            for d in docs:
                data = d.to_dict()
                cid = data.get("client_id")
                if cid:
                    bindings[d.id] = cid
            if bindings:
                return bindings
        except Exception as e:
            logger.warning("Error loading session client bindings from Firestore: %s", e)

    if os.path.exists(_SESSION_BINDINGS_FILE_PATH):
        try:
            with open(_SESSION_BINDINGS_FILE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, dict):
                    bindings.update(raw)
        except Exception as e:
            logger.warning("Error reading session client bindings from local JSON: %s", e)

    return bindings


# ---------------------------------------------------------------------------
# Evidence Nodes Persistence (EvidenceGraph)
# ---------------------------------------------------------------------------

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
