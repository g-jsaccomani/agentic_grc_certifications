# ROADMAP & EVOLUÇÃO DA PLATAFORMA AGENTIC GRC (GEAP)

Este documento registra o planejamento estratégico e os itens de backlog técnico para as próximas iterações do **Agentic GRC** no **Gemini Enterprise Agent Platform (GEAP)**.

---

## 1. Backlog Prioritário para Próxima Versão

### 🛡️ Correção de Vulnerabilidade no Código (CodeMender)
- **Controle Normativo Alvo**: ISO/IEC 27001:2022 **Controle A.8.28 (Desenvolvimento Seguro)** e **A.8.25 (Ciclo de Vida de Desenvolvimento Seguro)**.
- **Missão do Sub-agente**:
  O agente orquestrador de conformidade poderá delegar varreduras de código profundas e autônomas para o **CodeMender**.
- **Capacidades Operacionais**:
  1. **Varredura Contínua de Repositórios**:
     - Integração nativa com GitHub Enterprise, GitLab e Cloud Source Repositories.
     - Detecção de vulnerabilidades conhecidas (CVEs), secrets expostos e violações de SAST/DAST.
  2. **Simulação de Testes em Sandbox Segura**:
     - O CodeMender instancia um contêiner sandbox isolado (Jetsky Runtime).
     - Aplica a sugestão de correção e executa as suítes de testes automatizados do projeto para garantir ausência de regressões lógicas (*zero breaking changes*).
  3. **Proposta de Patches e Pull Requests com Gate Humano**:
     - Cria automaticamente um Pull Request com o diff e justificativa formal de segurança.
     - **Regra Zero-Trust**: O patch só é mesclado (*merged*) para a branch de produção após a revisão e aprovação formal (*Human-in-the-Loop*) do time de engenharia e do Lead Auditor.

---

## 2. Visão Geral da Arquitetura de Subagentes GEAP

```
                                  +------------------------------------+
                                  |    GRC Orchestrator Agent (ADK)    |
                                  +-----------------+------------------+
                                                    |
         +--------------------+---------------------+--------------------+--------------------+
         |                    |                     |                    |                    |
         v                    v                     v                    v                    v
+------------------+ +------------------+ +-------------------+ +------------------+ +------------------+
|  Annex A Agent   | |  GCP Telemetry   | |   Org Policies    | | Horizon Scanner  | |    CodeMender    |
| (A.5/6/7/8 Spec) | | (Asset/BQ/VPC)   | | (Zero-Copy Drive) | | (Deep Research)  | |   (A.8.28 Dev)   |
|     [ATIVO]      | |     [ATIVO]      | |      [ATIVO]      | |     [ATIVO]      | |    [BACKLOG]     |
+------------------+ +------------------+ +-------------------+ +------------------+ +------------------+
```

---

## 3. Registro de Histórico de Versões

- **v1.0.0 (Atual)**:
  - Implementação do servidor MCP StreamableHTTP com suporte a A.5.23, A.8.9, A.8.12, A.8.16 e Amd 1:2024.
  - Grafo Lógico de Evidências (`EvidenceGraph`) com hashing SHA-256 e tiers epistêmicos.
  - Memória persistente (`MemoryBank`) com cálculo de velocidade de drift.
  - Motor de remediação (`RemediationEngine`) com validação em sandbox e aprovação humana obrigatória (*HITL*).
  - Conectores Zero-Copy para Google Drive, Confluence, SharePoint, Jira.
  - Subagentes especializados (Annex A, GCP Telemetry, Org Policies, Horizon Scanner).

- **v1.1.0 (Planejada)**:
  - Ativação do módulo **CodeMender** para remediação automatizada em repositórios Git.
  - Conector para Jira Cloud Service Desk para abertura automática de tickets de compliance.
  - Dashboard visual do Agent Studio para modelagem low-code de fluxos de decisão GRC.
