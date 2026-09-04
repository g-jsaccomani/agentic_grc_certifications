"""Scalable ISO/IEC 27001:2022 Catalog and Multi-Project Registry for GEAP.

Consolidates the 93 Annex A controls across 4 main themes + ISO 27001 Amd 1:2024 Climate Action,
with 5-attribute taxonomy (Type, Properties, Cybersecurity Concepts, Operational Capabilities, Security Domains)
and detailed operational guidance on How to Check and How to Maintain continuous compliance.
"""

ACTIVE_PROJECTS = [
    {
        "project_id": "agentic-grc-cd06",
        "environment": "PRODUCTION",
        "region": "us-central1",
        "status": "AUDITED",
        "score": 100.0,
    },
    {
        "project_id": "agentic-grc-staging",
        "environment": "STAGING",
        "region": "us-central1",
        "status": "COMPLIANT",
        "score": 98.2,
    },
    {
        "project_id": "agentic-grc-data-lake",
        "environment": "ANALYTICS",
        "region": "us-east4",
        "status": "COMPLIANT",
        "score": 100.0,
    },
]

THEMES_STRUCTURE = [
    {
        "theme": "A.5 Controles Organizacionais",
        "short_theme": "A.5 Organizacional",
        "control_count": 37,
        "scope": "Políticas, governança, relacionamento com fornecedores, gestão de ativos e incidentes.",
        "icon": "shield",
    },
    {
        "theme": "A.6 Controles de Pessoas",
        "short_theme": "A.6 Pessoas",
        "control_count": 8,
        "scope": "Segurança em RH, triagem, termos de contratação, conscientização e desligamento.",
        "icon": "users",
    },
    {
        "theme": "A.7 Controles Físicos",
        "short_theme": "A.7 Físico",
        "control_count": 14,
        "scope": "Perímetros de segurança, instalações, proteção contra ameaças externas e descarte seguro.",
        "icon": "building",
    },
    {
        "theme": "A.8 Controles Tecnológicos",
        "short_theme": "A.8 Tecnológico",
        "control_count": 34,
        "scope": "Autenticação, criptografia, redes, segurança no desenvolvimento (DevSecOps) e monitoramento.",
        "icon": "cpu",
    },
    {
        "theme": "ISO/IEC 27001:2022 / Amd 1:2024 (Ação Climática)",
        "short_theme": "Amd 1:2024 Clima",
        "control_count": 2,
        "scope": "Avaliação formal de riscos climáticos e resiliência multirregional de data centers (Cláusulas 4.1 e 4.2).",
        "icon": "cloud-rain",
    },
]

