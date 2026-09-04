# ROADMAP & EVOLUÇÃO DA PLATAFORMA AGENTIC GRC (GEAP)

Este documento registra o planejamento estratégico, os itens de backlog técnico e a expansão para múltiplos frameworks regulatórios do **Agentic GRC** no **Gemini Enterprise Agent Platform (GEAP)**.

---

## 1. Visão Geral Estratégica: De ISO 27001 para Plataforma Multi-Framework

O Agentic GRC nasceu focado na automação completa dos 93 controles da **ISO/IEC 27001:2022** em ambientes Google Cloud. A próxima grande evolução transformará a plataforma em um motor **Multi-Framework Unificado**, permitindo auditar, simultaneamente ou de forma selecionada, os principais padrões globais de segurança, privacidade e governança corporativa.

```
                              +-------------------------------------------------------+
                              |        GCP Organization & Multi-Project Scope         |
                              +---------------------------+---------------------------+
                                                          |
                                                          v
                                     +-----------------------------------------+
                                     |   FRAMEWORK SELECTOR & CROSS-MAPPING    |
                                     |   (Pré-Deploy / Pré-Acesso / Onboarding)|
                                     +--------------------+--------------------+
                                                          |
             +--------------------+-----------------------+-----------------------+--------------------+
             |                    |                       |                       |                    |
             v                    v                       v                       v                    v
    +-----------------+  +-----------------+     +-----------------+     +-----------------+  +-----------------+
    | ISO 27001:2022  |  | SOC 2 Type II   |     |  PCI-DSS v4.0   |     | NIST CSF 2.0 /  |  |  LGPD & GDPR    |
    | (93 Controles)  |  | (Trust Criteria)|     | (CDE & Cloud)   |     | SP 800-53 Rev 5 |  | (DLP & Privacy) |
    +-----------------+  +-----------------+     +-----------------+     +-----------------+  +-----------------+
             |                    |                       |                       |                    |
             +--------------------+-----------------------+-----------------------+--------------------+
                                                          |
                                                          v
                                     +-----------------------------------------+
                                     |  UNIFIED EVIDENCE GRAPH & TELEMETRY     |
                                     |  (Zero-Copy: Ingest Once, Satisfy Many) |
                                     +--------------------+--------------------+
                                                          |
                                                          v
                                     +-----------------------------------------+
                                     |  ORCHESTRATOR & SUBAGENTS (Gemini 2.5)  |
                                     +-----------------------------------------+
```

---

## 2. Mecanismos de Seleção: Pré-Deploy e Pré-Acesso

Para garantir flexibilidade operacional, redução no consumo de tokens e adequação a diferentes clientes corporativos, a plataforma suportará a seleção dos frameworks em dois momentos cruciais:

### 2.1. Seleção Pré-Deploy (Deploy-Time Configuration)
Permite que o time de infraestrutura/SRE defina os frameworks ativados antes de compilar ou provisionar o serviço no Cloud Run:

1. **Variáveis de Ambiente / Cloud Run**:
   - `ACTIVE_FRAMEWORKS`: Lista delimitada por vírgula dos frameworks carregados na memória do contêiner.
     ```bash
     ACTIVE_FRAMEWORKS=ISO27001,SOC2,PCIDSS,NIST_CSF,LGPD
     ```
   - `DEFAULT_FRAMEWORK`: Framework ativo por padrão ao abrir a aplicação (ex.: `ISO27001` ou `SOC2`).
   - `ENABLE_CROSS_MAPPING`: `true` ativa a pontuação e correlação cruzada automática de evidências entre normas.

2. **Parâmetros no Terraform Bootstrap (`first_steps`)**:
   - Configuração declarativa no arquivo `terraform.tfvars`:
     ```hcl
     enabled_frameworks = [
       "iso_27001_2022",
       "soc_2_type_2",
       "pci_dss_v4",
       "nist_csf_2_0",
       "lgpd_gdpr"
     ]
     ```
   - Provisionamento condicional de permissões IAM e conectores específicos (ex.: módulo específico de cartões para PCI-DSS).

