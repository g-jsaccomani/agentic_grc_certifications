"""Agent Gateway & Model Armor Safety Enforcement Layer.

Implements the 'Iron Triangle' security boundary:
1. Cryptographic SPIFFE Identity
2. Outbound Agent Gateway egress control
3. Model Armor Ingress & Egress content filtering (prompt injection, PII, exfiltration).
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class IngressVerdict:
    allowed: bool
    sanitized_prompt: str
    violations: List[str]
    pii_redacted: bool
    verdict: str  # ALLOW, BLOCK, SANITIZED


@dataclass
class EgressVerdict:
    allowed: bool
    sanitized_output: str
    violations: List[str]
    secrets_redacted: bool
    verdict: str  # ALLOW, BLOCK, REDACTED


class ModelArmorGateway:
    """Inline safety proxy acting as the Agent Gateway and Model Armor evaluator."""

    def __init__(
        self,
        trust_domain: str = "grc.jetsky.gcp",
        allowed_egress_domains: Optional[Set[str]] = None,
    ):
        self.trust_domain = trust_domain
        self.allowed_egress_domains = allowed_egress_domains or {
            "googleapis.com",
            "run.app",
            "google.com",
            "github.com",
        }

        # Prompt Injection & Jailbreak Heuristics
        self._injection_patterns = [
            re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
            re.compile(r"you\s+are\s+now\s+in\s+developer\s+mode", re.IGNORECASE),
            re.compile(r"disregard\s+(all\s+)?rules", re.IGNORECASE),
            re.compile(r"system\s*override", re.IGNORECASE),
            re.compile(r"\bDAN\s+mode\b", re.IGNORECASE),
            re.compile(r"bypass\s+all\s+(security|safety)\s+protocols", re.IGNORECASE),
        ]

        # PII Detection Patterns
        self._email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        self._cpf_ssn_pattern = re.compile(r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")

        # Secret Detection Patterns (Egress)
        self._private_key_pattern = re.compile(r"-----BEGIN[ A-Z0-9_-]*PRIVATE KEY-----[\s\S]*?-----END[ A-Z0-9_-]*PRIVATE KEY-----")
        self._gcp_api_key_pattern = re.compile(r"AIza[0-9A-Za-z_-]{30,40}")
        self._jwt_pattern = re.compile(r"ey[A-Za-z0-9-_=]+\.ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+")

    def get_spiffe_id(self, agent_name: str = "grc-orchestrator", namespace: str = "production") -> str:
        """Generates the SPIFFE cryptographic URI for the agent runtime."""
        return f"spiffe://{self.trust_domain}/ns/{namespace}/sa/{agent_name}"

    def inspect_ingress(self, prompt: str, id_token: Optional[str] = None) -> IngressVerdict:
        """Inspects incoming user prompt for injection, jailbreak attempts, and PII."""
        violations: List[str] = []

        # Check Prompt Injection
        for pattern in self._injection_patterns:
            if pattern.search(prompt):
                violations.append("Prompt injection or system override pattern detected.")
                return IngressVerdict(
                    allowed=False,
                    sanitized_prompt="",
                    violations=violations,
                    pii_redacted=False,
                    verdict="BLOCK",
                )

        # Check and Redact PII
        sanitized = prompt
        pii_found = False

        if self._cpf_ssn_pattern.search(sanitized):
            sanitized = self._cpf_ssn_pattern.sub("[REDACTED_SSN_CPF]", sanitized)
            pii_found = True

        if self._email_pattern.search(sanitized):
            sanitized = self._email_pattern.sub("[REDACTED_EMAIL]", sanitized)
            pii_found = True

        return IngressVerdict(
            allowed=True,
            sanitized_prompt=sanitized,
            violations=violations,
            pii_redacted=pii_found,
            verdict="SANITIZED" if pii_found else "ALLOW",
        )

    def inspect_egress(self, output: str, target_destination: Optional[str] = None) -> EgressVerdict:
        """Inspects agent output and destination to prevent data exfiltration and credential leaks."""
        violations: List[str] = []

        # Check Destination Domain
        if target_destination:
            domain_allowed = any(
                target_destination.endswith(allowed) or target_destination == allowed
                for allowed in self.allowed_egress_domains
            )
            if not domain_allowed:
                violations.append(f"Destination '{target_destination}' is not in the allowed egress perimeter.")
                return EgressVerdict(
                    allowed=False,
                    sanitized_output="",
                    violations=violations,
                    secrets_redacted=False,
                    verdict="BLOCK",
                )

        # Detect and Redact Secrets
        sanitized = output
        secrets_found = False

        if self._private_key_pattern.search(sanitized):
            sanitized = self._private_key_pattern.sub("[REDACTED_PRIVATE_KEY]", sanitized)
            secrets_found = True
            violations.append("Private key leak intercepted and redacted.")

        if self._gcp_api_key_pattern.search(sanitized):
            sanitized = self._gcp_api_key_pattern.sub("[REDACTED_API_KEY]", sanitized)
            secrets_found = True
            violations.append("GCP API key leak intercepted and redacted.")

        return EgressVerdict(
            allowed=True,
            sanitized_output=sanitized,
            violations=violations,
            secrets_redacted=secrets_found,
            verdict="REDACTED" if secrets_found else "ALLOW",
        )