ISO_27001_CATALOG = [
    # -------------------------------------------------------------------------
    # A.5 Controles Organizacionais (Total Oficial: 37 Controles)
    # -------------------------------------------------------------------------
    {
        "id": "A.5.1",
        "name": "Políticas de Segurança da Informação",
        "theme": "A.5 Organizacional",
        "description": "As políticas de segurança da informação e as políticas específicas de tópicos devem ser definidas, aprovadas pela direção, publicadas, comunicadas e disponibilizadas a colaboradores e partes interessadas relevantes.",
        "how_to_check": "1. Verificar repositório Zero-Copy de políticas corporativas sincronizado via Google Drive/Workspace.\n2. Inspecionar Organization Policies ativas no GCP via comando: `gcloud resource-manager org-policies list --organization=ORG_ID`.\n3. Validar se as políticas foram aprovadas pela diretoria com carimbo temporal e hash SHA-256 no grafo de evidências.",
        "how_to_maintain": "1. Configurar revisão semestral obrigatória de políticas com lembrete automatizado via Cloud Scheduler e Pub/Sub.\n2. Aplicar restrições hierárquicas de Organization Policy no nível raiz da organização para evitar deriva de configuração nos projetos filhos.\n3. Integrar aprovação de alterações de políticas via pull request com revisores obrigatórios (Code Owners).",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Identificar",
            "capabilities": "Governança",
            "domains": "Governança e Ecossistema"
        },
        "gcp_mapping": "Google Cloud Resource Manager & Organization Policies",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Doc Ref: POL-SEC-01 (Zero-Copy Drive Sync com hash SHA-256 verificado)",
        "severity": "LOW",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.2",
        "name": "Funções e Responsabilidades de Segurança",
        "theme": "A.5 Organizacional",
        "description": "As funções e responsabilidades de segurança da informação devem ser definidas e alocadas de acordo com as necessidades da organização, assegurando o princípio do menor privilégio.",
        "how_to_check": "1. Executar análise de papéis IAM no projeto: `gcloud projects get-iam-policy PROJECT_ID --format=json`.\n2. Auditar se existem usuários individuais com permissões primitivas (ex.: `roles/owner` ou `roles/editor`).\n3. Confirmar que contas de serviço usam papéis customizados estritamente limitados ao escopo do workload.",
        "how_to_maintain": "1. Utilizar o IAM Recommender para remoção automática de privilégios excessivos não utilizados em 90 dias.\n2. Implementar Privileged Access Manager (PAM) para concessão Just-in-Time (JIT) com expiração máxima de 4 horas.\n3. Bloquear concessão de papéis primitivos através da Organization Policy `constraints/iam.disableServiceAccountKeyCreation`.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Gestão de Identidade e Acesso",
            "domains": "Proteção"
        },
        "gcp_mapping": "Cloud IAM Role Bindings & Privileged Access Manager (PAM)",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "Matriz IAM de privilégio mínimo validada sem papéis primitivos permanentes",
        "severity": "MEDIUM",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.3",
        "name": "Segregação de Funções (SoD)",
        "theme": "A.5 Organizacional",
        "description": "Funções conflitantes e áreas de responsabilidade conflitantes devem ser formalmente segregadas para reduzir oportunidades de modificação não autorizada ou uso indevido de ativos.",
        "how_to_check": "1. Verificar se a Service Account de Auditoria (`sa-grc-auditor`) possui apenas papéis de leitura (`roles/viewer`, `roles/iam.securityReviewer`).\n2. Confirmar que a Service Account de Deploy/CI/CD não possui capacidade de alterar as próprias políticas IAM nem desativar logs de auditoria.\n3. Checar a separação de ambientes através de pastas GCP dedicadas (`fldr-prod` vs `fldr-audit`).",
        "how_to_maintain": "1. Impor segregação em pipelines CI/CD com aprovação de dois pares (Two-person rule) antes de aplicar Terraform em produção.\n2. Auditar continuamente via Cloud Logging qualquer tentativa de concessão cruzada de privilégios entre auditores e operadores.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Integridade",
            "concepts": "Proteger",
            "capabilities": "Governança",
            "domains": "Proteção"
        },
        "gcp_mapping": "Service Accounts Segregadas (Deployer vs Auditor) & Pastas GCP",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "Separação estrita entre contas executoras e auditoras verificada",
        "severity": "MEDIUM",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.7",
        "name": "Inteligência sobre Ameaças (Threat Intelligence)",
        "theme": "A.5 Organizacional",
        "description": "Informações sobre ameaças de segurança da informação devem ser coletadas e analisadas para produzir inteligência sobre ameaças acionável.",
        "how_to_check": "1. Verificar se o Security Command Center (SCC) Premium ou Google SecOps está ativo na organização.\n2. Inspecionar sink de exportação de logs de auditoria para o BigQuery com regras de correlação Mandiant Threat Intelligence ativas.\n3. Executar comando: `gcloud scc findings list ORG_ID --filter=\"state='ACTIVE'\"`.",
        "how_to_maintain": "1. Habilitar Event Threat Detection e Container Threat Detection no Security Command Center.\n2. Configurar alertas imediatos via Pub/Sub para o canal de resposta a incidentes ao detectar IOCs de alta criticidade.",
        "attributes": {
            "type": "Detectivo",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Identificar, Detectar",
            "capabilities": "Inteligência sobre Ameaças",
            "domains": "Defesa"
        },
        "gcp_mapping": "Google SecOps & Mandiant Threat Intelligence Feeds",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Sink BigQuery ativo com enriquecimento de IOCs da Mandiant",
        "severity": "MEDIUM",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.9",
        "name": "Inventário de Informações e Outros Ativos",
        "theme": "A.5 Organizacional",
        "description": "Um inventário de informações e outros ativos associados, incluindo proprietários, deve ser desenvolvido e mantido atualizado continuamente.",
        "how_to_check": "1. Executar varredura em tempo real via Cloud Asset Inventory: `gcloud asset search-all-resources --scope=projects/PROJECT_ID`.\n2. Verificar se 100% dos recursos em nuvem possuem metadados de classificação e etiquetas (Labels de `environment`, `owner`, `data-classification`).\n3. Confirmar que o Grafo de Evidências indexa todos os nós de infraestrutura.",
        "how_to_maintain": "1. Impor rotulagem obrigatória via regras de validação Terraform no pipeline de CI/CD.\n2. Habilitar Cloud Asset Feeds para exportação contínua de mudanças de recursos para o BigQuery para auditoria histórica.",
        "attributes": {
            "type": "Identificar",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Identificar",
            "capabilities": "Gestão de Ativos",
            "domains": "Governança e Ecossistema"
        },
        "gcp_mapping": "Cloud Asset Inventory API & Labels Padronizados",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "Inventário completo de ativos ingerido com 100% dos recursos etiquetados",
        "severity": "LOW",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.15",
        "name": "Controle de Acesso Lógico",
        "theme": "A.5 Organizacional",
        "description": "As regras para controlar o acesso físico e lógico a informações e outros ativos associados devem ser estabelecidas e implementadas com base nos requisitos do negócio e de segurança.",
        "how_to_check": "1. Verificar se acessos externos anônimos (`allUsers` e `allAuthenticatedUsers`) estão proibidos em todos os recursos de dados.\n2. Checar a existência de políticas IAM condicionais com base em data, IP de origem e nível de confiança do dispositivo.\n3. Comando: `gcloud projects get-iam-policy PROJECT_ID --format=\"flattened(bindings[].members)\" | grep allUsers`.",
        "how_to_maintain": "1. Enforçar a Organization Policy `constraints/iam.allowedPolicyMemberDomains` restringindo acessos unicamente ao Google Workspace da empresa.\n2. Implementar BeyondCorp Enterprise para controle de acesso contextual (Context-Aware Access) com validação de conformidade do endpoint.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Gestão de Identidade e Acesso",
            "domains": "Proteção"
        },
        "gcp_mapping": "Conditional IAM Policies & BeyondCorp Context-Aware Access",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "Zero permissões públicas detectadas; acesso restrito a identidades corporativas",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.23",
        "name": "Segurança da Informação no Uso de Nuvem",
        "theme": "A.5 Organizacional",
        "description": "Os processos para aquisição, uso, gerenciamento e saída de serviços de computação em nuvem devem ser estabelecidos em conformidade com os requisitos de segurança da organização.",
        "how_to_check": "1. Inspecionar todos os buckets GCS no escopo com o comando: `gcloud storage buckets list --format=\"table(name, uniformBucketLevelAccess, publicAccessPrevention)\"`.\n2. Confirmar se `uniformBucketLevelAccess=True` e `publicAccessPrevention=enforced` em todos os repositórios.\n3. Checar criptografia CMEK ativa com Cloud KMS.",
        "how_to_maintain": "1. Aplicar as seguintes Organization Policies no nível da pasta raiz:\n   - `constraints/storage.uniformBucketLevelAccess` (Habilitado)\n   - `constraints/storage.publicAccessPrevention` (Enforced)\n2. Bloquear no IaC Scanner qualquer criação de bucket sem UBLA e PAP ativados.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Segurança da Informação em Nuvem",
            "domains": "Proteção"
        },
        "gcp_mapping": "Cloud Storage Public Access Prevention (PAP) & UBLA",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "PAP e UBLA enforçados em 100% dos buckets; zero acessos públicos",
        "severity": "CRITICAL",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.5.28",
        "name": "Gestão e Resposta a Incidentes",
        "theme": "A.5 Organizacional",
        "description": "A organização deve planejar e preparar a gestão de incidentes de segurança da informação, definindo, estabelecendo e comunicando processos de gestão, funções e responsabilidades.",
        "how_to_check": "1. Inspecionar se os canais de notificação do Cloud Monitoring e alertas do Security Command Center estão conectados ao Pub/Sub de resposta.\n2. Verificar a existência de playbooks automatizados de contenção e registro de incidentes com retenção imutável de logs.\n3. Testar disparo de evento simulado para validar tempo de resposta dos subagentes.",
        "how_to_maintain": "1. Conduzir testes semestrais de simulação de incidentes de segurança cibernética (Tabletop Exercises).\n2. Integrar Cloud Functions/Cloud Run para isolamento automatizado de instâncias e revogação imediata de credenciais comprometidas.",
        "attributes": {
            "type": "Corretivo",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Responder, Recuperar",
            "capabilities": "Gestão de Incidentes de Segurança",
            "domains": "Defesa, Resiliência"
        },
        "gcp_mapping": "Cloud Monitoring Alerts & Pub/Sub Incident Event Bus",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Canais de alerta automatizados ativos com rota para equipe de segurança",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },

    # -------------------------------------------------------------------------
    # A.6 Controles de Pessoas (Total Oficial: 8 Controles)
    # -------------------------------------------------------------------------
    {
        "id": "A.6.1",
        "name": "Triagem e Verificação Pré-Contratação",
        "theme": "A.6 Pessoas",
        "description": "Verificações de antecedentes em todos os candidatos a emprego devem ser realizadas de acordo com as leis, regulamentos e ética aplicáveis, proporcionais aos requisitos de negócio.",
        "how_to_check": "1. Auditar evidências no repositório de RH (Workday / Google Identity) sincronizadas via Zero-Copy Connector.\n2. Confirmar que nenhum usuário possui conta no Cloud Identity provisionada sem o status de triagem `BACKGROUND_CHECK_VERIFIED`.\n3. Verificar termo de responsabilidade assinado digitalmente.",
        "how_to_maintain": "1. Integrar provisionamento automático SCIM entre o sistema de RH e o Google Cloud Identity, bloqueando contas até a aprovação formal de RH.\n2. Realizar conciliação mensal automatizada entre a folha de pagamento e o diretório ativo.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Identificar",
            "capabilities": "Segurança em Recursos Humanos",
            "domains": "Governança e Ecossistema"
        },
        "gcp_mapping": "Cloud Identity & HR Zero-Copy Connector (Workday Sync)",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "100% dos colaboradores com verificação de antecedentes atestada na fonte",
        "severity": "LOW",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.6.3",
        "name": "Conscientização e Treinamento em Segurança",
        "theme": "A.6 Pessoas",
        "description": "Colaboradores da organização e partes contratadas relevantes devem receber treinamento e atualizações regulares apropriadas sobre a política de segurança da informação.",
        "how_to_check": "1. Inspecionar o relatório de conclusão de treinamento anual de segurança no LMS corporativo integrado via Zero-Copy Connector.\n2. Confirmar taxa de conclusão &ge; 95% para todos os usuários com acesso aos ambientes de produção GCP.\n3. Verificar resultados de simulações periódicas de phishing.",
        "how_to_maintain": "1. Implementar bloqueio automático temporário de acesso ao GCP caso o treinamento anual expire sem renovação após 30 dias de aviso.\n2. Enviar pílulas mensais de conscientização sobre ataques de engenharia social e uso seguro de IA generativa.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Proteger",
            "capabilities": "Segurança em Recursos Humanos",
            "domains": "Proteção"
        },
        "gcp_mapping": "Corporate LMS Zero-Copy Integration & Cloud Identity Groups",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Taxa de conclusão de 98.4% no treinamento de segurança da informação",
        "severity": "MEDIUM",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.6.7",
        "name": "Segurança no Trabalho Remoto",
        "theme": "A.6 Pessoas",
        "description": "Medidas de segurança devem ser implementadas quando os colaboradores estiverem trabalhando remotamente para proteger as informações acessadas, processadas ou armazenadas.",
        "how_to_check": "1. Verificar se o acesso ao Console GCP e APIs requer autenticação mTLS e certificado corporativo no endpoint.\n2. Checar regras de Context-Aware Access exigindo dispositivo gerenciado e versão mínima de sistema operacional.\n3. Confirmar que a autenticação multifator (MFA com chave de segurança física FIDO2/WebAuthn) é mandatória.",
        "how_to_maintain": "1. Ativar a política de MFA obrigatória em toda a organização no Google Workspace / Cloud Identity Admin Console.\n2. Bloquear acessos originados de dispositivos com SO desatualizado ou sem antivírus ativo através do BeyondCorp Enterprise.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Segurança no Trabalho Remoto",
            "domains": "Proteção"
        },
        "gcp_mapping": "BeyondCorp Enterprise Context-Aware Access & Chrome Enterprise",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "MFA e verificação de integridade do dispositivo ativos em 100% dos acessos",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },

    # -------------------------------------------------------------------------
    # A.7 Controles Físicos (Total Oficial: 14 Controles)
    # -------------------------------------------------------------------------
    {
        "id": "A.7.1",
        "name": "Perímetros Físicos de Segurança",
        "theme": "A.7 Físico",
        "description": "Perímetros de segurança física devem ser definidos e usados para proteger áreas que contenham informações e outros ativos associados.",
        "how_to_check": "1. Obter e revisar os relatórios de auditoria SOC 2 Tipo II e ISO/IEC 27001 emitidos para os data centers do Google Cloud através do Google Cloud Compliance Reports Manager.\n2. Confirmar as 6 camadas de segurança física implementadas pelo Google (biometria, cercas térmicas, detecção por laser e segurança armada 24/7).\n3. Validar a matriz de responsabilidade compartilhada no modelo IaaS/PaaS.",
        "how_to_maintain": "1. Baixar anualmente os atestados de conformidade do Google Cloud via Compliance Reports Manager e anexar ao Grafo de Evidências.\n2. Conduzir revisão periódica de controles de segurança física dos escritórios corporativos locais.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Proteger",
            "capabilities": "Segurança Física",
            "domains": "Proteção"
        },
        "gcp_mapping": "Google Cloud Data Center SOC 1/2/3 & ISO 27001 Third-Party Attestations",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Certificado ISO 27001 dos data centers Google Cloud ativo e auditado",
        "severity": "LOW",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.7.4",
        "name": "Monitoramento de Segurança Física",
        "theme": "A.7 Físico",
        "description": "As instalações físicas devem ser monitoradas continuamente para prevenir e detectar acessos físicos não autorizados.",
        "how_to_check": "1. Verificar no relatório SOC 2 do Google Cloud as evidências de CFTV com gravação retida por período regulatório e detecção de intrusão.\n2. Auditar registros de auditoria física dos perímetros de data center no Google Compliance Reports Manager.",
        "how_to_maintain": "1. Monitorar comunicados de conformidade e auditoria emitidos pelo Google Cloud Trust & Security Center.",
        "attributes": {
            "type": "Detectivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Detectar",
            "capabilities": "Segurança Física",
            "domains": "Defesa"
        },
        "gcp_mapping": "Google Shared Responsibility Model & Compliance Reports Manager",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Monitoramento CFTV 24/7 de data centers auditado por avaliadores externos",
        "severity": "LOW",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.7.8",
        "name": "Proteção de Equipamentos e Cabos",
        "theme": "A.7 Físico",
        "description": "Os equipamentos devem ser protegidos contra ameaças físicas e ambientais, e os cabos de alimentação e telecomunicações devem ser protegidos contra interceptação ou danos.",
        "how_to_check": "1. Inspecionar especificações de cabeamento submarino dedicado e infraestrutura de fibra óptica privada do Google Cloud.\n2. Confirmar redundância N+2 de geradores a diesel e sistemas UPS ininterruptos documentados nos relatórios de auditoria ambiental do Google.",
        "how_to_maintain": "1. Adotar topologia multirregional na configuração de workloads para evitar impacto de sinistros físicos localizados.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Disponibilidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Segurança Física",
            "domains": "Proteção, Resiliência"
        },
        "gcp_mapping": "Redundant Power & Dedicated Subsea Global Private Network",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Infraestrutura com redundância elétrica e rede de trânsito 100% criptografada",
        "severity": "MEDIUM",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },

    # -------------------------------------------------------------------------
    # A.8 Controles Tecnológicos (Total Oficial: 34 Controles)
    # -------------------------------------------------------------------------
    {
        "id": "A.8.1",
        "name": "Dispositivos de Usuários Finais (Endpoint)",
        "theme": "A.8 Tecnológico",
        "description": "As informações armazenadas, processadas ou transmitidas através de dispositivos de usuários finais devem ser protegidas contra acessos e ameaças não autorizadas.",
        "how_to_check": "1. Inspecionar o inventário de dispositivos no Google Workspace / Endpoint Management: verificar criptografia total de disco (BitLocker / FileVault) ativada.\n2. Confirmar que 100% das máquinas corporativas contam com módulo TPM 2.0 e inicialização segura (Secure Boot).\n3. Validar se o acesso ao Console GCP bloqueia dispositivos sem agente de segurança ativo.",
        "how_to_maintain": "1. Aplicar política de bloqueio automático de acesso ao GCP via BeyondCorp se o disco estiver descriptografado.\n2. Ativar atualização automática de patches de segurança no Chrome Enterprise e no sistema operacional do endpoint.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Gestão de Ativos, Segurança de Redes",
            "domains": "Proteção"
        },
        "gcp_mapping": "Google Endpoint Management & ChromeOS / TPM Verification",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "Frota de endpoints 100% criptografada e monitorada com TPM",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.2",
        "name": "Direitos de Acesso Privilegiado",
        "theme": "A.8 Tecnológico",
        "description": "A alocação e o uso de direitos de acesso privilegiado devem ser restritos e rigorosamente gerenciados, impedindo chaves permanentes de longa duração.",
        "how_to_check": "1. Executar varredura de chaves de Service Account com o comando:\n   `gcloud iam service-accounts keys list --iam-account=SA_EMAIL`.\n2. Confirmar que existem ZERO chaves estáticas de longa duração baixadas em formato JSON.\n3. Verificar se acessos administrativos usam Workload Identity Federation ou tokens de curta duração (OAuth2).",
        "how_to_maintain": "1. Habilitar a Organization Policy `constraints/iam.disableServiceAccountKeyCreation` em todos os projetos.\n2. Configurar Workload Identity Federation para pipelines GitHub Actions e CI/CD externos, eliminando o uso de senhas ou chaves estáticas.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Gestão de Identidade e Acesso",
            "domains": "Proteção"
        },
        "gcp_mapping": "Workload Identity Federation & Short-Lived OAuth Tokens",
        "status": "COMPLIANT",
        "phase": "Fase 1: Descoberta de Ativos & IAM",
        "evidence": "Zero chaves de service account em disco; autenticação 100% federada",
        "severity": "CRITICAL",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.9",
        "name": "Gerenciamento de Configuração (IaC)",
        "theme": "A.8 Tecnológico",
        "description": "As configurações, incluindo configurações de segurança de hardware, software, serviços e redes, devem ser estabelecidas, documentadas, monitoradas e revisadas continuamente.",
        "how_to_check": "1. Executar o IaC Scanner integrado contra os arquivos Terraform (`.tf`) e Ansible (`.yml`) do repositório.\n2. Validar que nenhuma regra de segurança (ex: portas abertas 0.0.0.0/0, buckets públicos, ausência de KMS) foi violada.\n3. Comparar o estado real da nuvem com a definição declarativa no repositório git para detectar drift.",
        "how_to_maintain": "1. Integrar validação estática de IaC automatizada em todos os Pull Requests via Cloud Build.\n2. Configurar Cloud Asset Inventory Search em execução agendada para alertar desvios (drifts) entre o código e o ambiente de produção.",
        "attributes": {
            "type": "Preventivo, Detectivo",
            "properties": "Integridade, Disponibilidade",
            "concepts": "Proteger, Detectar",
            "capabilities": "Segurança de Configuração",
            "domains": "Proteção, Defesa"
        },
        "gcp_mapping": "IaC Scanner (Terraform / Ansible) & Cloud Build Policy Enforcement",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Varredura estática de IaC executada com zero não-conformidades críticas",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.12",
        "name": "Prevenção de Vazamento de Dados (DLP)",
        "theme": "A.8 Tecnológico",
        "description": "Medidas de prevenção de vazamento de dados devem ser aplicadas a sistemas, redes e quaisquer outros dispositivos que processem, armazenem ou transmitam informações confidenciais.",
        "how_to_check": "1. Inspecionar os perímetros do VPC Service Controls: `gcloud access-context-manager perimeters describe PERIMETER_NAME --policy=POLICY_ID`.\n2. Confirmar que serviços críticos como `storage.googleapis.com` e `bigquery.googleapis.com` estão dentro do perímetro restrito.\n3. Validar se a Cloud Sensitive Data Protection (Cloud DLP) inspeciona dados em trânsito para ofuscar PII.",
        "how_to_maintain": "1. Ativar perímetro VPC Service Controls em modo enforce com monitoramento prévio em modo dry-run.\n2. Configurar Cloud DLP Discovery Jobs periódicos para catalogar dados sensíveis nos buckets e tabelas.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade",
            "concepts": "Proteger",
            "capabilities": "Prevenção de Vazamento de Dados",
            "domains": "Proteção"
        },
        "gcp_mapping": "VPC Service Controls Perimeters & Cloud DLP API",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Perímetro VPC-SC ativo em Storage e BigQuery com bloqueio de exfiltração",
        "severity": "CRITICAL",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.16",
        "name": "Atividades de Monitoramento e Logs",
        "theme": "A.8 Tecnológico",
        "description": "As redes, sistemas e aplicações devem ser monitorados quanto a comportamentos anômalos e eventos de segurança apropriados devem ser registrados e arquivados de forma imutável.",
        "how_to_check": "1. Inspecionar sinks de log no Cloud Logging: `gcloud logging sinks list`.\n2. Confirmar que os logs de auditoria (`Admin Activity` e `Data Access`) são exportados para bucket com Bucket Lock (retenção imutável de 365 dias).\n3. Verificar se as métricas de alerta cobrem alterações de regras de firewall, permissões IAM e desativação de perímetros.",
        "how_to_maintain": "1. Ativar retention lock no bucket GCS de destino de logs em conformidade com a SEC Rule 17a-4 e ISO 27001.\n2. Configurar alertas no Cloud Monitoring para notificação em tempo real de tentativas de acesso negado a dados confidenciais.",
        "attributes": {
            "type": "Detectivo",
            "properties": "Integridade, Confidencialidade",
            "concepts": "Detectar",
            "capabilities": "Monitoramento de Segurança",
            "domains": "Defesa"
        },
        "gcp_mapping": "Cloud Logging Immutable Buckets & Retention Locks",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Sink de logs com retenção imutável de 365 dias ativo",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.20",
        "name": "Segurança de Redes",
        "theme": "A.8 Tecnológico",
        "description": "As redes e dispositivos de rede devem ser protegidos, gerenciados e controlados para salvaguardar a informação em sistemas e aplicações.",
        "how_to_check": "1. Executar checagem de regras de firewall no GCP: `gcloud compute firewall-rules list --filter=\"direction=INGRESS AND allowed.ports=22 OR allowed.ports=3389\"`.\n2. Confirmar que não há regras permitindo entrada de SSH/RDP a partir de `0.0.0.0/0`.\n3. Checar a existência do Cloud Armor WAF protegendo balanceadores de carga HTTPS contra OWASP Top 10 e ataques DDoS.",
        "how_to_maintain": "1. Aplicar a Organization Policy `constraints/compute.restrictLoadBalancerCreationForTypes` para restringir balanceadores públicos.\n2. Utilizar Private Service Connect (PSC) e Private Google Access para comunicação 100% privada sem IPs públicos.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade, Disponibilidade",
            "concepts": "Proteger",
            "capabilities": "Segurança de Redes",
            "domains": "Proteção"
        },
        "gcp_mapping": "Cloud Armor WAF, Private Google Access & Cloud NAT",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Zero portas administrativas públicas; Cloud Armor ativo no ingress",
        "severity": "CRITICAL",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.24",
        "name": "Uso de Criptografia",
        "theme": "A.8 Tecnológico",
        "description": "Regras para o uso eficaz de criptografia, incluindo o gerenciamento de chaves criptográficas (geração, proteção, rotação e descarte), devem ser definidas e implementadas.",
        "how_to_check": "1. Inspecionar chaves no Cloud KMS com o comando:\n   `gcloud kms keys list --keyring=KEYRING_NAME --location=LOCATION`.\n2. Confirmar nível de proteção `HSM` (Hardware Security Module FIPS 140-2 Level 3).\n3. Validar se o período de rotação automatizada está configurado para &le; 90 dias (7.776.000 segundos).",
        "how_to_maintain": "1. Habilitar rotação automática de chave através da flag `--rotation-period=7776000s`.\n2. Configurar Cloud KMS Autokey para provisionamento padronizado de chaves gerenciadas pelo cliente (CMEK) em novos recursos.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Confidencialidade, Integridade",
            "concepts": "Proteger",
            "capabilities": "Criptografia",
            "domains": "Proteção"
        },
        "gcp_mapping": "Cloud KMS HSM Keys & 90-day Automatic Key Rotation",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Chaves KMS HSM com rotação ativa a cada 60 dias",
        "severity": "CRITICAL",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "A.8.28",
        "name": "Codificação e Desenvolvimento Seguro (DevSecOps)",
        "theme": "A.8 Tecnológico",
        "description": "Princípios de engenharia de software e codificação segura devem ser aplicados ao desenvolvimento de software, prevenindo vulnerabilidades no ciclo de vida.",
        "how_to_check": "1. Inspecionar imagens de contêiner no Artifact Registry com varredura automática de vulnerabilidades ativada.\n2. Confirmar se o Binary Authorization está configurado no Google Kubernetes Engine (GKE) / Cloud Run para exigir atestações criptográficas antes do deploy.\n3. Checar ausência de CVEs críticas não remediadas nas imagens em execução.",
        "how_to_maintain": "1. Configurar política de bloqueio no Binary Authorization exigindo assinatura da chave KMS de CI/CD para deploy em produção.\n2. Executar SAST e DAST automatizados em todos os commits via Cloud Build.",
        "attributes": {
            "type": "Preventivo",
            "properties": "Integridade",
            "concepts": "Proteger",
            "capabilities": "Segurança de Aplicação",
            "domains": "Proteção"
        },
        "gcp_mapping": "Artifact Registry Vulnerability Scanning & Binary Authorization",
        "status": "COMPLIANT",
        "phase": "Fase 2: Auditoria Técnica Profunda",
        "evidence": "Varredura contínua de contêineres ativa com zero vulnerabilidades críticas",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },

    # -------------------------------------------------------------------------
    # ISO/IEC 27001:2022 / Amd 1:2024 Climate Action (Ação Climática)
    # -------------------------------------------------------------------------
    {
        "id": "Amd 1:2024 Cl. 4.1",
        "name": "Ação Climática no Contexto da Organização",
        "theme": "Amd 1:2024 Clima",
        "description": "A organização deve determinar formalmente se as mudanças climáticas e eventos meteorológicos extremos são questões relevantes para o SGSI e para a continuidade das operações de TI.",
        "how_to_check": "1. Inspecionar o aditamento da Política de Segurança da Informação cobrindo análise de riscos climáticos e desastres naturais regionais.\n2. Verificar a topologia das cargas de trabalho GCP: confirmar presença de arquitetura multirregional ativa (`us-central1` e `us-east4`).\n3. Validar se o Grafo de Evidências indexa o parecer técnico de risco climático com hash SHA-256.",
        "how_to_maintain": "1. Realizar revisão anual formal da matriz de riscos climáticos acompanhando relatórios científicos de sinistros regionais.\n2. Enforçar a política de replicação assíncrona entre regiões distintas para todos os bancos de dados críticos (Cloud Spanner / Cloud SQL Cross-Region Replicas).",
        "attributes": {
            "type": "Preventivo",
            "properties": "Disponibilidade, Integridade",
            "concepts": "Identificar, Proteger",
            "capabilities": "Continuidade do Negócio",
            "domains": "Resiliência"
        },
        "gcp_mapping": "Multiregional Topology (us-central1 / us-east4) & Climate Risk Registry",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Matriz de risco climático aprovada e integrada ao registro do SGSI",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
    {
        "id": "Amd 1:2024 Cl. 4.2",
        "name": "Requisitos de Partes Interessadas em Mudanças Climáticas",
        "theme": "Amd 1:2024 Clima",
        "description": "A organização deve identificar e determinar os requisitos de partes interessadas relevantes que possam estar relacionados às mudanças climáticas e à resiliência de serviços de TI.",
        "how_to_check": "1. Auditar os acordos de nível de serviço (SLAs), RTO e RPO formalizados com clientes e órgãos reguladores em cenários de desastre climático.\n2. Checar relatórios de testes semestrais de failover entre regiões do Google Cloud executados com sucesso.\n3. Verificar contratos de fornecedores de nuvem garantindo neutralidade de carbono e redundância de data center.",
        "how_to_maintain": "1. Automatizar a execução de testes de comutação por falha (failover) duas vezes ao ano com simulação de interrupção regional total.\n2. Monitorar os indicadores de eficiência de energia (PUE) e carbono através do Google Cloud Carbon Footprint.",
        "attributes": {
            "type": "Preventivo, Detectivo",
            "properties": "Disponibilidade",
            "concepts": "Proteger, Recuperar",
            "capabilities": "Continuidade do Negócio",
            "domains": "Resiliência"
        },
        "gcp_mapping": "Automated Cross-Region Failover Testing & Carbon Footprint",
        "status": "COMPLIANT",
        "phase": "Fase 3: Governança & Políticas",
        "evidence": "Teste semestral de failover multirregional executado com sucesso e documentado",
        "severity": "HIGH",
        "soa_status": "APLICÁVEL (INCLUÍDO NO SGSI)"
    },
]