3. **Vantagens do Pré-Deploy**:
   - Imagens de contêiner otimizadas e consumo menor de memória RAM.
   - Bloqueio rígido de frameworks fora do escopo contratual da organização.

---

### 2.2. Seleção Pré-Acesso (Runtime Onboarding & Workspace Switcher)
Permite que o Lead Auditor e os times de segurança escolham dinamicamente quais frameworks auditar durante o uso da plataforma:

1. **Tela de Boas-Vindas / Onboarding Wizard**:
   - Ao acessar o portal pela primeira vez ou iniciar uma nova auditoria (`Nova Auditoria`), o usuário é recebido por uma tela modal com a seleção de frameworks:
     - Checkbox interativo com cards visuais de cada certificação (ISO 27001, SOC 2, PCI-DSS, NIST, LGPD).
     - Exibição da quantidade de controles associados e dos subagentes especializados necessários.
     - Estimativa prévia de custo de tokens FinOps com base na seleção.

2. **Seletor Global de Frameworks no Topo da Interface (Workspace Switcher)**:
   - Um menu suspenso (*dropdown com setinha*) na barra superior ao lado do Escopo de Projetos:
     - Permite alternar a visão ativa (ex.: visualizar apenas a Matriz SOC 2 ou a Matriz ISO 27001).
     - Modo **"Visão Consolidada Multi-Framework"**: Mostra a conformidade global da Organização cruzando todas as normas selecionadas.

3. **Grafo de Evidências com Mapeamento Cruzado (*Cross-Mapping Engine*)**:
   - **Princípio "Collect Once, Comply Many"**:
     - Uma única evidência de telemetria GCP (ex.: Cloud KMS com rotação automática de 90 dias) satisfaz:
       - **ISO 27001**: A.8.24 (Uso de Criptografia).
       - **SOC 2**: CC6.1 (Controles Lógicos e Criptografia em Repouso).
       - **PCI-DSS v4.0**: Requisito 3.5.1 (Gestão e Proteção de Chaves Criptográficas).
       - **NIST CSF 2.0**: PR.DS-01 (Dados Protegidos em Repouso).
     - Isso elimina o reprocessamento redundante de tokens Gemini (economia de até 80% via Context Caching).

---

## 3. Catálogo de Novos Frameworks no Roadmap

### 📋 SOC 2 Type II (AICPA Trust Services Criteria)
- **Foco**: Relatório de atestação para clientes B2B sobre a segurança dos serviços em nuvem.
- **Categorias Alvo**:
  - **Security (Common Criteria - CC1 a CC9)**: Controle de acesso IAM, monitoramento contínuo, resposta a incidentes.
  - **Availability (A1)**: Resiliência, backups, SLA no Google Cloud, Disaster Recovery.
  - **Confidentiality (C1)**: Proteção de dados confidenciais, DLP, Cloud KMS.
  - **Processing Integrity (PI1)**: Integridade e validação de pipelines de dados (Dataflow, BigQuery).
  - **Privacy (P1 a P8)**: Gestão de consentimento e retenção.
- **Subagente Especialista**: `SOC2SubAgent` (Auditor de Common Criteria e Geração de Pacote de Evidências para Auditores Externos Big 4).

### 💳 PCI-DSS v4.0 (Payment Card Industry Data Security Standard)
- **Foco**: Proteção de Dados de Titulares de Cartão (CHD) e Dados Sensíveis de Autenticação (SAD).
- **Controles Chave no GCP**:
  - **Requisito 1**: Firewall e Cloud Armor / VPC Service Controls ao redor do CDE (*Cardholder Data Environment*).
  - **Requisito 3**: Proteção de dados de cartões via criptografia forte (Cloud KMS / HSM).
  - **Requisito 7 & 8**: Acesso restrito por menor privilégio, MFA obrigatório e Workload Identity.
  - **Requisito 10**: Logs de auditoria imutáveis com Cloud Logging e BigQuery de retenção de 1 ano.
