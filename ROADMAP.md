# Roadmap Estratégico — Agentic GRC Platform

Planejamento de evolução da plataforma **Agentic GRC (GEAP)** para governança contínua, auditoria autônoma multi-framework e conformidade multi-cloud.

---

## 1. Fases e Marcos de Evolução (Milestones)

| Marco / Iniciativa | Foco Principal | Principais Entregas | Status |
| :--- | :--- | :--- | :--- |
| **Fundação Concluída** | **ISO 27001:2022 (GCP)** | 93 controles, servidor MCP, 4 fases autônomas, Grafo SHA-256, Dossiê C-Level e Relatório Stage 2 (PDF/JSON). | Concluído ✅ |
| **Interatividade & Governança** | **Questionários ISO & Evidências** | Roteiro de perguntas de auditoria, upload de evidências com hash SHA-256, validação por IA e recálculo em tempo real de métricas e relatórios. | Em Andamento 🚀 |
| **Telemetria Híbrida** | **Conectores Multi-Cloud (AWS & Azure)** | Ingestão de telemetria AWS e Azure via federação OIDC (Zero-Key), abstração unificada de controles (KMS, Storage, IAM, Rede). | Em Andamento 🚀 |
| **Remediação Automatizada** | **CodeMender** | Subagente de correção de código (A.8.28) em sandbox isolado, abertura de PRs com aprovação humana (HITL). | Próximo Ciclo 📋 |
| **Nuvem & Frameworks B2B** | **OCI & SOC 2 / PCI-DSS** | Conector Oracle Cloud (OCI), seletor de certificações (Pré-deploy/Pré-acesso), catálogos SOC 2 Type II e PCI-DSS v4.0. | Backlog 💡 |
| **Conformidade Global 360°** | **NIST CSF & LGPD/GDPR** | NIST CSF 2.0, LGPD/GDPR via Cloud DLP, motor de correlação cruzada (*Collect Once, Comply Many*) e auditoria contínua multi-cloud. | Visão Futura 🌐 |

---

## 2. Pilares Estratégicos de Evolução

```
                   +-------------------------------------------------------------+
                   |             AGENTIC GRC UNIFIED PLATFORM                    |
                   +------------------------------+------------------------------+
                                                  |
         +-----------------------+----------------+----------------+-----------------------+
         |                       |                                 |                       |
         v                       v                                 v                       v
+-----------------+     +-----------------+               +-----------------+     +-----------------+
| PILAR 1         |     | PILAR 2         |               | PILAR 3         |     | PILAR 4         |
| Questionários & |     | Conectores      |               | Expansão        |     | Remediação      |
| Evidências ISO  |     | Multi-Cloud     |               | Multi-Framework |     | Automatizada    |
| (HITL + Métricas|     | (AWS/Azure/OCI) |               | (SOC2/PCI/NIST) |     | (CodeMender)    |
+-----------------+     +-----------------+               +-----------------+     +-----------------+
```

---

### 📝 Pilar 1: Questionários de Auditoria ISO & Anexação de Evidências

Atende aos controles organizacionais (A.5), de pessoas (A.6) e cláusulas de governança (4 a 10) que exigem validação humana e documental.

- **Perguntas Normativas Estruturadas**:
  - Formulário interativo para os 93 controles da ISO 27001 com critérios formais de aceitação.
- **Anexação de Evidências com Integridade SHA-256**:
  - Upload direto (*drag-and-drop*) de políticas (PDF), atas de reunião, relatórios e prints.
  - Carimbo criptográfico (SHA-256) gerado no upload e ancorado ao Grafo de Evidências.
- **Análise & Scoring via Gemini 2.5**:
  - Validação por IA da coerência entre resposta textual e documento anexado.
  - Classificação formal: *Conforme*, *Conforme com Observação*, *Não Conformidade*.
- **Recálculo Imediato em Cascata**:
  - Atualização instantânea do **Scorecard e % de Conformidade**.
  - Atualização do **Dossiê Executivo (C-Level)**.
  - Inclusão automática das evidências no **Relatório Técnico de Auditoria Externa Stage 2 (A4 PDF / JSON / MD)**.

---

### 🌐 Pilar 2: Conectores e Telemetria Multi-Cloud (AWS, Azure, OCI)

Unifica a governança de segurança para organizações que operam em múltiplos provedores de nuvem.

- **Federação de Identidade OIDC (Zero-Key)**:
  - Autenticação sem chaves estáticas usando Google Workload Identity Federation para assumir roles na AWS, Azure e OCI.
