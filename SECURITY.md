# Security Policy

## Reporting a Vulnerability

The Agentic GRC team takes the security of our compliance platform and user cloud environments seriously. We appreciate responsible disclosure of security vulnerabilities.

### Reporting Mechanism
If you believe you have found a security vulnerability in this project, please report it privately. 

**Do NOT report security vulnerabilities via public GitHub issues or public discussions.**

Please submit your vulnerability report privately via:
- **Email**: `security@jsaccomani.altostrat.com` (or contact the repository maintainers directly via private channels)
- **Subject Line**: `[SECURITY VULNERABILITY] Agentic GRC - <Brief Summary>`

### What to Include in Your Report
To help us triage and reproduce the issue efficiently, please include:
- A detailed description of the vulnerability and its potential impact.
- Step-by-step reproduction instructions or a minimal Proof of Concept (PoC).
- Affected components (e.g., Model Armor Gateway, MCP server endpoints, RBAC/Auth logic, continuous audit collectors).
- Any proposed remediation or mitigation steps, if identified.

### Acknowledgment & Resolution Timeframe
- **Initial Acknowledgment**: We will acknowledge receipt of your vulnerability report within **48 hours**.
- **Assessment & Triage**: We will provide an initial severity assessment and verification status within **5 business days**.
- **Resolution & Disclosure**: We will work on a fix in a private branch, verify it against our test suite, deploy a patch, and coordinate responsible disclosure with the reporter.

## Scope & Protection
We ask that researchers and users adhere to the following:
- Make a good-faith effort to avoid privacy violations, destruction of data, and service disruption during vulnerability testing.
- Do not attempt to access or modify data belonging to other organizations or tenants.
- Give us reasonable time to remediate the vulnerability before public disclosure.