- **Subagente Especialista**: `PCIDSSSubAgent` (Varredura de perímetros de rede CDE e tokenização de cartões).

### 🏛️ NIST CSF 2.0 & NIST SP 800-53 Rev. 5
- **Foco**: Estrutura governamental e corporativa de cibersegurança dos EUA, amplamente adotada por grandes empresas.
- **Funções CSF 2.0**:
  - **Govern (GV)**: Políticas, estratégia e gestão de riscos da organização.
  - **Identify (ID)**: Gestão de inventário de ativos (Cloud Asset Inventory).
  - **Protect (PR)**: IAM, proteção de dados, conscientização.
  - **Detect (DE)**: Security Command Center (SCC Enterprise), detecção de anomalias.
  - **Respond (RS)** & **Recover (RC)**: Resposta a incidentes e resiliência operacional.
- **Subagente Especialista**: `NISTSubAgent` (Mapeamento de maturidade e relatórios no formato SP 800-53).

### ⚖️ LGPD (Brasil) & GDPR (Europa)
- **Foco**: Governança de privacidade, conformidade com a Autoridade Nacional de Proteção de Dados (ANPD) e direitos dos titulares.
- **Capacidades**:
  - Inventário e classificação automática de dados pessoais (PII) via **Cloud Data Loss Prevention (Cloud DLP)**.
  - Registro das Operações de Tratamento (ROPA - Relatório de Impacto à Proteção de Dados).
  - Auditoria de medidas técnicas de segurança (Art. 46 da LGPD) e notificação de incidentes (Art. 48).
- **Subagente Especialista**: `PrivacyAuditorSubAgent` (Conformidade com ANPD, relatórios RIPD e auditoria de políticas de privacidade).

### 🎯 CIS Google Cloud Foundation Benchmark v3.0
- **Foco**: Hardening técnico direto dos recursos e configurações de infraestrutura na GCP.
- **Seções**:
  - 1. Identity and Access Management (IAM)
  - 2. Logging and Monitoring
  - 3. Networking & Perimeter
  - 4. Virtual Machines & Compute Engine
  - 5. Storage (Cloud Storage Buckets & Database Hardening)
- **Subagente Especialista**: `CISBenchmarkSubAgent` (Verificação automatizada contra o checklist oficial do CIS).

---

## 4. Cronograma de Lançamento e Versões

| Versão | Escopo Principal | Destaques Técnicos | Previsão |
| :--- | :--- | :--- | :--- |
| **v1.0.0** (Live) | **ISO/IEC 27001:2022 Completa** | Servidor MCP, 93 controles, 4 fases autônomas, Grafo de Evidências, FinOps Dashboard, Dropdown de Projetos da Organização. | Concluído ✅ |
| **v1.1.0** (Próxima) | **Remediação de Código (CodeMender)** | Subagente de correção automática de código em sandbox (A.8.28), PRs automatizados com gate HITL, conector Jira. | Sprint Atual 🚀 |
| **v1.2.0** | **Seletor de Frameworks & SOC 2 Type II** | Onboarding Wizard de certificações, variáveis pré-deploy, catálogo SOC 2 (Common Criteria), subagente `SOC2SubAgent`. | Q4 2026 |
| **v1.3.0** | **PCI-DSS v4.0 & LGPD / GDPR** | Auditoria de CDE e Cloud DLP integrado, subagentes `PCIDSSSubAgent` e `PrivacyAuditorSubAgent`, gerador de ROPA. | Q1 2027 |
| **v2.0.0** | **NIST CSF 2.0 & CIS GCP Benchmark** | Matriz Unificada Multi-Framework 360°, Cross-Mapping Engine em tempo real, auditorias contínuas entre nuvens. | Q2 2027 |

---

## 5. Backlog Técnico Prioritário (CodeMender)

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