- **Conectores Nativos**:
  - **AWS**: Security Hub, AWS Config, IAM Access Analyzer, CloudTrail, KMS, S3.
  - **Microsoft Azure**: Defender for Cloud, Azure Policy, Entra ID, Key Vault, NSGs, Blob Storage.
  - **Oracle Cloud (OCI)**: Cloud Guard, Security Zones, OCI Vault, VCN Security Lists, Object Storage.
- **Abstração Agnóstica de Controles**:
  - Mapeamento uniforme para a ISO 27001:
    - *Criptografia (A.8.24)*: Google Cloud KMS = AWS KMS = Azure Key Vault = OCI Vault.
    - *Segurança de Rede (A.8.20)*: GCP Firewalls = AWS Security Groups = Azure NSGs = OCI Security Lists.
    - *Prevenção de Vazamento (A.8.12)*: GCS = S3 = Azure Blob = OCI Object Storage.
- **Filtro de Visão no Portal**:
  - Alternância entre visões específicas (`GCP`, `AWS`, `Azure`, `OCI`) e a **Postura Consolidada Global**.

---

### 📋 Pilar 3: Expansão Multi-Framework & Mapeamento Cruzado

Transformação do motor de auditoria em uma plataforma multi-normativa com inteligência de reutilização de evidências (*Collect Once, Comply Many*).

- **Novos Frameworks Integrados**:
  - **SOC 2 Type II**: Common Criteria (CC1 a CC9), Disponibilidade e Confidencialidade.
  - **PCI-DSS v4.0**: Requisitos de CDE, tokenização, firewall, criptografia de dados de cartões.
  - **NIST CSF 2.0 & SP 800-53 Rev. 5**: Govern, Identify, Protect, Detect, Respond, Recover.
  - **LGPD / GDPR**: Mapeamento de PII via Cloud DLP e geração de Relatório de Impacto (ROPA).
- **Mecanismos de Seleção**:
  - **Pré-Deploy**: Ativação declarativa via Terraform (`terraform.tfvars`) ou variáveis de ambiente no Cloud Run (`ACTIVE_FRAMEWORKS`).
  - **Pré-Acesso (Runtime)**: Seletor no cabeçalho do portal (*Workspace Switcher*) e wizard de onboarding de certificações.
- **Cross-Mapping de Evidências**:
  - Uma única verificação técnica (ex.: rotação de KMS) satisfaz simultaneamente ISO 27001 (A.8.24), SOC 2 (CC6.1), PCI-DSS (3.5.1) e NIST (PR.DS-01), reduzindo em até 80% o consumo de tokens FinOps via Gemini Context Caching.

---

### 🛡️ Pilar 4: Remediação Automatizada de Código (CodeMender)

Atende aos controles **A.8.28 (Desenvolvimento Seguro)** e **A.8.25 (Ciclo de Vida de Software Seguro)**.

- **Varredura Contínua**: Detecção de CVEs, segredos expostos e violações SAST em repositórios Git (GitHub, GitLab).
- **Sandbox de Testes Isolada**: Aplicação da correção e execução dos testes do projeto em ambiente seguro para validar ausência de regressões (*zero breaking changes*).
- **Pull Request com Gate Humano (HITL)**: Abertura automática de PR com diff e justificativa técnica; merge condicionado à aprovação do time de engenharia e Lead Auditor.

---

## 3. Matriz de Priorização

```
                  ALTO IMPACTO
                       ▲
                       │   [Pilar 1] Questionários & Evidências ISO
                       │   [Pilar 2] Conectores Multi-Cloud (AWS/Azure)
                       │   
                       │   [Pilar 3] SOC 2 Type II & PCI-DSS
                       │   [Pilar 4] CodeMender (Remediação de Código)
                       │   
                       │   [Pilar 3] NIST CSF 2.0 & OCI Connector
                       │   [Pilar 3] LGPD/GDPR Automation
                       └──────────────────────────────────────────►
                     BAIXA                           ALTA
                                 COMPLEXIDADE
```

---

## 4. Diretrizes de Engenharia e Critérios de Conclusão (DoD)

Para cada funcionalidade do Roadmap ser considerada pronta para produção:

1. **Zero Segredos Estáticos**: Qualquer integração multi-cloud ou externa deve utilizar federação OIDC / Workload Identity.
2. **Model Armor & Guardrails Ativos**: Todas as entradas e saídas de novos subagentes devem passar pelos filtros de injeção, redação de PII e anti-alucinação.
3. **Imutabilidade Probatória**: Toda evidência coletada ou anexada deve possuir hash SHA-256 registrado no Grafo de Evidências.
4. **Impacto Contínuo nos Relatórios**: Novos dados devem alimentar automaticamente o Dossiê C-Level e o Relatório Técnico Stage 2 (PDF/JSON).
5. **Cobertura de Testes**: Mínimo de 90% de cobertura com testes unitários e de integração automatizados no CI/CD (`make test`).
