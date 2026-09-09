"""Agent Gateway & Model Armor Safety Enforcement Layer.

Implements the 'Iron Triangle' security boundary:
1. Cryptographic SPIFFE Identity
2. Outbound Agent Gateway egress control
3. Model Armor Ingress & Egress content filtering (prompt injection, PII, exfiltration, anti-hallucination).
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set


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

        # Prompt Injection, Jailbreak & System Override Heuristics (Multilingual: EN, PT, ES)
        self._injection_patterns = [
            # 1. Instruction / Rule Override Attempts
            re.compile(
                r"(ignore|disregard|forget|override|bypass|desconsidere|esque[cç]a|ignora|ignorar|desconsiderar|olvida|olvidar)"
                r"\s+(all\s+|todas?\s+(as\s+|las\s+|os\s+|los\s+)?)?"
                r"((previous|prior|anterior(es)?|past|pr[eé]vias?)\s+)?"
                r"((iso\s+|soc\s+|pci\s+|cis\s+|audit\s+|compliance\s+|seguran[cç]a\s+)?(instructions|instru[cç][oõ]es|instrucciones|rules|regras|reglas|guidelines|diretrizes|directrices|prompts?|constraints?|system\s*prompts?|policies|pol[ií]ticas|controls?|controles?))"
                r"(\s+(previous|prior|anterior(es)?|past|pr[eé]vias?))?",
                re.IGNORECASE,
            ),
            # 2. Jailbreak Modes & Developer Personas
            re.compile(
                r"(you\s+are\s+now\s+in|enter|switch\s+to|ative|entrar\s+no|ativar\s+o\s+modo|cambia\s+a|pon\s+el\s+modo)\s+.*"
                r"(developer\s+mode|desenvolvedor|desarrollador|unrestricted|unfiltered|god\s*mode|evil\s*mode|jailbreak|\bDAN\s+mode\b)",
                re.IGNORECASE,
            ),
            # 3. Direct DAN mode or Developer mode standalone triggers
            re.compile(r"\b(DAN\s+mode|developer\s+mode|modo\s+desenvolvedor|modo\s+desarrollador)\b", re.IGNORECASE),
            # 4. System / Admin / Security overrides
            re.compile(r"\b(system|admin|root|security|seguran[cç]a)\s*(override|bypass|burlar|bypassar)\b", re.IGNORECASE),
            # 5. Security & Safety Protocol Bypass Requests
            re.compile(
                r"(bypass|disable|desativar|desabilitar|desactivar|ignore|ignorar|desconsidere|desconsiderar)\s+(all\s+|todas?\s+as\s+|todos\s+los\s+|todas?\s+os\s+)?"
                r"(security|safety|guardrails?|protocolos?|compliance|conformidade|prote[cç][oõ]es|((iso|soc|pci)\s+)?controls?|((iso|soc|pci)\s+)?controles?)\s*(protocols?|checks?|filters?|regras|normas)?",
                re.IGNORECASE,
            ),
            # 6. Malicious / Rebellious Roleplay Personas
            re.compile(
                r"(act\s+as|pretend\s+to\s+be|finja\s+que|comporte-se\s+como|hazte\s+pasar\s+por)\s+(an?\s+)?"
                r"(evil|unrestricted|jailbroken|rebellious|malicious|hacker|sem\s+regras|sin\s+reglas)",
                re.IGNORECASE,
            ),
            # 7. Anti-Compliance / Hallucination-Forcing Injections
            re.compile(
                r"(tell\s+me|diga\s+(a\s+todos\s+|me\s+)?que|declare\s+que|state\s+that|afirme\s+que|confirme\s+que)\s+.*"
                r"(iso\s*27001|iso\s*27002|soc\s*2|pci\s*dss|norma|compliance|conformidade|cumplimiento)\s+.*"
                r"(requires|demands|mandates|exige|obriga|pede)\s+.*"
                r"(disabling|removing|shutting\s+down|desativar|desabilitar|remover|apagar|desactivar|eliminat?ing|turning\s+off)\s+.*"
                r"(firewalls?|encryption|criptografia|mfa|backups?|security|access\s+control|waf|tls|controles?)",
                re.IGNORECASE,
            ),
            # 8. Semantic Evasion: Bypass specific control or force compliance (e.g., ignore PAP because staging)
            re.compile(
                r"(ignore|desconsidere|ignora|ignorar|bypass|override)\s+.*"
                r"(pap|ubla|cmek|mfa|firewall|criptografia|encryption|control|controle|controls|controles)\b.*"
                r"(marca|marque|mark|declare|declarar?|force|for[cç]ar?|considere|considerar?|report|reportar?|say|diga)\s+.*"
                r"(conforme|compliant|aprovado|approved)",
                re.IGNORECASE,
            ),
            re.compile(
                r"(force|for[cç]ar?|mark|marcar?|declare|declarar?|report|reportar?)\s+.*"
                r"(as\s+|como\s+)?(compliant|conforme|aprovado|approved)\s+.*"
                r"(because|porque|pois|já\s+que|devido|staging|dev|teste|sandbox|regardless|independentemente|sem\s+considerar|sem\s+evid[eê]ncia|without\s+evidence)",
                re.IGNORECASE,
            ),
            # 9. Direct False Compliance Forcing (e.g., always report compliant regardless of evidence)
            re.compile(
                r"(always|sempre|siempre)\s+.*(report|reportar?|mark|marcar?|declare|declarar?|consider|considere|considerar?)\s+.*(compliant|conforme|approved|aprovado)\s+.*(regardless|independentemente|sem\s+considerar|sin\s+importar|sem\s+evid[eê]ncia|without\s+evidence)",
                re.IGNORECASE,
            ),
        ]

        # PII Detection Patterns
        self._email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        self._cpf_ssn_pattern = re.compile(r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
        self._credit_card_pattern = re.compile(r"\b(?:\d[ -]*?){13,16}\b")

        # Secret Detection Patterns (Egress)
        self._private_key_pattern = re.compile(r"-----BEGIN[ A-Z0-9_-]*PRIVATE KEY-----[\s\S]*?-----END[ A-Z0-9_-]*PRIVATE KEY-----")
        self._gcp_api_key_pattern = re.compile(r"AIza[0-9A-Za-z_-]{30,40}")
        self._jwt_pattern = re.compile(r"ey[A-Za-z0-9-_=]+\.ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+")

        # Anti-Hallucination False Compliance Egress Patterns
        self._anti_hallucination_egress_patterns = [
            re.compile(
                r"(iso\s*27001|iso\s*27002|soc\s*2)\s+.*(requires|mandates|exige|obriga)\s+.*"
                r"(disabling|removing|desativar|desabilitar)\s+.*(firewalls?|encryption|criptografia)",
                re.IGNORECASE,
            ),
        ]

    def get_spiffe_id(self, agent_name: str = "grc-orchestrator", namespace: str = "production") -> str:
        """Generates the SPIFFE cryptographic URI for the agent runtime."""
        return f"spiffe://{self.trust_domain}/ns/{namespace}/sa/{agent_name}"

    def format_block_message(self, violations: List[str], locale: str = "pt") -> str:
        """Returns a formal, authoritative Model Armor block message in the requested locale."""
        loc = (locale or "pt").lower()
        violation_details = "; ".join(violations)
        if loc.startswith("en"):
            return (
                "🛡️ **Model Armor Security Interception**\n\n"
                f"- **Status**: `BLOCKED_BY_MODEL_ARMOR`\n"
                f"- **Detection**: {violation_details}\n\n"
                "**Policy Enforcement Notice**:\n"
                "As an autonomous GRC Readiness Advisor operating on the Gemini Enterprise Agent Platform (GEAP), "
                "this agent is cryptographically bound to ISO/IEC 27001:2022 standards and corporate security policies. "
                "Requests attempting Prompt Injection, System Overrides, Jailbreaks, or forcing false compliance statements "
                "(such as asserting that firewalls or encryption must be disabled) are strictly blocked at the security perimeter."
            )
        elif loc.startswith("es"):
            return (
                "🛡️ **Intercepción de Seguridad Model Armor**\n\n"
                f"- **Estado**: `BLOCKED_BY_MODEL_ARMOR`\n"
                f"- **Detección**: {violation_details}\n\n"
                "**Aviso de Cumplimiento de Políticas**:\n"
                "Como Asesor de Prontitud Autónomo de GRC en Gemini Enterprise Agent Platform (GEAP), "
                "este agente está vinculado criptográficamente a la norma ISO/IEC 27001:2022 y a las políticas corporativas. "
                "Los intentos de Inyección de Prompts, Anulación del Sistema, Jailbreaks o imposición de declaraciones falsas "
                "(como afirmar que deben desactivarse firewalls o criptografía) son bloqueados estrictamente en el perímetro."
            )
        else:
            return (
                "🛡️ **Interceptação de Segurança do Model Armor**\n\n"
                f"- **Status**: `BLOCKED_BY_MODEL_ARMOR`\n"
                f"- **Detecção**: {violation_details}\n\n"
                "**Aviso de Conformidade e Integridade Normativa**:\n"
                "Como Consultor de Prontidão Autônomo de GRC operando sobre o Gemini Enterprise Agent Platform (GEAP), "
                "este agente é ancorado criptograficamente aos controles da ISO/IEC 27001:2022 e às políticas de segurança corporativas. "
                "Tentativas de Prompt Injection, quebra de guardrails (Jailbreak) ou imposição de declarações falsas de conformidade "
                "(como alegar desativação de firewalls ou burlar controles) são sumariamente bloqueadas na borda do sistema."
            )

    def inspect_ingress(self, prompt: str, id_token: Optional[str] = None) -> IngressVerdict:
        """Inspects incoming user prompt for injection, jailbreak attempts, and PII."""
        violations: List[str] = []

        # Check Prompt Injection & Adversarial Jailbreaks
        for pattern in self._injection_patterns:
            if pattern.search(prompt):
                violations.append("Prompt injection, jailbreak or system override pattern intercepted by Model Armor.")
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

        if self._credit_card_pattern.search(sanitized):
            sanitized = self._credit_card_pattern.sub("[REDACTED_CARD]", sanitized)
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

    def _grounding_conflict(self, narrative: str, tool_evidence: Optional[List[Dict[str, Any]]]) -> bool:
        """Verifies if the LLM narrative asserts compliance while tool evidence reports non-compliance."""
        if not tool_evidence:
            return False

        has_non_compliant_evidence = any(
            isinstance(e, dict) and (
                (isinstance(e.get("result"), dict) and e["result"].get("status") in ("NON_COMPLIANT", "ERROR"))
                or e.get("status") in ("NON_COMPLIANT", "ERROR")
            )
            for e in tool_evidence
        )
        if not has_non_compliant_evidence:
            return False

        narrative_lower = narrative.lower()

        # Check if narrative explicitly declares non-compliance or identified violations (in harmony with evidence)
        asserts_non_compliance = any(
            phrase in narrative_lower for phrase in [
                "não conforme", "não-conforme", "não está conforme", "não estão conformes",
                "não é conforme", "não são conformes", "não conformidade", "não-conformidade",
                "inconforme", "non-compliant", "not compliant", "is not compliant",
                "are not compliant", "status: non_compliant", "status: não conforme",
                "status: non-compliant", "defeitos de resiliência", "violações encontradas",
                "violations found", "falhas identificadas", "não atende",
            ]
        )
        if asserts_non_compliance:
            return False

        # Check for explicit affirmative claims of compliance
        affirmative_patterns = [
            r"\b(?:is|are)\s+compliant\b",
            r"\b(?:100%|fully)\s+compliant\b",
            r"\bstatus:\s*compliant\b",
            r"\bverdict:\s*compliant\b",
            r"\bmeets\s+(?:all\s+)?requirements\b",
            r"\b(?:is|are|fully)\s+approved\b",
            r"\b(?:totalmente|100%)\s+conforme\b",
            r"(?<!não\s)(?<!nao\s)\b(?:está|é|são|estão)\s+conforme(?:s)?\b",
            r"\bstatus:\s*conforme\b",
            r"\bveredicto:\s*conforme\b",
            r"\bambiente\s+conforme\b",
            r"\binfraestrutura\s+conforme\b",
            r"\bem\s+(?:total|plena)\s+conformidade\b",
            r"\bem\s+conformidade\s+(?:total|plena)\b",
            r"(?<!não\s)(?<!nao\s)\batende\s+a(?:os)?\s+requisitos\b",
        ]
        claims_compliant = any(
            re.search(pattern, narrative_lower)
            for pattern in affirmative_patterns
        )
        return claims_compliant

    def inspect_egress(
        self,
        output: str,
        target_destination: Optional[str] = None,
        tool_evidence: Optional[List[Dict[str, Any]]] = None,
    ) -> EgressVerdict:
        """Inspects agent output, destination, and tool evidence grounding to prevent exfiltration, leaks, and hallucinations."""
        violations: List[str] = []

        # 1. Check Grounding Conflict against Technical Tool Evidence
        if tool_evidence and self._grounding_conflict(output, tool_evidence):
            violations.append(
                "Grounding conflict intercepted: agent narrative asserts compliance while technical tool evidence reports non-compliance or error."
            )
            return EgressVerdict(
                allowed=False,
                sanitized_output="",
                violations=violations,
                secrets_redacted=False,
                verdict="BLOCK",
            )

        # 2. Check Destination Domain Perimeter
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

        # 3. Check Anti-Hallucination False Compliance Patterns
        for pattern in self._anti_hallucination_egress_patterns:
            if pattern.search(output):
                violations.append("Anti-hallucination guardrail triggered: output contained invalid compliance statements.")
                return EgressVerdict(
                    allowed=False,
                    sanitized_output="",
                    violations=violations,
                    secrets_redacted=False,
                    verdict="BLOCK",
                )

        # 4. Detect and Redact Secrets
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

        if self._jwt_pattern.search(sanitized):
            sanitized = self._jwt_pattern.sub("[REDACTED_JWT_TOKEN]", sanitized)
            secrets_found = True
            violations.append("JWT token leak intercepted and redacted.")

        return EgressVerdict(
            allowed=True,
            sanitized_output=sanitized,
            violations=violations,
            secrets_redacted=secrets_found,
            verdict="REDACTED" if secrets_found else "ALLOW",
        )
