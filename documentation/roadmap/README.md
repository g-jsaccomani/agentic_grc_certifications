# Roadmap Estratégico — Agentic GRC Platform

Planejamento de evolução da plataforma **Agentic GRC (GEAP)** para governança contínua, auditoria autônoma multi-framework e conformidade multi-cloud.

**Escopo declarado da ferramenta:** o Agentic GRC realiza auditoria, coleta de evidências e recomendações de adequação. **A ferramenta não modifica código, infraestrutura ou configurações do ambiente do cliente** — toda correção é responsabilidade do time do cliente, orientada pelos achados e recomendações do auditor.

---

## 1. Fases e Marcos de Evolução (Milestones)

| Marco / Iniciativa | Foco Principal | Principais Entregas | Status |
| :--- | :--- | :--- | :--- |
| **Fundação** | **ISO 27001:2022 (GCP)** | 93 controles, servidor MCP, inspeção ao vivo (KMS, Storage, IAM, Cloud Run), Grafo SHA-256, Dossiê C-Level e Relatório Stage 2 (PDF/JSON). | Em Andamento 🚀 |
| **Interatividade & Governança** | **Questionários ISO & Evidências** | Roteiro de perguntas de auditoria, upload de evidências validado por conteúdo, validação por IA com tier de confiança separado (autodeclarado vs. verificado), e recálculo em tempo real de métricas e relatórios. | Em Andamento 🚀 |
| **Telemetria Híbrida** | **Conectores Multi-Cloud (AWS & Azure)** | Ingestão de telemetria AWS e Azure via federação OIDC (Zero-Key), abstração unificada de controles (KMS, Storage, IAM, Rede). | Backlog 💡 |
| **Nuvem & Frameworks B2B** | **OCI & SOC 2 / PCI-DSS** | Conector Oracle Cloud (OCI), seletor de certificações (Pré-deploy/Pré-acesso), catálogos SOC 2 Type II e PCI-DSS v4.0. | Backlog 💡 |
| **Conformidade Global 360°** | **NIST CSF & LGPD/GDPR** | NIST CSF 2.0, LGPD/GDPR via Cloud DLP, motor de correlação cruzada (*Collect Once, Comply Many*) e auditoria contínua multi-cloud. | Visão Futura 🌐 |

---

## 2. Percentual de Implementação por Pilar

> Percentuais baseados em verificação funcional direta (execução real de testes e endpoints),
> não em estimativa de esforço restante. Atualizado nesta revisão do roadmap.

| Pilar | % Implementado | O que já funciona de verdade | O que falta |
| :--- | :---: | :--- | :--- |
| **Fundação (ISO 27001 / GCP)** | **90%** | Inspeção ao vivo real para KMS, Cloud Storage, IAM e Cloud Run (falha fechada sem credencial, não fabrica dado). MCP server com dual-token + verificação de assinatura obrigatória. | Inspeção ao vivo de Firewall/VPC e Compute Engine ainda depende de config informado, não de chamada real à API. |
| **Pilar 1 — Questionários & Evidências** | **90%** | CRUD completo dos 93 controles, upload de evidência validado por conteúdo real (não extensão), tier `SELF_ATTESTED` separado de `VERIFIED`/`TELEMETRY`, validação de consistência por IA com fallback conservador, recálculo em cascata no scorecard/relatórios. | Seção de Metodologia/Responsabilidade do Auditor nos relatórios; taxonomia de severidade (Maior/Menor/OFI) ainda binária em alguns pontos. |
| **Pilar 2 — Multi-Cloud (AWS/Azure/OCI)** | **5%** | Seletor visual "em breve" no portal, honesto sobre o estado atual. | Nenhum conector real. Federação OIDC, ingestão de telemetria e mapeamento de controles ainda não iniciados. |
| **Pilar 3 — Multi-Framework (SOC2/PCI/NIST/LGPD)** | **15%** | Campo `framework` já existe em toda a cadeia de dados (resposta, evidência, link de conformidade) sem exigir migração futura. Catálogo SOC 2 com 5 controles-piloto (Common Criteria). | PCI-DSS, NIST CSF e LGPD sem catálogo. Motor de mapeamento cruzado (*Collect Once, Comply Many*) não iniciado. |

---

## 3. Pilares Estratégicos de Evolução

```
                   +-------------------------------------------------------------+
                   |             AGENTIC GRC UNIFIED PLATFORM                    |
                   +------------------------------+------------------------------+
                                                  |
                   +-----------------------+-----------------+-----------------------+
                   |                       |                                       |
                   v                       v                                       v
          +-----------------+     +-----------------+                     +-----------------+
          | PILAR 1         |     | PILAR 2         |                     | PILAR 3         |
          | Questionários & |     | Conectores      |                     | Expansão        |
          | Evidências ISO  |     | Multi-Cloud     |                     | Multi-Framework |
          | (HITL + Métricas|     | (AWS/Azure/OCI) |                     | (SOC2/PCI/NIST) |
          +-----------------+     +-----------------+                     +-----------------+
```

---

### 📝 Pilar 1: Questionários de Auditoria ISO & Anexação de Evidências

Atende aos controles organizacionais (A.5), de pessoas (A.6) e cláusulas de governança (4 a 10) que exigem validação humana e documental.

- **Perguntas Normativas Estruturadas**:
  - Formulário interativo para os 93 controles da ISO 27001 com critérios formais de aceitação.
- **Anexação de Evidências com Integridade SHA-256**:
  - Upload direto (*drag-and-drop*) de políticas (PDF), atas de reunião, relatórios e prints, validado por conteúdo real do arquivo (não por extensão).
  - Carimbo criptográfico (SHA-256) gerado no upload e ancorado ao Grafo de Evidências.
- **Análise & Scoring via Gemini 2.5**:
  - Validação por IA da coerência entre resposta textual e documento anexado.
  - Classificação formal: *Conforme*, *Conforme com Observação*, *Não Conformidade*.
  - Distinção explícita entre evidência autodeclarada (`SELF_ATTESTED`) e evidência verificada por telemetria (`VERIFIED`/`TELEMETRY`) — nunca apresentadas com o mesmo peso.
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
  - Uma única verificação técnica (ex.: rotação de KMS) satisfaz simultaneamente ISO 27001 (A.8.24), SOC 2 (CC6.1), PCI-DSS (3.5.1) e NIST (PR.DS-01) — a redução de consumo de tokens via Gemini Context Caching será medida e reportada quando esse mecanismo for implementado, não estimada previamente.

---

## 4. Matriz de Priorização

```
                  ALTO IMPACTO
                       ▲
                       │   [Pilar 1] Questionários & Evidências ISO
                       │   [Pilar 2] Conectores Multi-Cloud (AWS/Azure)
                       │
                       │   [Pilar 3] SOC 2 Type II & PCI-DSS
                       │
                       │   [Pilar 3] NIST CSF 2.0 & OCI Connector
                       │   [Pilar 3] LGPD/GDPR Automation
                       └──────────────────────────────────────────►
                     BAIXA                           ALTA
                                 COMPLEXIDADE
```

---

## 5. Diretrizes de Engenharia e Critérios de Conclusão (DoD)

Para cada funcionalidade do Roadmap ser considerada pronta para produção:

1. **Zero Segredos Estáticos**: Qualquer integração multi-cloud ou externa deve utilizar federação OIDC / Workload Identity.
2. **Model Armor & Guardrails Ativos**: Todas as entradas e saídas de novos subagentes devem passar pelos filtros de injeção, redação de PII e anti-alucinação.
3. **Imutabilidade Probatória**: Toda evidência coletada ou anexada deve possuir hash SHA-256 registrado no Grafo de Evidências.
4. **Impacto Contínuo nos Relatórios**: Novos dados devem alimentar automaticamente o Dossiê C-Level e o Relatório Técnico Stage 2 (PDF/JSON).
5. **Cobertura de Testes**: Mínimo de 90% de cobertura com testes unitários e de integração automatizados no CI/CD (`make test`).
6. **Verificação ao Vivo Obrigatória**: Nenhuma funcionalidade é considerada concluída apenas com testes unitários passando — é exigida ao menos uma verificação contra o endpoint real (não a função isolada) antes de qualquer status ser marcado como "Concluído".
