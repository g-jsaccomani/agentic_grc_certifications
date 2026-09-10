"""Multilingual Questionnaire Catalog with Comprehensive Assessment Questions and Evidence Guidance.
Provides detailed question formulation, regulatory descriptions, and evidence checklists
for all 93 ISO/IEC 27001:2022 Annex A controls and SOC 2 Trust Services Criteria across PT, EN, and ES.
"""

from typing import Any, Dict, List, Optional

# Themes Metadata localized
THEMES_I18N = {   'A.5': {   'en': {   'short': 'A.5 Organizational',
                         'subtitle': 'Policies, governance, roles, segregation of duties, asset management, and '
                                     'suppliers',
                         'title': 'A.5 — Organizational Controls'},
               'es': {   'short': 'A.5 Organizacional',
                         'subtitle': 'Políticas, gobernanza, roles, segregación de funciones, gestión de activos y '
                                     'proveedores',
                         'title': 'A.5 — Controles Organizacionales'},
               'pt': {   'short': 'A.5 Organizacional',
                         'subtitle': 'Políticas, governança, papéis, segregação de funções, gestão de ativos e '
                                     'fornecedores',
                         'title': 'A.5 — Controles Organizacionais'}},
    'A.6': {   'en': {   'short': 'A.6 People',
                         'subtitle': 'Screening, terms and conditions of employment, awareness, and disciplinary '
                                     'process',
                         'title': 'A.6 — People Controls'},
               'es': {   'short': 'A.6 Personas',
                         'subtitle': 'Selección, términos de contratación, concienciación y desvinculación laboral',
                         'title': 'A.6 — Controles de Personas'},
               'pt': {   'short': 'A.6 Pessoas',
                         'subtitle': 'Seleção, termos de contratação, conscientização e desligamento de colaboradores',
                         'title': 'A.6 — Controles de Pessoas'}},
    'A.7': {   'en': {   'short': 'A.7 Physical',
                         'subtitle': 'Physical security perimeters, environmental protection, and secure media '
                                     'disposal',
                         'title': 'A.7 — Physical Controls'},
               'es': {   'short': 'A.7 Físico',
                         'subtitle': 'Perímetros de seguridad física, protección ambiental y destrucción segura de '
                                     'soportes',
                         'title': 'A.7 — Controles Físicos'},
               'pt': {   'short': 'A.7 Físico',
                         'subtitle': 'Perímetros de segurança, proteção contra desastres físicos e descarte seguro de '
                                     'mídias',
                         'title': 'A.7 — Controles Físicos'}},
    'A.8': {   'en': {   'short': 'A.8 Technological',
                         'subtitle': 'IAM access control, Cloud KMS encryption, VPC protection, logging, and DevSecOps',
                         'title': 'A.8 — Technological Controls'},
               'es': {   'short': 'A.8 Tecnológico',
                         'subtitle': 'Control de acceso IAM, cifrado Cloud KMS, protección VPC, registros y desarrollo '
                                     'seguro',
                         'title': 'A.8 — Controles Tecnológicos'},
               'pt': {   'short': 'A.8 Tecnológico',
                         'subtitle': 'Controle de acesso IAM, criptografia Cloud KMS, proteção VPC, logs e '
                                     'desenvolvimento seguro',
                         'title': 'A.8 — Controles Tecnológicos'}},
    'SOC2_CC': {   'en': {   'short': 'SOC 2 Security',
                             'subtitle': 'Logical access controls, perimeter protection, vulnerability monitoring, and '
                                         'incident response',
                             'title': 'SOC 2 — Trust Services Security Criteria (Common Criteria)'},
                   'es': {   'short': 'SOC 2 Seguridad',
                             'subtitle': 'Controles de acceso lógico, protección perimetral, monitoreo de '
                                         'vulnerabilidades y respuesta a incidentes',
                             'title': 'SOC 2 — Criterios de Seguridad (Common Criteria)'},
                   'pt': {   'short': 'SOC 2 Segurança',
                             'subtitle': 'Controles de acesso lógico, proteção perimetral, monitoramento de '
                                         'vulnerabilidades e resposta a incidentes',
                             'title': 'SOC 2 — Critérios de Segurança (Common Criteria)'}}}

# All 93 ISO/IEC 27001:2022 Annex A Controls with Full Multilingual Specifications
ISO_27001_QUESTIONNAIRE_CATALOG = [   {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Resource Manager Organization Policies & Zero-Copy Drive',
        'how_to_check': '1. Inspecionar repositório de políticas corporativas sincronizado via Zero-Copy (Google Drive).\n'
                        '2. Checar Organization Policies ativas via: `gcloud resource-manager org-policies list`.\n'
                        '3. Validar assinaturas e carimbo temporal de aprovação da diretoria.',
        'how_to_maintain': '1. Revisão semestral automatizada com alertas via Cloud Scheduler.\n'
                           '2. Enforçar restrições hierárquicas no nível da organização do GCP.\n'
                           '3. Bloquear alterações de políticas sem revisão obrigatória de Code Owners.',
        'id': 'A.5.1',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.1): Ensure that '
                                                     'information security policies are formally approved by executive '
                                                     'management, communicated to all personnel, and reviewed at '
                                                     'planned intervals of at least 12 months.',
                                      'name': 'Policies for information security',
                                      'question': 'Does the organization ensure that information security policies are '
                                                  'formally approved by executive management, communicated to all '
                                                  'personnel, and reviewed at planned intervals of at least 12 months?',
                                      'recommended_evidence': '• Information Security Policy (ISMS) formally approved '
                                                              'and signed by Executive Leadership.\n'
                                                              '• Security Committee meeting minutes and annual policy '
                                                              'review records.\n'
                                                              '• Active GCP Organization Policies export (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '• Employee policy acknowledgment and sign-off records.',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.1): Asegurar que '
                                                     'las políticas de seguridad de la información sean formalmente '
                                                     'aprobadas por la alta dirección, comunicadas al personal y '
                                                     'revisadas periódicamente al menos cada 12 meses.',
                                      'name': 'Políticas para la seguridad de la información',
                                      'question': '¿Garantiza la organización que las políticas de seguridad de la '
                                                  'información sean formalmente aprobadas por la alta dirección, '
                                                  'comunicadas al personal y revisadas periódicamente al menos cada 12 '
                                                  'meses?',
                                      'recommended_evidence': '• Política General de Seguridad de la Información '
                                                              '(SGSI) aprobada formalmente por la Dirección.\n'
                                                              '• Actas de reuniones periódicas del Comité de Seguridad '
                                                              'de la Información.\n'
                                                              '• Exportación de Organization Policies activas en GCP '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '• Registros de acuse de recibo y aceptación por parte '
                                                              'del personal.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.1): '
                                                     'Assegurar que as políticas de segurança da informação sejam '
                                                     'formalmente aprovadas pela direção, comunicadas aos '
                                                     'colaboradores e revisadas periodicamente a cada 12 meses.',
                                      'name': 'Políticas para segurança da informação',
                                      'question': 'A organização garante que as políticas de segurança da informação '
                                                  'sejam formalmente aprovadas pela direção, comunicadas aos '
                                                  'colaboradores e revisadas periodicamente a cada 12 meses?',
                                      'recommended_evidence': '• Política Geral de Segurança da Informação (SGSI) '
                                                              'formalmente aprovada pela Diretoria Executiva.\n'
                                                              '• Atas de reunião periódica do Comitê de Segurança da '
                                                              'Informação.\n'
                                                              '• Exportação de Organization Policies ativas no GCP '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '• Registros de ciência e aceite dos colaboradores nos '
                                                              'canais corporativos.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud IAM Roles & Cloud Identity Groups',
        'how_to_check': '1. Inspecionar atribuições de papéis IAM no GCP via: `gcloud projects get-iam-policy '
                        'PROJECT_ID`.\n'
                        '2. Verificar segregação de Security Admin, Network Admin e Reviewer.\n'
                        '3. Checar vínculo de papéis corporativos em grupos do Google Workspace.',
        'how_to_maintain': '1. Manter RBAC centralizado em grupos do Cloud Identity/Workspace, proibindo concessão '
                           'direta a usuários individuais.\n'
                           '2. Executar revisão de privilégios com IAM Recommender mensalmente.',
        'id': 'A.5.2',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.2): Ensure that all '
                                                     'information security roles and responsibilities are formally '
                                                     'assigned, documented, and communicated throughout the '
                                                     'organization.',
                                      'name': 'Information security roles and responsibilities',
                                      'question': 'Does the organization ensure that all information security roles '
                                                  'and responsibilities are formally assigned, documented, and '
                                                  'communicated throughout the organization?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.2): Asegurar que '
                                                     'todos los roles y responsabilidades de seguridad de la '
                                                     'información estén formalmente asignados, documentados y '
                                                     'comunicados.',
                                      'name': 'Roles y responsabilidades en seguridad de la información',
                                      'question': '¿Garantiza la organización que todos los roles y responsabilidades '
                                                  'de seguridad de la información estén formalmente asignados, '
                                                  'documentados y comunicados?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.2): '
                                                     'Assegurar que todos os papéis e responsabilidades de segurança '
                                                     'da informação estejam formalmente atribuídos, documentados e '
                                                     'comunicados.',
                                      'name': 'Papéis e responsabilidades na segurança da informação',
                                      'question': 'A organização garante que todos os papéis e responsabilidades de '
                                                  'segurança da informação estejam formalmente atribuídos, '
                                                  'documentados e comunicados?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Proteger',
                          'domains': 'Defesa',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Privileged Access Manager (PAM) & IAM Conditions',
        'how_to_check': '1. Validar que contas de serviço de CI/CD não possuem permissão de aprovação de PR e deploy '
                        'em prod simultaneamente.\n'
                        '2. Checar se papéis de `roles/owner` foram substituídos por papéis granulares de menor '
                        'privilégio.',
        'how_to_maintain': '1. Enforçar aprovações duplas (Four-Eyes Principle) para merges em branches principais e '
                           'alterações de infraestrutura.\n'
                           '2. Utilizar Privileged Access Manager (PAM) para acessos pontuais e temporários.',
        'id': 'A.5.3',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.3): Ensure that '
                                                     'conflicting duties and conflicting areas of responsibility are '
                                                     'segregated to reduce unauthorized modification or fraud '
                                                     'opportunities.',
                                      'name': 'Segregation of duties',
                                      'question': 'Does the organization ensure that conflicting duties and '
                                                  'conflicting areas of responsibility are segregated to reduce '
                                                  'unauthorized modification or fraud opportunities?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.3): Asegurar que '
                                                     'las funciones y áreas de responsabilidad en conflicto estén '
                                                     'segregadas para reducir el riesgo de fraude o modificaciones no '
                                                     'autorizadas.',
                                      'name': 'Segregación de funciones',
                                      'question': '¿Garantiza la organización que las funciones y áreas de '
                                                  'responsabilidad en conflicto estén segregadas para reducir el '
                                                  'riesgo de fraude o modificaciones no autorizadas?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.3): '
                                                     'Assegurar que funções conflitantes e áreas de responsabilidade '
                                                     'conflitantes sejam segregadas para reduzir oportunidades de '
                                                     'modificação não autorizada ou fraude.',
                                      'name': 'Segregação de funções',
                                      'question': 'A organização garante que funções conflitantes e áreas de '
                                                  'responsabilidade conflitantes sejam segregadas para reduzir '
                                                  'oportunidades de modificação não autorizada ou fraude?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Executive GRC Dashboard & Security Scorecards',
        'how_to_check': '1. Verificar atas de reunião de gestão e relatórios de conformidade assinados pela '
                        'liderança.\n'
                        '2. Inspecionar trilhas de aprovação executiva no canal de GRC.',
        'how_to_maintain': '1. Estabelecer revisões trimestrais obrigatórias da postura de segurança entre CISO e '
                           'gestores de engenharia.\n'
                           '2. Integrar metas de segurança (SLOs) no plano de desempenho das equipes.',
        'id': 'A.5.4',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.4): Ensure that '
                                                     'management requires and verifies that all personnel and '
                                                     'contractors apply information security in accordance with '
                                                     'established policies.',
                                      'name': 'Management responsibilities',
                                      'question': 'Does the organization ensure that management requires and verifies '
                                                  'that all personnel and contractors apply information security in '
                                                  'accordance with established policies?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.4): Asegurar que '
                                                     'la dirección exija y verifique que todo el personal y '
                                                     'contratistas apliquen la seguridad de la información conforme a '
                                                     'las políticas establecidas.',
                                      'name': 'Responsabilidades de la dirección',
                                      'question': '¿Garantiza la organización que la dirección exija y verifique que '
                                                  'todo el personal y contratistas apliquen la seguridad de la '
                                                  'información conforme a las políticas establecidas?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.4): '
                                                     'Assegurar que a liderança exija e verifique que todos os '
                                                     'colaboradores e contratados apliquem a segurança da informação '
                                                     'de acordo com as políticas estabelecidas.',
                                      'name': 'Responsabilidades da direção',
                                      'question': 'A organização garante que a liderança exija e verifique que todos '
                                                  'os colaboradores e contratados apliquem a segurança da informação '
                                                  'de acordo com as políticas estabelecidas?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Resposta a Incidentes',
                          'concepts': 'Responder',
                          'domains': 'Defesa',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo, Corretivo'},
        'gcp_mapping': 'Incident Response Registry & Regulatory Contact Matrix',
        'how_to_check': '1. Checar registro de contatos de autoridades (ANPD, CERT.br, órgãos reguladores do setor) '
                        'documentado e atualizado.\n'
                        '2. Verificar procedimento formal de notificação de incidentes graves.',
        'how_to_maintain': '1. Revisar anualmente a lista de contatos de emergência e canais de notificação '
                           'regulatória.\n'
                           '2. Conduzir simulados de notificação de incidente com assessoria jurídica.',
        'id': 'A.5.5',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.5): Ensure that the '
                                                     'organization maintains appropriate contacts with relevant '
                                                     'authorities, regulatory bodies, and law enforcement agencies.',
                                      'name': 'Contact with authorities',
                                      'question': 'Does the organization ensure that the organization maintains '
                                                  'appropriate contacts with relevant authorities, regulatory bodies, '
                                                  'and law enforcement agencies?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.5): Asegurar que '
                                                     'la organización mantenga contactos apropiados con las '
                                                     'autoridades pertinentes, entidades reguladoras y fuerzas del '
                                                     'orden.',
                                      'name': 'Contacto con las autoridades',
                                      'question': '¿Garantiza la organización que la organización mantenga contactos '
                                                  'apropiados con las autoridades pertinentes, entidades reguladoras y '
                                                  'fuerzas del orden?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.5): '
                                                     'Assegurar que a organização mantenha canais e contatos '
                                                     'apropriados com autoridades relevantes, órgãos reguladores e '
                                                     'agências de aplicação da lei.',
                                      'name': 'Contato com autoridades',
                                      'question': 'A organização garante que a organização mantenha canais e contatos '
                                                  'apropriados com autoridades relevantes, órgãos reguladores e '
                                                  'agências de aplicação da lei?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Inteligência de Ameaças',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Threat Intelligence Communities & CSA Matrix',
        'how_to_check': '1. Verificar afiliações a fóruns de cibersegurança (FIRST, ISACA, Cloud Security Alliance, '
                        'OWASP).\n'
                        '2. Validar compartilhamento de inteligência e alertas de segurança recebidos.',
        'how_to_maintain': '1. Participação ativa em fóruns de segurança e grupos de interesse setoriais.\n'
                           '2. Incorporação contínua de boas práticas nos padrões de arquitetura em nuvem.',
        'id': 'A.5.6',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.6): Ensure that the '
                                                     'organization maintains contacts with professional associations, '
                                                     'cybersecurity forums, and specialized interest groups.',
                                      'name': 'Contact with special interest groups',
                                      'question': 'Does the organization ensure that the organization maintains '
                                                  'contacts with professional associations, cybersecurity forums, and '
                                                  'specialized interest groups?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.6): Asegurar que '
                                                     'la organización mantenga contacto con asociaciones '
                                                     'profesionales, foros de seguridad y grupos de interés '
                                                     'especializado.',
                                      'name': 'Contacto con grupos de interés especial',
                                      'question': '¿Garantiza la organización que la organización mantenga contacto '
                                                  'con asociaciones profesionales, foros de seguridad y grupos de '
                                                  'interés especializado?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.6): '
                                                     'Assegurar que a organização mantenha contato com associações '
                                                     'profissionais, fóruns de segurança e grupos de interesse '
                                                     'especializado em cibersegurança.',
                                      'name': 'Contato com grupos de interesse especial',
                                      'question': 'A organização garante que a organização mantenha contato com '
                                                  'associações profissionais, fóruns de segurança e grupos de '
                                                  'interesse especializado em cibersegurança?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Inteligência de Ameaças',
                          'concepts': 'Identificar, Detectar',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo, Preventivo'},
        'gcp_mapping': 'Security Command Center Enterprise & Mandiant Threat Intelligence',
        'how_to_check': '1. Verificar feeds de Threat Intelligence integrados ao Google Cloud Security Command Center '
                        '(SCC) Enterprise.\n'
                        '2. Inspecionar regras ativas do Mandiant Threat Intelligence.\n'
                        '3. Validar se indicadores de comprometimento (IoCs) são correlacionados com logs do Cloud '
                        'Logging.',
        'how_to_maintain': '1. Automatizar ingestão de feeds STIX/TAXII e alertas do Google Threat Intelligence.\n'
                           '2. Executar buscas proativas de caça a ameaças (Threat Hunting) com base em relatórios '
                           'Mandiant.',
        'id': 'A.5.7',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.7): Ensure that '
                                                     'information relating to information security threats is '
                                                     'collected, consolidated, and analyzed to produce actionable '
                                                     'threat intelligence.',
                                      'name': 'Threat intelligence',
                                      'question': 'Does the organization ensure that information relating to '
                                                  'information security threats is collected, consolidated, and '
                                                  'analyzed to produce actionable threat intelligence?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.7): Asegurar que '
                                                     'la información sobre amenazas a la seguridad de la información '
                                                     'sea recopilada, consolidada y analizada para generar '
                                                     'inteligencia procesable.',
                                      'name': 'Inteligencia sobre amenazas',
                                      'question': '¿Garantiza la organización que la información sobre amenazas a la '
                                                  'seguridad de la información sea recopilada, consolidada y analizada '
                                                  'para generar inteligencia procesable?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.7): '
                                                     'Assegurar que informações sobre ameaças à segurança da '
                                                     'informação sejam coletadas, consolidadas e analisadas para gerar '
                                                     'inteligência acionável.',
                                      'name': 'Inteligência sobre ameaças',
                                      'question': 'A organização garante que informações sobre ameaças à segurança da '
                                                  'informação sejam coletadas, consolidadas e analisadas para gerar '
                                                  'inteligência acionável?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar, Proteger',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Enterprise Landing Zone Architecture & Cloud Build Gates',
        'how_to_check': '1. Inspecionar se novos projetos no GCP passam por gate de revisão de arquitetura de segurança '
                        'antes do provisionamento.\n'
                        '2. Validar questionário de segurança e modelo de ameaças (Threat Model) em projetos críticos.',
        'how_to_maintain': '1. Integrar checklist automatizado de segurança em templates do Jira e Cloud Build.\n'
                           '2. Bloquear criação de novos projetos fora da hierarquia padrão de Landing Zone.',
        'id': 'A.5.8',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.8): Ensure that '
                                                     'information security is integrated into project management '
                                                     'methodology regardless of the project type.',
                                      'name': 'Information security in project management',
                                      'question': 'Does the organization ensure that information security is '
                                                  'integrated into project management methodology regardless of the '
                                                  'project type?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.8): Asegurar que '
                                                     'la seguridad de la información se integre en la gestión de '
                                                     'proyectos independientemente del tipo de proyecto.',
                                      'name': 'Seguridad de la información en la gestión de proyectos',
                                      'question': '¿Garantiza la organización que la seguridad de la información se '
                                                  'integre en la gestión de proyectos independientemente del tipo de '
                                                  'proyecto?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.8): '
                                                     'Assegurar que a segurança da informação seja integrada no '
                                                     'gerenciamento de projetos independentemente do tipo de projeto.',
                                      'name': 'Segurança da informação no gerenciamento de projetos',
                                      'question': 'A organização garante que a segurança da informação seja integrada '
                                                  'no gerenciamento de projetos independentemente do tipo de projeto?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Gestão de Ativos',
                          'concepts': 'Identificar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Cloud Asset Inventory & Resource Tags Enforce',
        'how_to_check': '1. Executar inventário automático via Cloud Asset Inventory API: `gcloud asset '
                        'search-all-resources --scope=organizations/ORG_ID`.\n'
                        '2. Confirmar se 100% dos recursos possuem rótulos obrigatórios (`owner`, `environment`, '
                        '`data-classification`).',
        'how_to_maintain': '1. Impor política de organização que exige tags e labels em recursos recém-criados.\n'
                           '2. Reconciliar diariamente o grafo de ativos com alertas de recursos órfãos.',
        'id': 'A.5.9',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.9): Ensure that a '
                                                     'complete and up-to-date inventory of information and other '
                                                     'associated assets, including cloud workloads, is maintained.',
                                      'name': 'Inventory of information and other associated assets',
                                      'question': 'Does the organization ensure that a complete and up-to-date '
                                                  'inventory of information and other associated assets, including '
                                                  'cloud workloads, is maintained?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.9): Asegurar que '
                                                     'se mantenga un inventario completo y actualizado de la '
                                                     'información y otros activos asociados, incluidos recursos en la '
                                                     'nube.',
                                      'name': 'Inventario de información y otros activos asociados',
                                      'question': '¿Garantiza la organización que se mantenga un inventario completo y '
                                                  'actualizado de la información y otros activos asociados, incluidos '
                                                  'recursos en la nube?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.9): '
                                                     'Assegurar que um inventário completo e atualizado de informações '
                                                     'e outros ativos associados, incluindo recursos em nuvem, seja '
                                                     'mantido.',
                                      'name': 'Inventário de informações e outros ativos associados',
                                      'question': 'A organização garante que um inventário completo e atualizado de '
                                                  'informações e outros ativos associados, incluindo recursos em '
                                                  'nuvem, seja mantido?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'BeyondCorp Endpoint Verification & Google Workspace Policies',
        'how_to_check': '1. Inspecionar o termo de uso aceitável de ativos assinado por colaboradores e prestadores.\n'
                        '2. Inspecionar regras de bloqueio de navegação e transferência de dados em endpoints BeyondCorp.',
        'how_to_maintain': '1. Revisão e aceite digital periódico do termo de uso no onboarding e anualmente.\n'
                           '2. Monitoramento de desvios através de telemetria de endpoint e Cloud Identity.',
        'id': 'A.5.10',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.10): Ensure that rules '
                                                     'for the acceptable use of information and associated assets are '
                                                     'defined, documented, communicated, and enforced.',
                                      'name': 'Acceptable use of information and other associated assets',
                                      'question': 'Does the organization ensure that rules for the acceptable use of '
                                                  'information and associated assets are defined, documented, '
                                                  'communicated, and enforced?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.10): Asegurar que '
                                                     'se definan, documenten, comuniquen y apliquen normas para el uso '
                                                     'aceptable de la información y activos asociados.',
                                      'name': 'Uso aceptable de la información y otros activos asociados',
                                      'question': '¿Garantiza la organización que se definan, documenten, comuniquen y '
                                                  'apliquen normas para el uso aceptable de la información y activos '
                                                  'asociados?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.10): '
                                                     'Assegurar que regras para o uso aceitável de informações e '
                                                     'ativos associados sejam definidas, documentadas, comunicadas e '
                                                     'aplicadas.',
                                      'name': 'Uso aceitável de informações e outros ativos associados',
                                      'question': 'A organização garante que regras para o uso aceitável de '
                                                  'informações e ativos associados sejam definidas, documentadas, '
                                                  'comunicadas e aplicadas?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Segurança de RH',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud Identity Deprovisioning & MDM Wipe',
        'how_to_check': '1. Inspecionar fluxo de offboarding: verificar devolução de hardware e revogação de licenças '
                        'corporativas em até 24 horas.\n'
                        '2. Validar protocolo de desassociação de certificados e dispositivos corporativos.',
        'how_to_maintain': '1. Automatizar bloqueio de conta e revogação de tokens de acesso via integração HRIS '
                           '(Workday/BambooHR) e Cloud Identity.\n'
                           '2. Manter termo de devolução com assinatura digital.',
        'id': 'A.5.11',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.11): Ensure that all '
                                                     'personnel and external parties return all organizational assets '
                                                     'in their possession upon termination of employment or contract.',
                                      'name': 'Return of assets',
                                      'question': 'Does the organization ensure that all personnel and external '
                                                  'parties return all organizational assets in their possession upon '
                                                  'termination of employment or contract?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.11): Asegurar que '
                                                     'todo el personal y partes externas devuelvan todos los activos '
                                                     'de la organización tras la finalización de su empleo o contrato.',
                                      'name': 'Devolución de activos',
                                      'question': '¿Garantiza la organización que todo el personal y partes externas '
                                                  'devuelvan todos los activos de la organización tras la finalización '
                                                  'de su empleo o contrato?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.11): '
                                                     'Assegurar que todos os colaboradores e partes externas devolvam '
                                                     'todos os ativos da organização após o término de suas atividades '
                                                     'ou contrato.',
                                      'name': 'Devolução de ativos',
                                      'question': 'A organização garante que todos os colaboradores e partes externas '
                                                  'devolvam todos os ativos da organização após o término de suas '
                                                  'atividades ou contrato?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Identificar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Sensitive Data Protection (Cloud DLP) & BigQuery Policy Tags',
        'how_to_check': '1. Inspecionar esquemas de classificação de dados corporativos (Público, Interno, '
                        'Confidencial, Restrito).\n'
                        '2. Executar varredura com Cloud Sensitive Data Protection (DLP) para identificar dados '
                        'PII/financeiros em Cloud Storage e BigQuery.',
        'how_to_maintain': '1. Configurar inspeções periódicas automáticas de DLP com templates de detecção de CPF, '
                           'cartões de crédito e credenciais.\n'
                           '2. Alocar automaticamente tags de classificação aos buckets e datasets.',
        'id': 'A.5.12',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.12): Ensure that '
                                                     'information is classified in accordance with security needs '
                                                     'based on confidentiality, integrity, availability, and '
                                                     'stakeholder requirements.',
                                      'name': 'Classification of information',
                                      'question': 'Does the organization ensure that information is classified in '
                                                  'accordance with security needs based on confidentiality, integrity, '
                                                  'availability, and stakeholder requirements?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.12): Asegurar que '
                                                     'la información se clasifique de acuerdo con las necesidades de '
                                                     'seguridad basadas en confidencialidad, integridad y '
                                                     'disponibilidad.',
                                      'name': 'Clasificación de la información',
                                      'question': '¿Garantiza la organización que la información se clasifique de '
                                                  'acuerdo con las necesidades de seguridad basadas en '
                                                  'confidencialidad, integridad y disponibilidad?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.12): '
                                                     'Assegurar que a informação seja classificada de acordo com as '
                                                     'necessidades de segurança baseadas em confidencialidade, '
                                                     'integridade e disponibilidade.',
                                      'name': 'Classificação da informação',
                                      'question': 'A organização garante que a informação seja classificada de acordo '
                                                  'com as necessidades de segurança baseadas em confidencialidade, '
                                                  'integridade e disponibilidade?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'BigQuery Column-Level Access & Data Catalog',
        'how_to_check': '1. Checar se datasets do BigQuery possuem rótulos de política de dados (Policy Tags) ativos.\n'
                        '2. Validar rótulos em buckets Cloud Storage contendo dados sensíveis.',
        'how_to_maintain': '1. Enforçar controle de acesso fino baseado em colunas no BigQuery utilizando Data Catalog '
                           'Policy Tags.\n'
                           '2. Bloquear criação de recursos de armazenamento sem rótulo de sensibilidade via '
                           'Terraform.',
        'id': 'A.5.13',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.13): Ensure that an '
                                                     'appropriate set of procedures for information labelling is '
                                                     'developed and implemented in accordance with the classification '
                                                     'scheme.',
                                      'name': 'Labelling of information',
                                      'question': 'Does the organization ensure that an appropriate set of procedures '
                                                  'for information labelling is developed and implemented in '
                                                  'accordance with the classification scheme?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.13): Asegurar que '
                                                     'se desarrolle e implemente un conjunto adecuado de '
                                                     'procedimientos para el etiquetado de la información según su '
                                                     'clasificación.',
                                      'name': 'Etiquetado de la información',
                                      'question': '¿Garantiza la organización que se desarrolle e implemente un '
                                                  'conjunto adecuado de procedimientos para el etiquetado de la '
                                                  'información según su clasificación?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.13): '
                                                     'Assegurar que um conjunto apropriado de procedimentos para '
                                                     'rotulagem da informação seja desenvolvido e implementado de '
                                                     'acordo com a classificação.',
                                      'name': 'Rotulagem da informação',
                                      'question': 'A organização garante que um conjunto apropriado de procedimentos '
                                                  'para rotulagem da informação seja desenvolvido e implementado de '
                                                  'acordo com a classificação?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'SSL Policies & VPC Service Controls Egress Rules',
        'how_to_check': '1. Validar que canais de transferência utilizam TLS 1.3 obrigatório e certificados '
                        'gerenciados.\n'
                        '2. Inspecionar se canais de egresso de dados são protegidos por VPC Service Controls para evitar '
                        'exfiltração.',
        'how_to_maintain': '1. Bloquear tráfego HTTP desprotegido em Cloud Load Balancers com SSL Policies modernas '
                           '(MODERN / RESTRICTED).\n'
                           '2. Monitorar fluxos de egresso não autorizados no VPC Flow Logs.',
        'id': 'A.5.14',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.14): Ensure that formal '
                                                     'information transfer rules, procedures, or agreements are in '
                                                     'place for all types of transfer facilities and channels.',
                                      'name': 'Information transfer',
                                      'question': 'Does the organization ensure that formal information transfer '
                                                  'rules, procedures, or agreements are in place for all types of '
                                                  'transfer facilities and channels?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.14): Asegurar que '
                                                     'existan normas, procedimientos o acuerdos formales de '
                                                     'transferencia de información para todo tipo de medios de '
                                                     'comunicación.',
                                      'name': 'Transferencia de información',
                                      'question': '¿Garantiza la organización que existan normas, procedimientos o '
                                                  'acuerdos formales de transferencia de información para todo tipo de '
                                                  'medios de comunicación?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.14): '
                                                     'Assegurar que regras, procedimentos ou acordos formais de '
                                                     'transferência de informações estejam em vigor para todos os '
                                                     'tipos de canais de comunicação.',
                                      'name': 'Transferência de informações',
                                      'question': 'A organização garante que regras, procedimentos ou acordos formais '
                                                  'de transferência de informações estejam em vigor para todos os '
                                                  'tipos de canais de comunicação?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade e Acesso',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud IAM Policy & BeyondCorp Context-Aware Access',
        'how_to_check': '1. Inspecionar política corporativa de controle de acesso (Need-to-Know e Menor Privilégio).\n'
                        '2. Inspecionar se acessos administrativos a instâncias de produção exigem autenticação '
                        'centralizada e aprovada.',
        'how_to_maintain': '1. Impor autenticação context-aware (BeyondCorp) baseada em dispositivo, IP e localização '
                           'geográfica.\n'
                           '2. Revisão trimestral de acessos com IAM Access Review.',
        'id': 'A.5.15',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.15): Ensure that rules '
                                                     'to control physical and logical access to information and other '
                                                     'associated assets are established and enforced based on business '
                                                     'requirements.',
                                      'name': 'Access control',
                                      'question': 'Does the organization ensure that rules to control physical and '
                                                  'logical access to information and other associated assets are '
                                                  'established and enforced based on business requirements?',
                                      'recommended_evidence': '• Access Control Matrix and formal Logical/Physical '
                                                              'Access Control Policy.\n'
                                                              '• GCP IAM policy export showing least-privilege role '
                                                              'assignments (`gcloud projects get-iam-policy`).\n'
                                                              '• Monthly IAM Recommender reports demonstrating review '
                                                              'and reduction of excess privileges.\n'
                                                              '• Just-in-Time privileged access workflows configured '
                                                              'via Privileged Access Manager (PAM).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.15): Asegurar que '
                                                     'se definan y apliquen reglas de control de acceso físico y '
                                                     'lógico basadas en requisitos de negocio y seguridad.',
                                      'name': 'Control de acceso',
                                      'question': '¿Garantiza la organización que se definan y apliquen reglas de '
                                                  'control de acceso físico y lógico basadas en requisitos de negocio '
                                                  'y seguridad?',
                                      'recommended_evidence': '• Matriz de Control de Acceso y Política de Control de '
                                                              'Acceso Lógico y Físico.\n'
                                                              '• Exportación de políticas IAM en GCP (`gcloud projects '
                                                              'get-iam-policy`).\n'
                                                              '• Informes mensuales de IAM Recommender demostrando '
                                                              'revisión de privilegios excesivos.\n'
                                                              '• Flujos de aprobación de acceso temporal configurados '
                                                              'en Privileged Access Manager (PAM).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.15): '
                                                     'Assegurar que regras para controle de acesso lógico e físico '
                                                     'sejam definidas e aplicadas com base nos requisitos de negócio e '
                                                     'de segurança.',
                                      'name': 'Controle de acesso',
                                      'question': 'A organização garante que regras para controle de acesso lógico e '
                                                  'físico sejam definidas e aplicadas com base nos requisitos de '
                                                  'negócio e de segurança?',
                                      'recommended_evidence': '• Matriz de Controle de Acesso e Política de Controle '
                                                              'de Acesso Lógico e Físico.\n'
                                                              '• Exportação de políticas IAM e papéis granulares no '
                                                              'GCP (`gcloud projects get-iam-policy`).\n'
                                                              '• Relatórios mensais do IAM Recommender demonstrando '
                                                              'revisão de privilégios excessivos.\n'
                                                              '• Configuração de aprovação para privilégios '
                                                              'temporários via Privileged Access Manager (PAM).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade e Acesso',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud Identity Lifecycle & GCDS / SCIM',
        'how_to_check': '1. Inspecionar sincronização do Cloud Identity / Google Workspace com o diretório corporativo '
                        '(Active Directory / Okta).\n'
                        '2. Checar tempo médio de desativação de contas inativas (> 90 dias).',
        'how_to_maintain': '1. Integrar provisionamento e desprovisionamento via SCIM / Google Cloud Directory Sync '
                           '(GCDS).\n'
                           '2. Automatizar desativação de credenciais de contas suspensas imediatamente.',
        'id': 'A.5.16',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.16): Ensure that the '
                                                     'full lifecycle of identities is securely managed, from '
                                                     'provisioning, modification, verification, to deprovisioning.',
                                      'name': 'Identity management',
                                      'question': 'Does the organization ensure that the full lifecycle of identities '
                                                  'is securely managed, from provisioning, modification, verification, '
                                                  'to deprovisioning?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.16): Asegurar que '
                                                     'se gestione el ciclo de vida completo de las identidades, desde '
                                                     'la asignación, modificación hasta la revocación.',
                                      'name': 'Gestión de identidades',
                                      'question': '¿Garantiza la organización que se gestione el ciclo de vida '
                                                  'completo de las identidades, desde la asignación, modificación '
                                                  'hasta la revocación?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.16): '
                                                     'Assegurar que o ciclo de vida completo de identidades seja '
                                                     'gerenciado desde a criação, alocação, modificação até a '
                                                     'revogação.',
                                      'name': 'Gestão de identidades',
                                      'question': 'A organização garante que o ciclo de vida completo de identidades '
                                                  'seja gerenciado desde a criação, alocação, modificação até a '
                                                  'revogação?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade e Acesso',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': '2-Step Verification (FIDO2 Keys) & Enforce MFA',
        'how_to_check': '1. Checar se 100% dos usuários corporativos possuem MFA/2FA mandatório com chave física FIDO2 '
                        '(Titan Security Key).\n'
                        '2. Validar proibição de reutilização de senhas e complexidade mínima.',
        'how_to_maintain': '1. Ativar política de organização `constraints/iam.enforceMfa` no Google Cloud.\n'
                           '2. Bloquear uso de métodos fracos de autenticação (SMS, email OTP) em contas '
                           'privilegiadas.',
        'id': 'A.5.17',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.17): Ensure that '
                                                     'allocation and management of authentication information '
                                                     '(passwords, keys, certificates, MFA tokens) are strictly '
                                                     'controlled.',
                                      'name': 'Authentication information',
                                      'question': 'Does the organization ensure that allocation and management of '
                                                  'authentication information (passwords, keys, certificates, MFA '
                                                  'tokens) are strictly controlled?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.17): Asegurar que '
                                                     'la asignación y gestión de información de autenticación '
                                                     '(contraseñas, claves, certificados, tokens MFA) se controlen '
                                                     'rigurosamente.',
                                      'name': 'Información de autenticación',
                                      'question': '¿Garantiza la organización que la asignación y gestión de '
                                                  'información de autenticación (contraseñas, claves, certificados, '
                                                  'tokens MFA) se controlen rigurosamente?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.17): '
                                                     'Assegurar que a alocação e gestão de informações de autenticação '
                                                     '(senhas, chaves, certificados, tokens MFA) sejam rigorosamente '
                                                     'controladas.',
                                      'name': 'Informações de autenticação',
                                      'question': 'A organização garante que a alocação e gestão de informações de '
                                                  'autenticação (senhas, chaves, certificados, tokens MFA) sejam '
                                                  'rigorosamente controladas?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade e Acesso',
                          'concepts': 'Proteger, Detectar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'IAM Recommender & Automated Access Revocation',
        'how_to_check': '1. Inspecionar relatórios de revisão de IAM Recommender para remoção de privilégios não '
                        'utilizados nos últimos 90 dias.\n'
                        '2. Inspecionar permissões excessivas atribuídas a Service Accounts.',
        'how_to_maintain': '1. Automatizar aceitação de recomendações do IAM Recommender via Cloud Functions.\n'
                           '2. Proibir atribuição de `roles/editor` e `roles/owner` em ambientes de produção.',
        'id': 'A.5.18',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.18): Ensure that access '
                                                     'rights to information and assets are provisioned, periodically '
                                                     'reviewed, modified, and revoked in accordance with access '
                                                     'control policy.',
                                      'name': 'Access rights',
                                      'question': 'Does the organization ensure that access rights to information and '
                                                  'assets are provisioned, periodically reviewed, modified, and '
                                                  'revoked in accordance with access control policy?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.18): Asegurar que '
                                                     'los derechos de acceso a la información y activos asociados se '
                                                     'aprovisionen, revisen periódicamente y revoquen según la '
                                                     'política.',
                                      'name': 'Derechos de acceso',
                                      'question': '¿Garantiza la organización que los derechos de acceso a la '
                                                  'información y activos asociados se aprovisionen, revisen '
                                                  'periódicamente y revoquen según la política?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.18): '
                                                     'Assegurar que os direitos de acesso a informações e ativos '
                                                     'associados sejam provisionados, revisados periodicamente e '
                                                     'revogados de acordo com a política.',
                                      'name': 'Direitos de acesso',
                                      'question': 'A organização garante que os direitos de acesso a informações e '
                                                  'ativos associados sejam provisionados, revisados periodicamente e '
                                                  'revogados de acordo com a política?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Vendor Risk Management & Third-Party Audit Matrix',
        'how_to_check': '1. Verificar inventário de fornecedores e prestadores com acesso a ambientes Google Cloud.\n'
                        '2. Checar questionário de segurança e relatórios SOC 2 / ISO 27001 dos parceiros.',
        'how_to_maintain': '1. Exigir assinatura de aditivo de segurança e privacidade (DPA) em 100% dos contratos com '
                           'terceiros.\n'
                           '2. Conduzir avaliação anual de risco de segurança de fornecedores.',
        'id': 'A.5.19',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.19): Ensure that '
                                                     'processes and procedures are defined and implemented to manage '
                                                     'information security risks associated with supplier access.',
                                      'name': 'Information security in supplier relationships',
                                      'question': 'Does the organization ensure that processes and procedures are '
                                                  'defined and implemented to manage information security risks '
                                                  'associated with supplier access?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.19): Asegurar que '
                                                     'se definan e implementen procesos y procedimientos para '
                                                     'gestionar los riesgos de seguridad asociados al acceso de '
                                                     'proveedores.',
                                      'name': 'Seguridad de la información en las relaciones con proveedores',
                                      'question': '¿Garantiza la organización que se definan e implementen procesos y '
                                                  'procedimientos para gestionar los riesgos de seguridad asociados al '
                                                  'acceso de proveedores?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.19): '
                                                     'Assegurar que processos e procedimentos sejam definidos e '
                                                     'implementados para gerenciar os riscos de segurança associados '
                                                     'ao acesso de fornecedores.',
                                      'name': 'Segurança da informação no relacionamento com fornecedores',
                                      'question': 'A organização garante que processos e procedimentos sejam definidos '
                                                  'e implementados para gerenciar os riscos de segurança associados ao '
                                                  'acesso de fornecedores?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Supplier Security Addendum & Contractual SLA Repository',
        'how_to_check': '1. Inspecionar cláusulas contratuais de segurança, SLAs de resposta a incidentes e direito de '
                        'avaliação com provedores.\n'
                        '2. Verificar conformidade de cláusulas de proteção de dados (LGPD / GDPR).',
        'how_to_maintain': '1. Padronizar minutas contratuais de TI com revisão obrigatória do departamento de '
                           'Segurança e Jurídico.\n'
                           '2. Incluir obrigação de notificação de brechas de segurança em até 48 horas.',
        'id': 'A.5.20',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.20): Ensure that '
                                                     'relevant information security requirements are formally '
                                                     'established and agreed with each supplier that accesses '
                                                     'corporate assets.',
                                      'name': 'Addressing information security within supplier agreements',
                                      'question': 'Does the organization ensure that relevant information security '
                                                  'requirements are formally established and agreed with each supplier '
                                                  'that accesses corporate assets?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.20): Asegurar que '
                                                     'los requisitos pertinentes de seguridad de la información se '
                                                     'establezcan y acuerden formalmente con cada proveedor.',
                                      'name': 'Tratamiento de la seguridad de la información en los acuerdos con '
                                              'proveedores',
                                      'question': '¿Garantiza la organización que los requisitos pertinentes de '
                                                  'seguridad de la información se establezcan y acuerden formalmente '
                                                  'con cada proveedor?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.20): '
                                                     'Assegurar que requisitos relevantes de segurança da informação '
                                                     'sejam formalmente estabelecidos e acordados com cada fornecedor.',
                                      'name': 'Abordando a segurança da informação nos acordos com fornecedores',
                                      'question': 'A organização garante que requisitos relevantes de segurança da '
                                                  'informação sejam formalmente estabelecidos e acordados com cada '
                                                  'fornecedor?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Binary Authorization & Artifact Registry Vulnerability Scanning',
        'how_to_check': '1. Inspecionar proveniência de contêineres e imagens de software no Artifact Registry.\n'
                        '2. Validar assinatura criptográfica de binários com Binary Authorization antes da implantação '
                        'no GKE.',
        'how_to_maintain': '1. Enforçar verificação de atestados SLSA (Supply-chain Levels for Software Artifacts) '
                           'nível 3.\n'
                           '2. Bloquear imagens não assinadas ou construídas fora dos pipelines Cloud Build '
                           'homologados.',
        'id': 'A.5.21',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.21): Ensure that '
                                                     'processes and procedures are implemented to manage security '
                                                     'risks associated with the ICT products and services supply '
                                                     'chain.',
                                      'name': 'Managing information security in the ICT supply chain',
                                      'question': 'Does the organization ensure that processes and procedures are '
                                                  'implemented to manage security risks associated with the ICT '
                                                  'products and services supply chain?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.21): Asegurar que '
                                                     'se implementen procesos y procedimientos para gestionar los '
                                                     'riesgos de seguridad asociados a la cadena de suministro de TIC.',
                                      'name': 'Gestión de la seguridad de la información en la cadena de suministro de '
                                              'TIC',
                                      'question': '¿Garantiza la organización que se implementen procesos y '
                                                  'procedimientos para gestionar los riesgos de seguridad asociados a '
                                                  'la cadena de suministro de TIC?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.21): '
                                                     'Assegurar que processos e procedimentos sejam implementados para '
                                                     'gerenciar os riscos de segurança associados à cadeia de '
                                                     'suprimentos de produtos e serviços de TIC.',
                                      'name': 'Gestão da segurança da informação na cadeia de suprimentos de TIC',
                                      'question': 'A organização garante que processos e procedimentos sejam '
                                                  'implementados para gerenciar os riscos de segurança associados à '
                                                  'cadeia de suprimentos de produtos e serviços de TIC?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Detectar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Disponibilidade, Integridade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Cloud Monitoring SLA Dashboards & Supplier Review',
        'how_to_check': '1. Inspecionar relatórios mensais de cumprimento de SLA e disponibilidade de serviços '
                        'terceirizados.\n'
                        '2. Inspecionar alterações em serviços de terceiros integrados via APIs GCP.',
        'how_to_maintain': '1. Revisão trimestral de desempenho de segurança dos fornecedores críticos.\n'
                           '2. Monitorar métricas de disponibilidade e latência via Cloud Monitoring com alertas de '
                           'desvio de SLA.',
        'id': 'A.5.22',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.22): Ensure that the '
                                                     'organization regularly monitors, reviews, audits, and manages '
                                                     'changes in supplier security practices and service delivery.',
                                      'name': 'Monitoring, review and change management of supplier services',
                                      'question': 'Does the organization ensure that the organization regularly '
                                                  'monitors, reviews, audits, and manages changes in supplier security '
                                                  'practices and service delivery?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.22): Asegurar que '
                                                     'la organización supervise, revise y audite periódicamente las '
                                                     'prácticas de seguridad de los proveedores y gestione los '
                                                     'cambios.',
                                      'name': 'Monitoreo, revisión y gestión de cambios en los servicios de '
                                              'proveedores',
                                      'question': '¿Garantiza la organización que la organización supervise, revise y '
                                                  'audite periódicamente las prácticas de seguridad de los proveedores '
                                                  'y gestione los cambios?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.22): '
                                                     'Assegurar que a organização monitore, analise e audite '
                                                     'regularmente as práticas de segurança de serviços de '
                                                     'fornecedores e gerencie mudanças contratuais.',
                                      'name': 'Monitoramento, análise e gestão de mudanças de serviços de fornecedores',
                                      'question': 'A organização garante que a organização monitore, analise e audite '
                                                  'regularmente as práticas de segurança de serviços de fornecedores e '
                                                  'gerencie mudanças contratuais?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Segurança em Nuvem',
                          'concepts': 'Identificar, Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'GCS Public Access Prevention (PAP) & VPC Service Controls',
        'how_to_check': '1. Inspecionar matriz de responsabilidade compartilhada (Shared Responsibility Model) no '
                        'Google Cloud.\n'
                        '2. Checar controles nativos: Public Access Prevention (PAP) em buckets GCS e VPC Service '
                        'Controls.\n'
                        '3. Validar estratégia de saída (Exit Strategy) e portabilidade de dados.',
        'how_to_maintain': '1. Enforçar Organization Policies que proíbem criação de buckets públicos e serviços '
                           'expostos sem aprovação.\n'
                           '2. Utilizar ferramentas de infraestrutura como código (Terraform) para garantir '
                           'portabilidade e replicabilidade dos ambientes.',
        'id': 'A.5.23',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.23): Ensure that '
                                                     'processes for acquisition, use, management, and exit from cloud '
                                                     'services are established in accordance with organizational '
                                                     'security requirements.',
                                      'name': 'Information security for use of cloud services',
                                      'question': 'Does the organization ensure that processes for acquisition, use, '
                                                  'management, and exit from cloud services are established in '
                                                  'accordance with organizational security requirements?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.23): Asegurar que '
                                                     'se establezcan procesos para la adquisición, uso, gestión y '
                                                     'salida de servicios en la nube conforme a los requisitos '
                                                     'organizacionales.',
                                      'name': 'Seguridad de la información para el uso de servicios en la nube',
                                      'question': '¿Garantiza la organización que se establezcan procesos para la '
                                                  'adquisición, uso, gestión y salida de servicios en la nube conforme '
                                                  'a los requisitos organizacionales?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.23): '
                                                     'Assegurar que processos para aquisição, uso, gestão e saída de '
                                                     'serviços em nuvem sejam estabelecidos em conformidade com os '
                                                     'requisitos organizacionais.',
                                      'name': 'Segurança da informação para o uso de serviços em nuvem',
                                      'question': 'A organização garante que processos para aquisição, uso, gestão e '
                                                  'saída de serviços em nuvem sejam estabelecidos em conformidade com '
                                                  'os requisitos organizacionais?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Resposta a Incidentes',
                          'concepts': 'Responder',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Incident Response Playbooks & Cloud Incident Response Team',
        'how_to_check': '1. Inspecionar plano formal de resposta a incidentes de segurança cibernética (IRP).\n'
                        '2. Verificar se o playbook de resposta a incidentes em nuvem cobre compromisso de chaves, '
                        'negação de serviço e vazamento de dados.',
        'how_to_maintain': '1. Atualizar contatos e playbooks semestralmente.\n'
                           '2. Conduzir simulações de mesa (Tabletop Exercises) e testes de contenção de incidentes a '
                           'cada 6 meses.',
        'id': 'A.5.24',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.24): Ensure that the '
                                                     'organization plans and prepares for managing information '
                                                     'security incidents by defining processes, roles, and '
                                                     'responsibilities.',
                                      'name': 'Information security incident management planning and preparation',
                                      'question': 'Does the organization ensure that the organization plans and '
                                                  'prepares for managing information security incidents by defining '
                                                  'processes, roles, and responsibilities?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.24): Asegurar que '
                                                     'la organización planifique y se prepare para la gestión de '
                                                     'incidentes de seguridad mediante procesos, roles y '
                                                     'responsabilidades.',
                                      'name': 'Planificación y preparación de la gestión de incidentes de seguridad de '
                                              'la información',
                                      'question': '¿Garantiza la organización que la organización planifique y se '
                                                  'prepare para la gestión de incidentes de seguridad mediante '
                                                  'procesos, roles y responsabilidades?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.24): '
                                                     'Assegurar que a organização planeje e se prepare para gerenciar '
                                                     'incidentes de segurança da informação definindo processos, '
                                                     'papéis e responsabilidades.',
                                      'name': 'Planejamento e preparação para gestão de incidentes de segurança da '
                                              'informação',
                                      'question': 'A organização garante que a organização planeje e se prepare para '
                                                  'gerenciar incidentes de segurança da informação definindo '
                                                  'processos, papéis e responsabilidades?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Resposta a Incidentes',
                          'concepts': 'Detectar',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Security Command Center Findings & Chronicle SIEM Triaging',
        'how_to_check': '1. Inspecionar regras de correlação no Google Security Operations (Chronicle SIEM).\n'
                        '2. Inspecionar a triagem e severidade de alertas gerados pelo Security Command Center (SCC).',
        'how_to_maintain': '1. Integrar alertas automáticos do SCC com plataformas de ITSM (Jira / ServiceNow / '
                           'PagerDuty).\n'
                           '2. Monitorar tempo médio de triagem (MTTA) de eventos de segurança.',
        'id': 'A.5.25',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.25): Ensure that '
                                                     'information security events are promptly assessed and decided '
                                                     'whether they should be categorized as information security '
                                                     'incidents.',
                                      'name': 'Assessment and decision on information security events',
                                      'question': 'Does the organization ensure that information security events are '
                                                  'promptly assessed and decided whether they should be categorized as '
                                                  'information security incidents?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.25): Asegurar que '
                                                     'los eventos de seguridad de la información se evalúen y se '
                                                     'decida si deben categorizarse como incidentes de seguridad.',
                                      'name': 'Evaluación y toma de decisiones sobre eventos de seguridad de la '
                                              'información',
                                      'question': '¿Garantiza la organización que los eventos de seguridad de la '
                                                  'información se evalúen y se decida si deben categorizarse como '
                                                  'incidentes de seguridad?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.25): '
                                                     'Assegurar que eventos de segurança da informação sejam avaliados '
                                                     'e seja decidido se devem ser categorizados formalmente como '
                                                     'incidentes de segurança.',
                                      'name': 'Avaliação e decisão sobre eventos de segurança da informação',
                                      'question': 'A organização garante que eventos de segurança da informação sejam '
                                                  'avaliados e seja decidido se devem ser categorizados formalmente '
                                                  'como incidentes de segurança?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Resposta a Incidentes',
                          'concepts': 'Responder',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Corretivo'},
        'gcp_mapping': 'Automated VPC Quarantine & Incident Response Orchestration',
        'how_to_check': '1. Validar histórico de incidentes tratados nos últimos 12 meses e tempo de contenção '
                        '(MTTR).\n'
                        '2. Checar se procedimentos de isolamento de rede (VPC Quarantine) e revogação de credenciais '
                        'comprometidas foram seguidos.',
        'how_to_maintain': '1. Manter automações de contenção via Cloud Functions / Workflows para isolar instâncias e '
                           'revogar tokens comprometidos.\n'
                           '2. Conduzir análise post-mortem em 100% dos incidentes de severidade alta.',
        'id': 'A.5.26',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.26): Ensure that '
                                                     'information security incidents are responded to in accordance '
                                                     'with documented procedures and communicated in a timely manner.',
                                      'name': 'Response to information security incidents',
                                      'question': 'Does the organization ensure that information security incidents '
                                                  'are responded to in accordance with documented procedures and '
                                                  'communicated in a timely manner?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.26): Asegurar que '
                                                     'los incidentes de seguridad de la información se respondan de '
                                                     'acuerdo con procedimientos documentados y se comuniquen '
                                                     'oportunamente.',
                                      'name': 'Respuesta a incidentes de seguridad de la información',
                                      'question': '¿Garantiza la organización que los incidentes de seguridad de la '
                                                  'información se respondan de acuerdo con procedimientos documentados '
                                                  'y se comuniquen oportunamente?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.26): '
                                                     'Assegurar que incidentes de segurança da informação sejam '
                                                     'respondidos de acordo com procedimentos documentados e '
                                                     'comunicados tempestivamente.',
                                      'name': 'Resposta a incidentes de segurança da informação',
                                      'question': 'A organização garante que incidentes de segurança da informação '
                                                  'sejam respondidos de acordo com procedimentos documentados e '
                                                  'comunicados tempestivamente?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Recuperar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Corretivo'},
        'gcp_mapping': 'Post-Mortem Action Tracker & Continuous Improvement Loop',
        'how_to_check': '1. Inspecionar relatórios post-mortem e planos de ação corretiva resultantes de incidentes '
                        'passados.\n'
                        '2. Validar se os planos de ação geraram novos controles técnicos no Terraform e Organization '
                        'Policies.',
        'how_to_maintain': '1. Reunião mensal de revisão de lições aprendidas com times de engenharia e operações.\n'
                           '2. Acompanhar fechamento de itens de remediação através de painel executivo de GRC.',
        'id': 'A.5.27',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.27): Ensure that '
                                                     'knowledge gained from information security incidents is used to '
                                                     'strengthen controls, reduce recurrence likelihood, and improve '
                                                     'response.',
                                      'name': 'Learning from information security incidents',
                                      'question': 'Does the organization ensure that knowledge gained from information '
                                                  'security incidents is used to strengthen controls, reduce '
                                                  'recurrence likelihood, and improve response?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.27): Asegurar que '
                                                     'el conocimiento adquirido de los incidentes de seguridad se '
                                                     'utilice para prevenir su recurrencia y mejorar los controles.',
                                      'name': 'Aprendizaje de los incidentes de seguridad de la información',
                                      'question': '¿Garantiza la organización que el conocimiento adquirido de los '
                                                  'incidentes de seguridad se utilice para prevenir su recurrencia y '
                                                  'mejorar los controles?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.27): '
                                                     'Assegurar que o conhecimento adquirido na análise e resolução de '
                                                     'incidentes de segurança seja utilizado para prevenir a '
                                                     'recorrência e melhorar controles.',
                                      'name': 'Aprendizado com incidentes de segurança da informação',
                                      'question': 'A organização garante que o conhecimento adquirido na análise e '
                                                  'resolução de incidentes de segurança seja utilizado para prevenir a '
                                                  'recorrência e melhorar controles?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Forense Digital',
                          'concepts': 'Responder',
                          'domains': 'Defesa',
                          'properties': 'Integridade',
                          'type': 'Corretivo'},
        'gcp_mapping': 'Cloud Storage Bucket Lock (WORM) & Forensic Snapshots',
        'how_to_check': '1. Validar preservação de evidências digitais: buckets de logs com Object Retention / Bucket '
                        'Lock (WORM).\n'
                        '2. Checar integridade criptográfica de snapshots e logs forenses.',
        'how_to_maintain': '1. Habilitar retenção imutável de logs no Cloud Storage por no mínimo 365 dias para fins '
                           'forenses e regulatórios.\n'
                           '2. Garantir cadeia de custódia com hash SHA-256 no grafo imutável.',
        'id': 'A.5.28',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.28): Ensure that the '
                                                     'organization defines and applies procedures for identification, '
                                                     'collection, acquisition, and preservation of digital evidence of '
                                                     'incidents.',
                                      'name': 'Collection of evidence',
                                      'question': 'Does the organization ensure that the organization defines and '
                                                  'applies procedures for identification, collection, acquisition, and '
                                                  'preservation of digital evidence of incidents?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.28): Asegurar que '
                                                     'la organización defina y aplique procedimientos para la '
                                                     'identificación, recolección y preservación de evidencias '
                                                     'forenses digitales.',
                                      'name': 'Recopilación de evidencias',
                                      'question': '¿Garantiza la organización que la organización defina y aplique '
                                                  'procedimientos para la identificación, recolección y preservación '
                                                  'de evidencias forenses digitales?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.28): '
                                                     'Assegurar que a organização defina e aplique procedimentos para '
                                                     'identificação, coleta, aquisição e preservação de evidências '
                                                     'digitais de incidentes.',
                                      'name': 'Coleta de evidências',
                                      'question': 'A organização garante que a organização defina e aplique '
                                                  'procedimentos para identificação, coleta, aquisição e preservação '
                                                  'de evidências digitais de incidentes?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Continuidade do Negócio',
                          'concepts': 'Proteger, Recuperar',
                          'domains': 'Resiliência',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'High-Availability Security Topology & Identity Federation Fallback',
        'how_to_check': '1. Inspecionar plano de continuidade de negócios (BCP) em cenários de indisponibilidade de '
                        'serviços de segurança.\n'
                        '2. Validar que controles de autenticação e criptografia continuam operacionais durante modos '
                        'degradados.',
        'how_to_maintain': '1. Testar cenários de fallback mantendo autenticação federada resiliente em múltiplos '
                           'provedores de identidade.\n'
                           '2. Proibir bypass de segurança em procedimentos de contingência.',
        'id': 'A.5.29',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.29): Ensure that the '
                                                     'organization plans how to maintain information security at an '
                                                     'appropriate level during disruption or disaster situations.',
                                      'name': 'Information security during disruption',
                                      'question': 'Does the organization ensure that the organization plans how to '
                                                  'maintain information security at an appropriate level during '
                                                  'disruption or disaster situations?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.29): Asegurar que '
                                                     'la organización planifique cómo mantener la seguridad de la '
                                                     'información en el nivel adecuado durante situaciones de '
                                                     'interrupción.',
                                      'name': 'Seguridad de la información durante interrupciones',
                                      'question': '¿Garantiza la organización que la organización planifique cómo '
                                                  'mantener la seguridad de la información en el nivel adecuado '
                                                  'durante situaciones de interrupción?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.29): '
                                                     'Assegurar que a organização planeje como manter a segurança da '
                                                     'informação no nível apropriado durante eventos de crise ou '
                                                     'interrupção.',
                                      'name': 'Segurança da informação durante interrupções',
                                      'question': 'A organização garante que a organização planeje como manter a '
                                                  'segurança da informação no nível apropriado durante eventos de '
                                                  'crise ou interrupção?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Continuidade do Negócio',
                          'concepts': 'Recuperar',
                          'domains': 'Resiliência',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo, Corretivo'},
        'gcp_mapping': 'Multiregion Cloud SQL / Spanner & Cloud DNS Failover',
        'how_to_check': '1. Inspecionar arquitetura de alta disponibilidade: cargas de trabalho distribuídas em múltiplas '
                        'zonas e regiões GCP.\n'
                        '2. Checar relatórios de testes de failover e métricas de RTO/RPO alcançadas.',
        'how_to_maintain': '1. Automatizar testes semestrais de Disaster Recovery com comutação de tráfego via Cloud '
                           'DNS / Global Load Balancing.\n'
                           '2. Habilitar replicação assíncrona para bancos de dados críticos (Cloud Spanner / Cloud '
                           'SQL Cross-Region).',
        'id': 'A.5.30',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.30): Ensure that ICT '
                                                     'readiness is planned, implemented, maintained, and tested based '
                                                     'on business continuity objectives and RTO/RPO requirements.',
                                      'name': 'ICT readiness for business continuity',
                                      'question': 'Does the organization ensure that ICT readiness is planned, '
                                                  'implemented, maintained, and tested based on business continuity '
                                                  'objectives and RTO/RPO requirements?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.30): Asegurar que '
                                                     'la preparación de las TIC se planifique, implemente, mantenga y '
                                                     'pruebe según los objetivos de continuidad del negocio y RTO/RPO.',
                                      'name': 'Preparación de las TIC para la continuidad del negocio',
                                      'question': '¿Garantiza la organización que la preparación de las TIC se '
                                                  'planifique, implemente, mantenga y pruebe según los objetivos de '
                                                  'continuidad del negocio y RTO/RPO?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.30): '
                                                     'Assegurar que a prontidão de TIC seja planejada, implementada, '
                                                     'mantida e testada com base nos objetivos de continuidade de '
                                                     'negócios e RTO/RPO.',
                                      'name': 'Prontidão de TIC para continuidade de negócios',
                                      'question': 'A organização garante que a prontidão de TIC seja planejada, '
                                                  'implementada, mantida e testada com base nos objetivos de '
                                                  'continuidade de negócios e RTO/RPO?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Compliance Obligations Register & Horizon Scanner',
        'how_to_check': '1. Inspecionar matriz de conformidade legal e regulatória (LGPD, BACEN, PCI-DSS, ISO 27001).\n'
                        '2. Validar mapeamento dos requisitos legais com controles técnicos implementados na nuvem.',
        'how_to_maintain': '1. Revisão semestral da matriz regulatória com apoio da assessoria jurídica.\n'
                           '2. Monitorar novas resoluções e normas setoriais via subagente Horizon Scanner.',
        'id': 'A.5.31',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.31): Ensure that '
                                                     'applicable legal, statutory, regulatory, and contractual '
                                                     'requirements related to information security are explicitly '
                                                     'identified and met.',
                                      'name': 'Legal, statutory, regulatory and contractual requirements',
                                      'question': 'Does the organization ensure that applicable legal, statutory, '
                                                  'regulatory, and contractual requirements related to information '
                                                  'security are explicitly identified and met?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.31): Asegurar que '
                                                     'los requisitos legales, estatutarios, reglamentarios y '
                                                     'contractuales aplicables se identifiquen explícitamente y se '
                                                     'cumplan.',
                                      'name': 'Requisitos legales, estatutarios, reglamentarios y contractuales',
                                      'question': '¿Garantiza la organización que los requisitos legales, '
                                                  'estatutarios, reglamentarios y contractuales aplicables se '
                                                  'identifiquen explícitamente y se cumplan?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.31): '
                                                     'Assegurar que requisitos legais, estatutários, regulatórios e '
                                                     'contratuais aplicáveis à segurança da informação sejam '
                                                     'explicitamente identificados e atendidos.',
                                      'name': 'Requisitos legais, estatutários, regulamentares e contratuais',
                                      'question': 'A organização garante que requisitos legais, estatutários, '
                                                  'regulatórios e contratuais aplicáveis à segurança da informação '
                                                  'sejam explicitamente identificados e atendidos?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Proteger',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Software License Scanner & Artifact Registry Licensing Checks',
        'how_to_check': '1. Inspecionar licenças de software e dependências de código aberto utilizadas nos projetos '
                        'GCP.\n'
                        '2. Checar escaneamento de licenças em pipelines Cloud Build / GitHub Actions.',
        'how_to_maintain': '1. Automatizar bloqueio de pacotes com licenças incompatíveis ou restritivas (GPL em '
                           'bibliotecas proprietárias).\n'
                           '2. Manter inventário de software proprietário protegido em repositórios com acesso '
                           'restrito.',
        'id': 'A.5.32',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.32): Ensure that the '
                                                     'organization implements appropriate procedures to protect '
                                                     'intellectual property rights and maintain software license '
                                                     'compliance.',
                                      'name': 'Intellectual property rights',
                                      'question': 'Does the organization ensure that the organization implements '
                                                  'appropriate procedures to protect intellectual property rights and '
                                                  'maintain software license compliance?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.32): Asegurar que '
                                                     'la organización implemente procedimientos adecuados para '
                                                     'proteger los derechos de propiedad intelectual y licencias de '
                                                     'software.',
                                      'name': 'Derechos de propiedad intelectual',
                                      'question': '¿Garantiza la organización que la organización implemente '
                                                  'procedimientos adecuados para proteger los derechos de propiedad '
                                                  'intelectual y licencias de software?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.32): '
                                                     'Assegurar que a organização implemente procedimentos adequados '
                                                     'para proteger os direitos de propriedade intelectual e '
                                                     'conformidade de licenças de software.',
                                      'name': 'Direitos de propriedade intelectual',
                                      'question': 'A organização garante que a organização implemente procedimentos '
                                                  'adequados para proteger os direitos de propriedade intelectual e '
                                                  'conformidade de licenças de software?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'GCS Retention Policies & Immutable Object Versioning',
        'how_to_check': '1. Inspecionar retenção de registros contábeis, logs fiscais e avaliações no Cloud Storage com '
                        'Bucket Lock.\n'
                        '2. Validar controle de versão e proteção contra exclusão acidental.',
        'how_to_maintain': '1. Enforçar política de imutabilidade e retenção mínima de 5 anos para registros '
                           'corporativos obrigatórios.\n'
                           '2. Bloquear permissão de exclusão de registros mesmo para administradores '
                           '(`roles/storage.admin`).',
        'id': 'A.5.33',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.33): Ensure that '
                                                     'organizational records are protected from loss, destruction, '
                                                     'falsification, unauthorized access, and unauthorized release.',
                                      'name': 'Protection of records',
                                      'question': 'Does the organization ensure that organizational records are '
                                                  'protected from loss, destruction, falsification, unauthorized '
                                                  'access, and unauthorized release?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.33): Asegurar que '
                                                     'los registros se protejan contra pérdida, destrucción, '
                                                     'falsificación, acceso no autorizado y divulgación indebida.',
                                      'name': 'Protección de registros',
                                      'question': '¿Garantiza la organización que los registros se protejan contra '
                                                  'pérdida, destrucción, falsificación, acceso no autorizado y '
                                                  'divulgación indebida?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.33): '
                                                     'Assegurar que registros corporativos sejam protegidos contra '
                                                     'perda, destruição, falsificação, acesso não autorizado e '
                                                     'liberação indevida.',
                                      'name': 'Proteção de registros',
                                      'question': 'A organização garante que registros corporativos sejam protegidos '
                                                  'contra perda, destruição, falsificação, acesso não autorizado e '
                                                  'liberação indevida?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Privacidade',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Sensitive Data Protection (Cloud DLP) & CMEK Encryption',
        'how_to_check': '1. Inspecionar bases de dados contendo dados pessoais: verificar anonimização e criptografia em '
                        'repouso com CMEK.\n'
                        '2. Inspecionar relatórios de impacto à proteção de dados (RIPD / DPIA).',
        'how_to_maintain': '1. Implementar mascaramento automático de dados PII em tempo real com Sensitive Data '
                           'Protection (DLP).\n'
                           '2. Manter canal de atendimento aos direitos dos titulares de dados (DSR).',
        'id': 'A.5.34',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.34): Ensure that the '
                                                     'organization ensures compliance with applicable privacy '
                                                     'legislation and protection of Personally Identifiable '
                                                     'Information (LGPD/GDPR).',
                                      'name': 'Privacy and protection of PII',
                                      'question': 'Does the organization ensure that the organization ensures '
                                                  'compliance with applicable privacy legislation and protection of '
                                                  'Personally Identifiable Information (LGPD/GDPR)?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.34): Asegurar que '
                                                     'la organización garantice el cumplimiento de las leyes de '
                                                     'privacidad y protección de datos personales (LGPD/GDPR).',
                                      'name': 'Privacidad y protección de datos personales (PII)',
                                      'question': '¿Garantiza la organización que la organización garantice el '
                                                  'cumplimiento de las leyes de privacidad y protección de datos '
                                                  'personales (LGPD/GDPR)?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.34): '
                                                     'Assegurar que a organização garanta a conformidade com leis e '
                                                     'regulamentações aplicáveis de privacidade e proteção de dados '
                                                     'pessoais (LGPD/GDPR).',
                                      'name': 'Privacidade e proteção de dados pessoais (PII)',
                                      'question': 'A organização garante que a organização garanta a conformidade com '
                                                  'leis e regulamentações aplicáveis de privacidade e proteção de '
                                                  'dados pessoais (LGPD/GDPR)?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Independent Audit Reports & External Penetration Testing',
        'how_to_check': '1. Inspecionar relatórios de avaliação independente e testes de intrusão (pentest) externos '
                        'dos últimos 12 meses.\n'
                        '2. Validar independência do avaliador em relação à operação técnica auditada.',
        'how_to_maintain': '1. Realizar avaliações independentes anuais e pentests externos antes de grandes '
                           'lançamentos.\n'
                           '2. Acompanhar a execução do plano de remediação de apontamentos de conformidade.',
        'id': 'A.5.35',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.35): Ensure that the '
                                                     'organization approach to managing information security and its '
                                                     'implementation is independently reviewed at planned intervals.',
                                      'name': 'Independent review of information security',
                                      'question': 'Does the organization ensure that the organization approach to '
                                                  'managing information security and its implementation is '
                                                  'independently reviewed at planned intervals?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.35): Asegurar que '
                                                     'el enfoque de la organización para gestionar la seguridad de la '
                                                     'información se revise de forma independiente a intervalos '
                                                     'planificados.',
                                      'name': 'Revisión independiente de la seguridad de la información',
                                      'question': '¿Garantiza la organización que el enfoque de la organización para '
                                                  'gestionar la seguridad de la información se revise de forma '
                                                  'independiente a intervalos planificados?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.35): '
                                                     'Assegurar que a abordagem da organização para gerenciar a '
                                                     'segurança da informação seja revisada de forma independente a '
                                                     'intervalos planejados.',
                                      'name': 'Revisão independente da segurança da informação',
                                      'question': 'A organização garante que a abordagem da organização para gerenciar '
                                                  'a segurança da informação seja revisada de forma independente a '
                                                  'intervalos planejados?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar, Detectar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Security Health Analytics & Continuous Policy Scanner',
        'how_to_check': '1. Inspecionar score contínuo de conformidade no Security Health Analytics do Google Cloud.\n'
                        '2. Inspecionar desvios entre código Terraform e infraestrutura real no GCP.',
        'how_to_maintain': '1. Executar varreduras diárias automatizadas de conformidade com alertas no Slack/Chat.\n'
                           '2. Impedir merge de pull requests que introduzam desvios de conformidade.',
        'id': 'A.5.36',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.36): Ensure that '
                                                     'managers regularly review the compliance of information '
                                                     'processing and procedures within their area with security '
                                                     'policies.',
                                      'name': 'Compliance with policies, rules and standards for information security',
                                      'question': 'Does the organization ensure that managers regularly review the '
                                                  'compliance of information processing and procedures within their '
                                                  'area with security policies?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.36): Asegurar que '
                                                     'los responsables revisen periódicamente la conformidad de los '
                                                     'procedimientos y procesos con las políticas de seguridad.',
                                      'name': 'Cumplimiento de políticas, normas y estándares de seguridad de la '
                                              'información',
                                      'question': '¿Garantiza la organización que los responsables revisen '
                                                  'periódicamente la conformidad de los procedimientos y procesos con '
                                                  'las políticas de seguridad?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.36): '
                                                     'Assegurar que os gestores revisem regularmente a conformidade '
                                                     'dos procedimentos e processos sob sua responsabilidade com as '
                                                     'políticas de segurança.',
                                      'name': 'Conformidade com políticas, regras e normas de segurança da informação',
                                      'question': 'A organização garante que os gestores revisem regularmente a '
                                                  'conformidade dos procedimentos e processos sob sua responsabilidade '
                                                  'com as políticas de segurança?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Zero-Copy SOP Repository & Runbooks',
        'how_to_check': '1. Inspecionar repositório centralizado de Procedimentos Operacionais Padrão (SOPs) no Google '
                        'Workspace/Drive.\n'
                        '2. Checar se procedimentos de backup, patching, provisionamento e resposta a incidentes estão '
                        'documentados.',
        'how_to_maintain': '1. Revisão e homologação anual obrigatória de 100% dos SOPs com controle de versão.\n'
                           '2. Garantir acesso imediato aos procedimentos para equipes de plantão (SRE/SecOps).',
        'id': 'A.5.37',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.5',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.5.37): Ensure that '
                                                     'operating procedures for information processing facilities are '
                                                     'documented and made available to all users who need them.',
                                      'name': 'Documented operating procedures',
                                      'question': 'Does the organization ensure that operating procedures for '
                                                  'information processing facilities are documented and made available '
                                                  'to all users who need them?',
                                      'recommended_evidence': '1. Documented corporate policies and procedures '
                                                              'approved by executive management.\n'
                                                              '2. Information security committee meeting minutes and '
                                                              'management reviews.\n'
                                                              '3. Internal audit reports and Google Cloud Organization '
                                                              'Policies compliance export (`gcloud resource-manager '
                                                              'org-policies list`).\n'
                                                              '4. Vendor contracts, service level agreements (SLAs), '
                                                              'and non-disclosure agreements (NDAs).',
                                      'theme': 'A.5 Organizational',
                                      'theme_title': 'A.5 — Organizational Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.5.37): Asegurar que '
                                                     'los procedimientos operativos para las instalaciones de '
                                                     'procesamiento de información se documenten y estén a disposición '
                                                     'de los usuarios.',
                                      'name': 'Procedimientos operativos documentados',
                                      'question': '¿Garantiza la organización que los procedimientos operativos para '
                                                  'las instalaciones de procesamiento de información se documenten y '
                                                  'estén a disposición de los usuarios?',
                                      'recommended_evidence': '1. Políticas y procedimientos corporativos documentados '
                                                              'y aprobados por la alta dirección.\n'
                                                              '2. Actas de reuniones del comité de seguridad de la '
                                                              'información y revisiones por la dirección.\n'
                                                              '3. Informes de evaluación interna y exportación de '
                                                              'Google Cloud Organization Policies (`gcloud '
                                                              'resource-manager org-policies list`).\n'
                                                              '4. Contratos de proveedores, acuerdos de nivel de '
                                                              'servicio (SLA) y acuerdos de confidencialidad (NDA).',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionales'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.5.37): '
                                                     'Assegurar que procedimentos operacionais para instalações de '
                                                     'processamento de informações sejam documentados e '
                                                     'disponibilizados para os operadores.',
                                      'name': 'Procedimentos operacionais documentados',
                                      'question': 'A organização garante que procedimentos operacionais para '
                                                  'instalações de processamento de informações sejam documentados e '
                                                  'disponibilizados para os operadores?',
                                      'recommended_evidence': '1. Políticas e procedimentos corporativos documentados '
                                                              'e aprovados pela Diretoria.\n'
                                                              '2. Atas de reunião do comitê de segurança da informação '
                                                              'e análises críticas da gestão.\n'
                                                              '3. Relatórios de avaliação interna e registros de '
                                                              'conformidade do Google Cloud Organization Policies '
                                                              '(`gcloud resource-manager org-policies list`).\n'
                                                              '4. Contratos e acordos de nível de serviço (SLA/NDA) '
                                                              'com terceiros e fornecedores.',
                                      'theme': 'A.5 Organizacional',
                                      'theme_title': 'A.5 — Controles Organizacionais'}}},
    {   'attributes': {   'capabilities': 'Segurança de RH',
                          'concepts': 'Identificar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'HR Screening Workflow & Access Pre-requisite Gate',
        'how_to_check': '1. Inspecionar processos de RH: checar relatórios de checagem de antecedentes para 100% dos '
                        'colaboradores e terceiros admitidos.\n'
                        '2. Verificar conformidade com legislações de privacidade no processo de triagem.',
        'how_to_maintain': '1. Integrar checklist de antecedentes no sistema de admissão de pessoal (HRIS).\n'
                           '2. Repetir verificações periódicas para colaboradores com acesso a dados confidenciais.',
        'id': 'A.6.1',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.1): Ensure that '
                                                     'background verification checks on all candidates for employment '
                                                     'are carried out in accordance with relevant laws, regulations, '
                                                     'and ethics.',
                                      'name': 'Screening',
                                      'question': 'Does the organization ensure that background verification checks on '
                                                  'all candidates for employment are carried out in accordance with '
                                                  'relevant laws, regulations, and ethics?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.1): Asegurar que '
                                                     'se realicen comprobaciones de antecedentes a todos los '
                                                     'candidatos a empleo conforme a las leyes y regulaciones '
                                                     'aplicables.',
                                      'name': 'Selección y verificación de antecedentes',
                                      'question': '¿Garantiza la organización que se realicen comprobaciones de '
                                                  'antecedentes a todos los candidatos a empleo conforme a las leyes y '
                                                  'regulaciones aplicables?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.1): '
                                                     'Assegurar que checagens de verificação de antecedentes de todos '
                                                     'os candidatos a emprego sejam realizadas de acordo com as leis e '
                                                     'regulamentações relevantes.',
                                      'name': 'Triagem de antecedentes',
                                      'question': 'A organização garante que checagens de verificação de antecedentes '
                                                  'de todos os candidatos a emprego sejam realizadas de acordo com as '
                                                  'leis e regulamentações relevantes?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Segurança de RH',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Contractual Security Clauses & HR Portal',
        'how_to_check': '1. Inspecionar contratos de trabalho: confirmar presença de cláusulas explícitas de '
                        'responsabilidade sobre segurança da informação e sigilo.\n'
                        '2. Checar termos de contratação de pessoas jurídicas e prestadores de serviços.',
        'how_to_maintain': '1. Atualizar termos de trabalho sempre que houver mudanças na política de segurança.\n'
                           '2. Manter guarda digital dos contratos assinados com certificados válidos.',
        'id': 'A.6.2',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.2): Ensure that '
                                                     'employment agreements state personnel and organizational '
                                                     'information security responsibilities and obligations.',
                                      'name': 'Terms and conditions of employment',
                                      'question': 'Does the organization ensure that employment agreements state '
                                                  'personnel and organizational information security responsibilities '
                                                  'and obligations?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.2): Asegurar que '
                                                     'los contratos de trabajo declaren las responsabilidades de '
                                                     'seguridad de la información tanto del colaborador como de la '
                                                     'organización.',
                                      'name': 'Términos y condiciones de empleo',
                                      'question': '¿Garantiza la organización que los contratos de trabajo declaren '
                                                  'las responsabilidades de seguridad de la información tanto del '
                                                  'colaborador como de la organización?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.2): '
                                                     'Assegurar que os contratos de trabalho declarem as '
                                                     'responsabilidades de segurança da informação tanto do '
                                                     'colaborador quanto da organização.',
                                      'name': 'Termos e condições de contratação',
                                      'question': 'A organização garante que os contratos de trabalho declarem as '
                                                  'responsabilidades de segurança da informação tanto do colaborador '
                                                  'quanto da organização?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Segurança de RH',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Security Awareness LMS & Phishing Simulation Metrics',
        'how_to_check': '1. Inspecionar relatórios de conclusão de treinamentos de segurança da informação (taxa de '
                        'adesão > 95%).\n'
                        '2. Avaliar campanhas semestrais de phishing simulado e índices de cliques.',
        'how_to_maintain': '1. Treinamento mandatório anual de segurança para todos os colaboradores e na integração '
                           'de novos funcionários.\n'
                           '2. Treinamento especializado em DevSecOps e segurança em nuvem para equipes técnicas.',
        'id': 'A.6.3',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.3): Ensure that '
                                                     'personnel and relevant interested parties receive appropriate '
                                                     'information security awareness, education, and periodic '
                                                     'training.',
                                      'name': 'Information security awareness, education and training',
                                      'question': 'Does the organization ensure that personnel and relevant interested '
                                                  'parties receive appropriate information security awareness, '
                                                  'education, and periodic training?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.3): Asegurar que '
                                                     'el personal y partes pertinentes reciban concienciación, '
                                                     'educación y capacitación adecuada y periódica en seguridad de la '
                                                     'información.',
                                      'name': 'Concienciación, educación y capacitación en seguridad de la información',
                                      'question': '¿Garantiza la organización que el personal y partes pertinentes '
                                                  'reciban concienciación, educación y capacitación adecuada y '
                                                  'periódica en seguridad de la información?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.3): '
                                                     'Assegurar que colaboradores e partes relevantes recebam '
                                                     'conscientização, educação e treinamento adequados e atualizações '
                                                     'periódicas sobre segurança.',
                                      'name': 'Conscientização, educação e treinamento em segurança da informação',
                                      'question': 'A organização garante que colaboradores e partes relevantes recebam '
                                                  'conscientização, educação e treinamento adequados e atualizações '
                                                  'periódicas sobre segurança?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Segurança de RH',
                          'concepts': 'Responder',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Integridade',
                          'type': 'Corretivo'},
        'gcp_mapping': 'Disciplinary Policy & Ethics Committee Logs',
        'how_to_check': '1. Inspecionar processo disciplinar formal publicado e comunicado a todos os colaboradores.\n'
                        '2. Inspecionar histórico de aplicações de sanções por incidentes provocados por dolo ou '
                        'negligência.',
        'how_to_maintain': '1. Garantir aplicação isonômica do processo disciplinar com acompanhamento do departamento '
                           'Jurídico e RH.\n'
                           '2. Revisar o processo anualmente.',
        'id': 'A.6.4',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.4): Ensure that a formal '
                                                     'and communicated disciplinary process is in place to take action '
                                                     'against personnel who have committed an information security '
                                                     'breach.',
                                      'name': 'Disciplinary process',
                                      'question': 'Does the organization ensure that a formal and communicated '
                                                  'disciplinary process is in place to take action against personnel '
                                                  'who have committed an information security breach?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.4): Asegurar que '
                                                     'exista un proceso disciplinario formal y comunicado para tomar '
                                                     'medidas contra el personal que viole las políticas de seguridad.',
                                      'name': 'Proceso disciplinario',
                                      'question': '¿Garantiza la organización que exista un proceso disciplinario '
                                                  'formal y comunicado para tomar medidas contra el personal que viole '
                                                  'las políticas de seguridad?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.4): '
                                                     'Assegurar que um processo formal e comunicado esteja em vigor '
                                                     'para tomar medidas contra colaboradores que violem as políticas '
                                                     'de segurança.',
                                      'name': 'Processo disciplinar',
                                      'question': 'A organização garante que um processo formal e comunicado esteja em '
                                                  'vigor para tomar medidas contra colaboradores que violem as '
                                                  'políticas de segurança?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Segurança de RH',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Offboarding Exit Checklist & Legal Non-Disclosure',
        'how_to_check': '1. Checar termos de encerramento contratual e lembretes de obrigações de sigilo e '
                        'não-concorrência pós-desligamento.\n'
                        '2. Inspecionar se equipamentos e credenciais foram revogados antes do último dia útil.',
        'how_to_maintain': '1. Formalizar termo de ciência das responsabilidades continuadas no processo de saída.\n'
                           '2. Monitorar tentativas de login ou exfiltração antes e após a notificação de '
                           'desligamento.',
        'id': 'A.6.5',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.5): Ensure that '
                                                     'information security responsibilities that remain valid after '
                                                     'termination or change of employment are defined, enforced, and '
                                                     'communicated.',
                                      'name': 'Responsibilities after termination or change of employment',
                                      'question': 'Does the organization ensure that information security '
                                                  'responsibilities that remain valid after termination or change of '
                                                  'employment are defined, enforced, and communicated?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.5): Asegurar que '
                                                     'las responsabilidades de seguridad de la información que sigan '
                                                     'vigentes tras el cese o cambio de empleo estén definidas y se '
                                                     'cumplan.',
                                      'name': 'Responsabilidades posteriores a la terminación o cambio de empleo',
                                      'question': '¿Garantiza la organización que las responsabilidades de seguridad '
                                                  'de la información que sigan vigentes tras el cese o cambio de '
                                                  'empleo estén definidas y se cumplan?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.5): '
                                                     'Assegurar que as responsabilidades de segurança da informação '
                                                     'que permanecem válidas após a rescisão ou mudança de função '
                                                     'sejam definidas e cumpridas.',
                                      'name': 'Responsabilidades após o encerramento ou mudança de emprego',
                                      'question': 'A organização garante que as responsabilidades de segurança da '
                                                  'informação que permanecem válidas após a rescisão ou mudança de '
                                                  'função sejam definidas e cumpridas?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Digital NDA Repository & Zero-Copy Validation',
        'how_to_check': '1. Inspecionar registro de Termos de Confidencialidade (NDAs) assinados por 100% dos empregados e '
                        'parceiros comerciais.\n'
                        '2. Validar data de validade dos NDAs e abrangência do escopo de dados protegidos.',
        'how_to_maintain': '1. Enforçar assinatura digital de NDA antes da concessão de qualquer credencial de acesso '
                           'aos ambientes GCP.\n'
                           '2. Revisar NDAs em caso de novas parcerias e projetos estratégicos.',
        'id': 'A.6.6',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.6): Ensure that '
                                                     'confidentiality or non-disclosure agreements reflecting the '
                                                     'organization needs for information protection are identified, '
                                                     'signed, and reviewed.',
                                      'name': 'Confidentiality or non-disclosure agreements',
                                      'question': 'Does the organization ensure that confidentiality or non-disclosure '
                                                  'agreements reflecting the organization needs for information '
                                                  'protection are identified, signed, and reviewed?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.6): Asegurar que '
                                                     'los acuerdos de confidencialidad o no divulgación (NDA) reflejen '
                                                     'las necesidades de protección de la información y se revisen '
                                                     'regularmente.',
                                      'name': 'Acuerdos de confidencialidad o no divulgación (NDA)',
                                      'question': '¿Garantiza la organización que los acuerdos de confidencialidad o '
                                                  'no divulgación (NDA) reflejen las necesidades de protección de la '
                                                  'información y se revisen regularmente?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.6): '
                                                     'Assegurar que termos de confidencialidade e não divulgação (NDA) '
                                                     'reflitam as necessidades de proteção da informação e sejam '
                                                     'revisados regularmente.',
                                      'name': 'Acordos de confidencialidade ou de não divulgação (NDA)',
                                      'question': 'A organização garante que termos de confidencialidade e não '
                                                  'divulgação (NDA) reflitam as necessidades de proteção da informação '
                                                  'e sejam revisados regularmente?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Segurança de Recursos Humanos',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'BeyondCorp Enterprise & Remote Device Posture Checks',
        'how_to_check': '1. Inspecionar política de trabalho remoto e telemetria de segurança nos laptops '
                        'corporativos.\n'
                        '2. Checar postura de conformidade de endpoints remotos via BeyondCorp Enterprise (OS '
                        'atualizado, antivírus ativo, criptografia de disco).',
        'how_to_maintain': '1. Bloquear acesso a recursos de produção a partir de redes domésticas ou públicas sem '
                           'túnel seguro e validação de dispositivo.\n'
                           '2. Conduzir varredura contínua de vulnerabilidades em dispositivos remotos.',
        'id': 'A.6.7',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.7): Ensure that security '
                                                     'measures are implemented when personnel work remotely to protect '
                                                     'information accessed, processed, or stored outside premises.',
                                      'name': 'Remote working',
                                      'question': 'Does the organization ensure that security measures are implemented '
                                                  'when personnel work remotely to protect information accessed, '
                                                  'processed, or stored outside premises?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.7): Asegurar que '
                                                     'se implementen medidas de seguridad cuando el personal trabaje '
                                                     'de forma remota para proteger la información procesada fuera de '
                                                     'las instalaciones.',
                                      'name': 'Trabajo remoto',
                                      'question': '¿Garantiza la organización que se implementen medidas de seguridad '
                                                  'cuando el personal trabaje de forma remota para proteger la '
                                                  'información procesada fuera de las instalaciones?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.7): '
                                                     'Assegurar que medidas de segurança da informação sejam '
                                                     'implementadas quando o pessoal estiver trabalhando remotamente '
                                                     'para proteger os ativos acessados.',
                                      'name': 'Trabalho remoto',
                                      'question': 'A organização garante que medidas de segurança da informação sejam '
                                                  'implementadas quando o pessoal estiver trabalhando remotamente para '
                                                  'proteger os ativos acessados?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Resposta a Incidentes',
                          'concepts': 'Detectar',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Incident Reporting Hotlines & Phishing Alert Add-in',
        'how_to_check': '1. Inspecionar canal formal de reporte de incidentes e suspeitas de segurança (ex: botão de '
                        'reporte de phishing, canal SecOps).\n'
                        '2. Avaliar volume de reportes realizados por colaboradores e tempo de resposta do time de '
                        'segurança.',
        'how_to_maintain': '1. Disponibilizar canal ágil e sem atrito para notificação de incidentes via Google Chat e '
                           'email dedicado.\n'
                           '2. Reconhecer e incentivar atitudes proativas de reporte na organização.',
        'id': 'A.6.8',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.6',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.6.8): Ensure that the '
                                                     'organization provides a clear and accessible mechanism for '
                                                     'personnel to report observed or suspected information security '
                                                     'events in a timely manner.',
                                      'name': 'Information security event reporting',
                                      'question': 'Does the organization ensure that the organization provides a clear '
                                                  'and accessible mechanism for personnel to report observed or '
                                                  'suspected information security events in a timely manner?',
                                      'recommended_evidence': '1. Signed employee and contractor confidentiality '
                                                              'agreements (NDAs) and acceptable use acknowledgments.\n'
                                                              '2. Pre-employment screening and background check '
                                                              'records.\n'
                                                              '3. Security awareness training completion certificates '
                                                              'and LMS attendance logs.\n'
                                                              '4. Formal offboarding checklist and access '
                                                              'deprovisioning records across all enterprise systems.',
                                      'theme': 'A.6 People',
                                      'theme_title': 'A.6 — People Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.6.8): Asegurar que '
                                                     'la organización proporcione un canal accesible para que el '
                                                     'personal informe sobre eventos o debilidades de seguridad '
                                                     'observadas.',
                                      'name': 'Reporte de eventos de seguridad de la información',
                                      'question': '¿Garantiza la organización que la organización proporcione un canal '
                                                  'accesible para que el personal informe sobre eventos o debilidades '
                                                  'de seguridad observadas?',
                                      'recommended_evidence': '1. Acuerdos de confidencialidad (NDA) y compromiso de '
                                                              'seguridad firmados por empleados y contratistas.\n'
                                                              '2. Registros de verificación de antecedentes y '
                                                              'selección previa a la contratación.\n'
                                                              '3. Certificados y registros de finalización de cursos '
                                                              'de concientización en seguridad de la información.\n'
                                                              '4. Lista de verificación de desvinculación '
                                                              '(offboarding) y revocación inmediata de credenciales y '
                                                              'accesos.',
                                      'theme': 'A.6 Personas',
                                      'theme_title': 'A.6 — Controles de Personas'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.6.8): '
                                                     'Assegurar que a organização forneça um canal fácil e acessível '
                                                     'para que colaboradores relatem eventos e fragilidades de '
                                                     'segurança observadas.',
                                      'name': 'Relato de eventos de segurança da informação',
                                      'question': 'A organização garante que a organização forneça um canal fácil e '
                                                  'acessível para que colaboradores relatem eventos e fragilidades de '
                                                  'segurança observadas?',
                                      'recommended_evidence': '1. Termos de confidencialidade (NDA) e responsabilidade '
                                                              'assinados por colaboradores e terceiros.\n'
                                                              '2. Registros de verificação de antecedentes (background '
                                                              'checks) e triagem pré-admissional.\n'
                                                              '3. Certificados e logs de conclusão de treinamentos de '
                                                              'conscientização em segurança da informação.\n'
                                                              '4. Checklist de revogação de acessos e procedimentos '
                                                              'formais de desligamento (offboarding).',
                                      'theme': 'A.6 Pessoas',
                                      'theme_title': 'A.6 — Controles de Pessoas'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Google Cloud SOC 2 Type II Reports & Physical Perimeter Controls',
        'how_to_check': '1. Inspecionar relatórios SOC 2 Tipo II do Google Cloud demonstrando perímetros de segurança '
                        'física multicamadas nos data centers que hospedam as regiões utilizadas (`us-central1`).\n'
                        '2. Inspecionar perímetros de escritórios corporativos e salas de servidores locais.',
        'how_to_maintain': '1. Revisar anualmente os relatórios de conformidade física dos data centers do provedor de '
                           'nuvem via Google Compliance Reports Manager.\n'
                           '2. Manter controle de perímetro nos escritórios da organização.',
        'id': 'A.7.1',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.1): Ensure that security '
                                                     'perimeters are defined and used to protect areas that contain '
                                                     'information and other associated assets.',
                                      'name': 'Physical security perimeters',
                                      'question': 'Does the organization ensure that security perimeters are defined '
                                                  'and used to protect areas that contain information and other '
                                                  'associated assets?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.1): Asegurar que '
                                                     'se definan y utilicen perímetros de seguridad física para '
                                                     'proteger áreas que contengan información y activos asociados.',
                                      'name': 'Perímetros de seguridad física',
                                      'question': '¿Garantiza la organización que se definan y utilicen perímetros de '
                                                  'seguridad física para proteger áreas que contengan información y '
                                                  'activos asociados?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.1): '
                                                     'Assegurar que perímetros de segurança física sejam definidos e '
                                                     'usados para proteger áreas que contenham informações e ativos de '
                                                     'processamento.',
                                      'name': 'Perímetros de segurança física',
                                      'question': 'A organização garante que perímetros de segurança física sejam '
                                                  'definidos e usados para proteger áreas que contenham informações e '
                                                  'ativos de processamento?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Data Center Physical Access Attestation & Office Badge Access',
        'how_to_check': '1. Inspecionar controles de entrada física nos data centers GCP (autenticação biométrica, crachás '
                        'RFID, guardas 24/7).\n'
                        '2. Inspecionar registros de acesso e catracas nas instalações corporativas.',
        'how_to_maintain': '1. Revisão trimestral dos relatórios de conformidade física do Google Cloud.\n'
                           '2. Revogação imediata de credenciais de acesso físico no desligamento de funcionários.',
        'id': 'A.7.2',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.2): Ensure that secure '
                                                     'areas are protected by appropriate entry controls to ensure that '
                                                     'only authorized personnel are allowed access.',
                                      'name': 'Physical entry',
                                      'question': 'Does the organization ensure that secure areas are protected by '
                                                  'appropriate entry controls to ensure that only authorized personnel '
                                                  'are allowed access?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.2): Asegurar que '
                                                     'las áreas seguras estén protegidas por controles de acceso '
                                                     'físico adecuados para garantizar que solo el personal autorizado '
                                                     'acceda.',
                                      'name': 'Entrada física',
                                      'question': '¿Garantiza la organización que las áreas seguras estén protegidas '
                                                  'por controles de acceso físico adecuados para garantizar que solo '
                                                  'el personal autorizado acceda?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.2): '
                                                     'Assegurar que áreas seguras sejam protegidas por controles de '
                                                     'entrada física adequados e autenticação para garantir que apenas '
                                                     'pessoal autorizado tenha acesso.',
                                      'name': 'Entrada física',
                                      'question': 'A organização garante que áreas seguras sejam protegidas por '
                                                  'controles de entrada física adequados e autenticação para garantir '
                                                  'que apenas pessoal autorizado tenha acesso?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Facility Security Procedures & Restricted Room Access',
        'how_to_check': '1. Inspecionar projeto de segurança física das instalações e salas com equipamentos de rede.\n'
                        '2. Checar se salas técnicas permanecem trancadas e com acesso restrito a pessoas autorizadas.',
        'how_to_maintain': '1. Inspeção semestral das fechaduras e alarmes das instalações corporativas.\n'
                           '2. Proibir acesso de visitantes sem acompanhamento às salas críticas.',
        'id': 'A.7.3',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.3): Ensure that physical '
                                                     'security for offices, rooms, and facilities is designed and '
                                                     'applied to prevent unauthorized physical access and damage.',
                                      'name': 'Securing offices, rooms and facilities',
                                      'question': 'Does the organization ensure that physical security for offices, '
                                                  'rooms, and facilities is designed and applied to prevent '
                                                  'unauthorized physical access and damage?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.3): Asegurar que '
                                                     'la seguridad física de oficinas, salas e instalaciones esté '
                                                     'diseñada y aplicada para evitar accesos no autorizados y daños.',
                                      'name': 'Seguridad de oficinas, salas e instalaciones',
                                      'question': '¿Garantiza la organización que la seguridad física de oficinas, '
                                                  'salas e instalaciones esté diseñada y aplicada para evitar accesos '
                                                  'no autorizados y daños?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.3): '
                                                     'Assegurar que a segurança física para escritórios, salas e '
                                                     'instalações seja projetada e aplicada para prevenir acesso não '
                                                     'autorizado e danos.',
                                      'name': 'Proteção de escritórios, salas e instalações',
                                      'question': 'A organização garante que a segurança física para escritórios, '
                                                  'salas e instalações seja projetada e aplicada para prevenir acesso '
                                                  'não autorizado e danos?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Detectar',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'CCTV Surveillance Attestation & Intrusion Detection Systems',
        'how_to_check': '1. Validar monitoramento contínuo por CFTV com retenção de gravações em data centers GCP e '
                        'instalações corporativas.\n'
                        '2. Inspecionar alarmes de intrusão e sensores de presença ativos 24x7.',
        'how_to_maintain': '1. Revisão anual dos relatórios de conformidade e monitoramento de data centers do Google '
                           'Cloud.\n'
                           '2. Testar mensalmente alarmes de intrusão nos escritórios corporativos.',
        'id': 'A.7.4',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.4): Ensure that premises '
                                                     'are continuously monitored by surveillance systems, intrusion '
                                                     'alarms, and environmental sensors to prevent unauthorized '
                                                     'access.',
                                      'name': 'Physical security monitoring',
                                      'question': 'Does the organization ensure that premises are continuously '
                                                  'monitored by surveillance systems, intrusion alarms, and '
                                                  'environmental sensors to prevent unauthorized access?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.4): Asegurar que '
                                                     'las instalaciones sean monitoreadas continuamente mediante '
                                                     'sistemas de videovigilancia y detección de intrusos.',
                                      'name': 'Monitoreo de la seguridad física',
                                      'question': '¿Garantiza la organización que las instalaciones sean monitoreadas '
                                                  'continuamente mediante sistemas de videovigilancia y detección de '
                                                  'intrusos?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.4): '
                                                     'Assegurar que as instalações sejam continuamente monitoradas por '
                                                     'sistemas de vigilância, alarmes e detecção de intrusão física.',
                                      'name': 'Monitoramento de segurança física',
                                      'question': 'A organização garante que as instalações sejam continuamente '
                                                  'monitoradas por sistemas de vigilância, alarmes e detecção de '
                                                  'intrusão física?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Environmental Controls Certification & Google Data Center Infrastructure',
        'how_to_check': '1. Inspecionar sistemas de proteção contra incêndio (gás inerte), controle de temperatura/umidade '
                        'e sensores de inundação nos data centers utilizados.\n'
                        '2. Inspecionar geradores e no-breaks (UPS) redundantes.',
        'how_to_maintain': '1. Validar relatórios ISO 22301 e SOC 2 dos data centers do Google Cloud que garantem '
                           'resiliência ambiental.\n'
                           '2. Manter testes de combate a incêndio nos prédios corporativos.',
        'id': 'A.7.5',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.5): Ensure that '
                                                     'protection against physical and environmental threats (floods, '
                                                     'fire, earthquakes, civil unrest) is designed and applied.',
                                      'name': 'Protecting against physical and environmental threats',
                                      'question': 'Does the organization ensure that protection against physical and '
                                                  'environmental threats (floods, fire, earthquakes, civil unrest) is '
                                                  'designed and applied?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.5): Asegurar que '
                                                     'se diseñe y aplique protección contra amenazas físicas y '
                                                     'desastres naturales (incendios, inundaciones, sismos).',
                                      'name': 'Protección contra amenazas físicas y ambientales',
                                      'question': '¿Garantiza la organización que se diseñe y aplique protección '
                                                  'contra amenazas físicas y desastres naturales (incendios, '
                                                  'inundaciones, sismos)?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.5): '
                                                     'Assegurar que proteção contra ameaças físicas e desastres '
                                                     'ambientais (incêndios, inundações, terremotos) seja projetada e '
                                                     'implementada.',
                                      'name': 'Proteção contra ameaças físicas e ambientais',
                                      'question': 'A organização garante que proteção contra ameaças físicas e '
                                                  'desastres ambientais (incêndios, inundações, terremotos) seja '
                                                  'projetada e implementada?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Secure Area Protocols & Visitor Escort Policy',
        'how_to_check': '1. Inspecionar procedimentos operacionais em áreas seguras (proibição de câmeras e gravação '
                        'não autorizada).\n'
                        '2. Inspecionar registros de entrada e saída em ambientes restritos.',
        'how_to_maintain': '1. Comunicar regras de conduta em áreas seguras a todos os envolvidos.\n'
                           '2. Conduzir inspeções visuais periódicas nas áreas restritas.',
        'id': 'A.7.6',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.6): Ensure that security '
                                                     'measures for working in secure areas are designed and applied, '
                                                     'including prohibitions on unauthorized recording devices.',
                                      'name': 'Working in secure areas',
                                      'question': 'Does the organization ensure that security measures for working in '
                                                  'secure areas are designed and applied, including prohibitions on '
                                                  'unauthorized recording devices?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.6): Asegurar que '
                                                     'se diseñen y apliquen medidas de seguridad para el trabajo en '
                                                     'áreas seguras, prohibiendo dispositivos de grabación no '
                                                     'autorizados.',
                                      'name': 'Trabajo en áreas seguras',
                                      'question': '¿Garantiza la organización que se diseñen y apliquen medidas de '
                                                  'seguridad para el trabajo en áreas seguras, prohibiendo '
                                                  'dispositivos de grabación no autorizados?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.6): '
                                                     'Assegurar que medidas de segurança para trabalho em áreas '
                                                     'restritas sejam projetadas e aplicadas, proibindo dispositivos '
                                                     'de gravação não autorizados.',
                                      'name': 'Trabalho em áreas seguras',
                                      'question': 'A organização garante que medidas de segurança para trabalho em '
                                                  'áreas restritas sejam projetadas e aplicadas, proibindo '
                                                  'dispositivos de gravação não autorizados?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Screen Lock MDM Policy & Clean Desk Audit',
        'how_to_check': '1. Inspecionar política de mesa limpa e tela limpa: checar configuração de bloqueio de tela '
                        'automático em computadores corporativos (máximo 5 minutos de inatividade).\n'
                        '2. Inspecionar se documentos físicos sensíveis são trancados em gavetas.',
        'how_to_maintain': '1. Enforçar bloqueio automático de tela e proteção de senha via política de MDM do Google '
                           'Workspace.\n'
                           '2. Realizar rondas periódicas de conformidade nos escritórios corporativos.',
        'id': 'A.7.7',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.7): Ensure that clear '
                                                     'desk rules for papers and removable storage media and clear '
                                                     'screen rules for information processing facilities are defined '
                                                     'and enforced.',
                                      'name': 'Clear desk and clear screen',
                                      'question': 'Does the organization ensure that clear desk rules for papers and '
                                                  'removable storage media and clear screen rules for information '
                                                  'processing facilities are defined and enforced?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.7): Asegurar que '
                                                     'se definan y apliquen normas de escritorio limpio para '
                                                     'documentos y pantallas limpias para equipos de procesamiento de '
                                                     'información.',
                                      'name': 'Escritorio limpio y pantalla limpia',
                                      'question': '¿Garantiza la organización que se definan y apliquen normas de '
                                                  'escritorio limpio para documentos y pantallas limpias para equipos '
                                                  'de procesamiento de información?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.7): '
                                                     'Assegurar que regras de mesa limpa para papéis e mídias '
                                                     'removíveis e regras de tela limpa para instalações de '
                                                     'processamento de informações sejam aplicadas.',
                                      'name': 'Mesa limpa e tela limpa',
                                      'question': 'A organização garante que regras de mesa limpa para papéis e mídias '
                                                  'removíveis e regras de tela limpa para instalações de processamento '
                                                  'de informações sejam aplicadas?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Infrastructure Siting Controls & Google Cloud Redundancy',
        'how_to_check': '1. Inspecionar proteção de servidores e equipamentos de conectividade contra sobrecargas '
                        'elétricas e umidade.\n'
                        '2. Validar redundância de alimentação elétrica nas zonas de disponibilidade do Google Cloud.',
        'how_to_maintain': '1. Hospedar cargas de trabalho em regiões Google Cloud com infraestrutura de nível '
                           'Enterprise N+1.\n'
                           '2. Manter manutenção preventiva nos equipamentos de TI locais.',
        'id': 'A.7.8',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.8): Ensure that '
                                                     'equipment is sited and protected to reduce risks from '
                                                     'environmental threats, hazards, and unauthorized access '
                                                     'opportunities.',
                                      'name': 'Equipment siting and protection',
                                      'question': 'Does the organization ensure that equipment is sited and protected '
                                                  'to reduce risks from environmental threats, hazards, and '
                                                  'unauthorized access opportunities?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.8): Asegurar que '
                                                     'los equipos estén ubicados y protegidos para reducir los riesgos '
                                                     'derivados de amenazas ambientales y accesos no autorizados.',
                                      'name': 'Emplazamiento y protección de equipos',
                                      'question': '¿Garantiza la organización que los equipos estén ubicados y '
                                                  'protegidos para reducir los riesgos derivados de amenazas '
                                                  'ambientales y accesos no autorizados?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.8): '
                                                     'Assegurar que equipamentos sejam posicionados de forma segura e '
                                                     'protegidos para reduzir riscos ambientais e oportunidades de '
                                                     'acesso não autorizado.',
                                      'name': 'Posicionamento e proteção de equipamentos',
                                      'question': 'A organização garante que equipamentos sejam posicionados de forma '
                                                  'segura e protegidos para reduzir riscos ambientais e oportunidades '
                                                  'de acesso não autorizado?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Proteção de Ativos',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Full Disk Encryption (FileVault / BitLocker) & Remote Wipe',
        'how_to_check': '1. Inspecionar se todos os notebooks e dispositivos corporativos utilizados fora do '
                        'escritório possuem criptografia total de disco (FileVault/BitLocker) ativa.\n'
                        '2. Validar proteção contra perda e roubo com rastreamento e bloqueio remoto.',
        'how_to_maintain': '1. Enforçar criptografia de disco obrigatória via política de endpoint management do '
                           'Google Workspace.\n'
                           '2. Executar bloqueio ou limpeza remota (Remote Wipe) imediata em caso de furto ou '
                           'extravio.',
        'id': 'A.7.9',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.9): Ensure that off-site '
                                                     'assets are protected taking into account the different risks of '
                                                     'working outside the organization premises.',
                                      'name': 'Security of assets off-premises',
                                      'question': 'Does the organization ensure that off-site assets are protected '
                                                  'taking into account the different risks of working outside the '
                                                  'organization premises?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.9): Asegurar que '
                                                     'los activos fuera de las instalaciones estén protegidos teniendo '
                                                     'en cuenta los riesgos de trabajar fuera de la organización.',
                                      'name': 'Seguridad de los activos fuera de las instalaciones',
                                      'question': '¿Garantiza la organización que los activos fuera de las '
                                                  'instalaciones estén protegidos teniendo en cuenta los riesgos de '
                                                  'trabajar fuera de la organización?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.9): '
                                                     'Assegurar que ativos fora das instalações corporativas sejam '
                                                     'protegidos contra roubo, perda ou comprometimento.',
                                      'name': 'Segurança de ativos fora das instalações',
                                      'question': 'A organização garante que ativos fora das instalações corporativas '
                                                  'sejam protegidos contra roubo, perda ou comprometimento?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Ativos',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Endpoint USB Storage Restrictions & Media Sanitization',
        'how_to_check': '1. Inspecionar procedimento de controle de mídias removíveis (bloqueio de portas USB para '
                        'gravação em massa).\n'
                        '2. Checar procedimentos de descarte de mídias magnéticas e de estado sólido.',
        'how_to_maintain': '1. Desabilitar portas USB para dispositivos de armazenamento não autorizados via política '
                           'de MDM.\n'
                           '2. Exigir destruição física ou desmagnetização certificada para mídias descartadas.',
        'id': 'A.7.10',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.10): Ensure that storage '
                                                     'media are managed through their lifecycle of acquisition, use, '
                                                     'transportation, and disposal in accordance with classification.',
                                      'name': 'Storage media',
                                      'question': 'Does the organization ensure that storage media are managed through '
                                                  'their lifecycle of acquisition, use, transportation, and disposal '
                                                  'in accordance with classification?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.10): Asegurar que '
                                                     'los medios de almacenamiento se gestionen a lo largo de su ciclo '
                                                     'de vida de adquisición, uso, transporte y eliminación.',
                                      'name': 'Medios de almacenamiento',
                                      'question': '¿Garantiza la organización que los medios de almacenamiento se '
                                                  'gestionen a lo largo de su ciclo de vida de adquisición, uso, '
                                                  'transporte y eliminación?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.10): '
                                                     'Assegurar que mídias de armazenamento sejam gerenciadas ao longo '
                                                     'de seu ciclo de vida de aquisição, uso, transporte e descarte de '
                                                     'acordo com a classificação.',
                                      'name': 'Mídias de armazenamento',
                                      'question': 'A organização garante que mídias de armazenamento sejam gerenciadas '
                                                  'ao longo de seu ciclo de vida de aquisição, uso, transporte e '
                                                  'descarte de acordo com a classificação?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança Física',
                          'concepts': 'Proteger',
                          'domains': 'Resiliência',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Utility Failure Safeguards & Data Center Power SLA',
        'how_to_check': '1. Validar relatórios de fornecimento ininterrupto de energia (UPS/geradores a diesel) nos '
                        'data centers GCP.\n'
                        '2. Checar testes regulares de comutação para geradores em caso de apagão elétrico.',
        'how_to_maintain': '1. Contratar serviços em zonas redundantes do Google Cloud com geradores de backup '
                           'autônomos.\n'
                           '2. Testar mensalmente no-breaks das salas técnicas corporativas.',
        'id': 'A.7.11',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.11): Ensure that '
                                                     'information processing facilities are protected from power '
                                                     'failures and other disruptions caused by failures in supporting '
                                                     'utilities.',
                                      'name': 'Supporting utilities',
                                      'question': 'Does the organization ensure that information processing facilities '
                                                  'are protected from power failures and other disruptions caused by '
                                                  'failures in supporting utilities?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.11): Asegurar que '
                                                     'las instalaciones de procesamiento estén protegidas contra '
                                                     'cortes de energía e interrupciones de suministros esenciales.',
                                      'name': 'Instalaciones de suministro y soporte',
                                      'question': '¿Garantiza la organización que las instalaciones de procesamiento '
                                                  'estén protegidas contra cortes de energía e interrupciones de '
                                                  'suministros esenciales?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.11): '
                                                     'Assegurar que instalações de processamento de informações sejam '
                                                     'protegidas contra falhas de energia e outras interrupções de '
                                                     'utilidades essenciais.',
                                      'name': 'Utilidades de suporte (energia, climatização)',
                                      'question': 'A organização garante que instalações de processamento de '
                                                  'informações sejam protegidas contra falhas de energia e outras '
                                                  'interrupções de utilidades essenciais?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Google Backbone Physical Encryption (MACsec) & Cable Trays',
        'how_to_check': '1. Inspecionar infraestrutura de cabeamento de rede: canaletas protegidas e trancadas contra '
                        'interceptação de cabos.\n'
                        '2. Validar que todo tráfego entre data centers do Google Cloud é criptografado '
                        'automaticamente na camada física (MACsec / PSP).',
        'how_to_maintain': '1. Beneficiar-se da criptografia automática de links privados e fibra óptica submarina do '
                           'Google Cloud.\n'
                           '2. Proteger cabeamento físico nas sedes corporativas com identificação e controle de '
                           'acesso.',
        'id': 'A.7.12',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.12): Ensure that cables '
                                                     'carrying power, data, or supporting information services are '
                                                     'protected from interception, interference, or damage.',
                                      'name': 'Cabling security',
                                      'question': 'Does the organization ensure that cables carrying power, data, or '
                                                  'supporting information services are protected from interception, '
                                                  'interference, or damage?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.12): Asegurar que '
                                                     'el cableado que transporta energía o datos esté protegido contra '
                                                     'interceptaciones, interferencias o daños.',
                                      'name': 'Seguridad del cableado',
                                      'question': '¿Garantiza la organización que el cableado que transporta energía o '
                                                  'datos esté protegido contra interceptaciones, interferencias o '
                                                  'daños?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.12): '
                                                     'Assegurar que cabos de transmissão de dados e de energia '
                                                     'elétrica que transportam informações sejam protegidos contra '
                                                     'interceptação ou danos.',
                                      'name': 'Segurança do cabeamento',
                                      'question': 'A organização garante que cabos de transmissão de dados e de '
                                                  'energia elétrica que transportam informações sejam protegidos '
                                                  'contra interceptação ou danos?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Ativos',
                          'concepts': 'Proteger',
                          'domains': 'Resiliência',
                          'properties': 'Disponibilidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Hardware Maintenance Agreements & Telemetry Tracking',
        'how_to_check': '1. Inspecionar cronograma de manutenção preventiva de hardware e equipamentos de '
                        'telecomunicações.\n'
                        '2. Checar contratos de suporte com fabricantes de hardware.',
        'how_to_maintain': '1. Monitorar telemetria de saúde de hardware e discos com Cloud Monitoring.\n'
                           '2. Renovar contratos de suporte e garantia com SLA 24x7 para equipamentos críticos.',
        'id': 'A.7.13',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.13): Ensure that '
                                                     'equipment is correctly maintained to ensure its continuous '
                                                     'availability and integrity in accordance with manufacturer '
                                                     'specifications.',
                                      'name': 'Equipment maintenance',
                                      'question': 'Does the organization ensure that equipment is correctly maintained '
                                                  'to ensure its continuous availability and integrity in accordance '
                                                  'with manufacturer specifications?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.13): Asegurar que '
                                                     'el equipamiento se mantenga adecuadamente para asegurar su '
                                                     'continua disponibilidad e integridad conforme a las '
                                                     'especificaciones.',
                                      'name': 'Mantenimiento de equipos',
                                      'question': '¿Garantiza la organización que el equipamiento se mantenga '
                                                  'adecuadamente para asegurar su continua disponibilidad e integridad '
                                                  'conforme a las especificaciones?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.13): '
                                                     'Assegurar que equipamentos sejam mantidos corretamente por '
                                                     'pessoal qualificado para garantir sua disponibilidade e '
                                                     'integridade contínuas.',
                                      'name': 'Manutenção de equipamentos',
                                      'question': 'A organização garante que equipamentos sejam mantidos corretamente '
                                                  'por pessoal qualificado para garantir sua disponibilidade e '
                                                  'integridade contínuas?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Ativos',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Google Cloud NIST 800-88 Sanitization & Destruction Certificates',
        'how_to_check': '1. Inspecionar documentação de descarte seguro do Google Cloud (trituração de discos e '
                        'desmagnetização conforme NIST SP 800-88 R1).\n'
                        '2. Inspecionar certificados de destruição de hardware local emitidos por empresas '
                        'especializadas.',
        'how_to_maintain': '1. Exigir laudo de destruição segura para todo hardware aposentado.\n'
                           '2. Realizar sanitização criptográfica de discos antes de qualquer remanejamento.',
        'id': 'A.7.14',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.7',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.7.14): Ensure that items '
                                                     'of equipment containing storage media are verified to ensure '
                                                     'that any sensitive data and licensed software have been '
                                                     'sanitized.',
                                      'name': 'Secure disposal or re-use of equipment',
                                      'question': 'Does the organization ensure that items of equipment containing '
                                                  'storage media are verified to ensure that any sensitive data and '
                                                  'licensed software have been sanitized?',
                                      'recommended_evidence': '1. Third-party data center audit reports (Google Cloud '
                                                              'SOC 2 / SOC 3 / ISO 27001 Certification & Compliance '
                                                              'Reports).\n'
                                                              '2. Physical facility badge access logs, CCTV monitoring '
                                                              'records, and visitor registration logs.\n'
                                                              '3. Environmental threat protection procedures (UPS '
                                                              'power backups, fire suppression, HVAC redundancy).\n'
                                                              '4. Certificates of secure media disposal, degaussing, '
                                                              'and cryptographic sanitization.',
                                      'theme': 'A.7 Physical',
                                      'theme_title': 'A.7 — Physical Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.7.14): Asegurar que '
                                                     'los equipos que contengan medios de almacenamiento sean '
                                                     'verificados para asegurar que los datos confidenciales hayan '
                                                     'sido destruidos.',
                                      'name': 'Eliminación segura o reutilización de equipos',
                                      'question': '¿Garantiza la organización que los equipos que contengan medios de '
                                                  'almacenamiento sean verificados para asegurar que los datos '
                                                  'confidenciales hayan sido destruidos?',
                                      'recommended_evidence': '1. Informes de evaluación independiente de centros de '
                                                              'datos (Google Cloud SOC 2 / SOC 3 / Certificaciones ISO '
                                                              '27001).\n'
                                                              '2. Registros de control de acceso físico mediante '
                                                              'tarjetas electrónicas y libros de visitas a '
                                                              'instalaciones.\n'
                                                              '3. Procedimientos de protección contra amenazas '
                                                              'ambientales (sistemas contra incendios, respaldo UPS, '
                                                              'climatización).\n'
                                                              '4. Certificados de destrucción segura, desmagnetización '
                                                              'y desecho de soportes de almacenamiento.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.7.14): '
                                                     'Assegurar que itens de equipamento que contenham mídias de '
                                                     'armazenamento sejam verificados para assegurar que dados '
                                                     'confidenciais tenham sido sanitizados.',
                                      'name': 'Descarte seguro ou reutilização de equipamentos',
                                      'question': 'A organização garante que itens de equipamento que contenham mídias '
                                                  'de armazenamento sejam verificados para assegurar que dados '
                                                  'confidenciais tenham sido sanitizados?',
                                      'recommended_evidence': '1. Relatórios de conformidade e avaliação independente '
                                                              'de data centers (Google Cloud SOC 2 / SOC 3 / ISO 27001 '
                                                              'Audit Reports).\n'
                                                              '2. Registros de controle de acesso físico, crachás '
                                                              'eletrônicos e logs de visitantes em instalações '
                                                              'corporativas.\n'
                                                              '3. Procedimentos documentados para proteção contra '
                                                              'ameaças ambientais (incêndio, falha de energia, '
                                                              'climatização).\n'
                                                              '4. Certificados de descarte seguro, sanitização e '
                                                              'desmagnetização de mídias e discos rígidos.',
                                      'theme': 'A.7 Físico',
                                      'theme_title': 'A.7 — Controles Físicos'}}},
    {   'attributes': {   'capabilities': 'Proteção de Ativos',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'BeyondCorp Endpoint Verification & Context-Aware Access',
        'how_to_check': '1. Verificar se 100% dos dispositivos que acessam o GCP possuem BeyondCorp Endpoint '
                        'Verification ativo.\n'
                        '2. Inspecionar regras de Context-Aware Access exigindo sistema operacional atualizado e disco '
                        'criptografado.',
        'how_to_maintain': '1. Bloquear requisições ao console e APIs do Google Cloud originadas de dispositivos não '
                           'conformes.\n'
                           '2. Executar revisão semanal do inventário de dispositivos no Google Admin Console.',
        'id': 'A.8.1',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.1): Ensure that '
                                                     'information stored on, processed by, or accessed via user '
                                                     'endpoint devices is continuously protected through technical '
                                                     'policies.',
                                      'name': 'User end point devices',
                                      'question': 'Does the organization ensure that information stored on, processed '
                                                  'by, or accessed via user endpoint devices is continuously protected '
                                                  'through technical policies?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.1): Asegurar que '
                                                     'la información procesada o accesible a través de dispositivos de '
                                                     'punto final de usuario esté continuamente protegida.',
                                      'name': 'Dispositivos de punto final de usuario',
                                      'question': '¿Garantiza la organización que la información procesada o accesible '
                                                  'a través de dispositivos de punto final de usuario esté '
                                                  'continuamente protegida?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.1): '
                                                     'Assegurar que informações armazenadas em, processadas por ou '
                                                     'acessadas via dispositivos de ponto de extremidade de usuários '
                                                     'sejam protegidas.',
                                      'name': 'Dispositivos de ponto de extremidade do usuário',
                                      'question': 'A organização garante que informações armazenadas em, processadas '
                                                  'por ou acessadas via dispositivos de ponto de extremidade de '
                                                  'usuários sejam protegidas?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade e Acesso',
                          'concepts': 'Proteger, Detectar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Privileged Access Manager (PAM) & Just-In-Time Elevation',
        'how_to_check': '1. Inspecionar contas com papéis administrativos no GCP '
                        '(`roles/resourcemanager.organizationAdmin`, `roles/owner`).\n'
                        '2. Checar se acessos com privilégios elevados utilizam concessão just-in-time via Privileged '
                        'Access Manager (PAM).',
        'how_to_maintain': '1. Restringir atribuições permanentes de privilégios elevados: impor expiração automática '
                           'de sessões de acesso privilegiado.\n'
                           '2. Habilitar alertas no Cloud Monitoring para qualquer concessão de papel administrativo.',
        'id': 'A.8.2',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.2): Ensure that '
                                                     'allocation and use of privileged access rights are strictly '
                                                     'restricted and controlled based on least privilege and '
                                                     'just-in-time access.',
                                      'name': 'Privileged access rights',
                                      'question': 'Does the organization ensure that allocation and use of privileged '
                                                  'access rights are strictly restricted and controlled based on least '
                                                  'privilege and just-in-time access?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.2): Asegurar que '
                                                     'la asignación y uso de derechos de acceso privilegiado estén '
                                                     'estrictamente restringidos y controlados según el mínimo '
                                                     'privilegio.',
                                      'name': 'Derechos de acceso privilegiado',
                                      'question': '¿Garantiza la organización que la asignación y uso de derechos de '
                                                  'acceso privilegiado estén estrictamente restringidos y controlados '
                                                  'según el mínimo privilegio?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.2): '
                                                     'Assegurar que a alocação e uso de direitos de acesso '
                                                     'privilegiado sejam estritamente controlados e monitorados com '
                                                     'base no princípio do menor privilégio.',
                                      'name': 'Direitos de acesso privilegiado',
                                      'question': 'A organização garante que a alocação e uso de direitos de acesso '
                                                  'privilegiado sejam estritamente controlados e monitorados com base '
                                                  'no princípio do menor privilégio?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Uniform Bucket-Level Access (UBLA) & BigQuery IAM Restrictions',
        'how_to_check': '1. Inspecionar ACLs e permissões IAM granulares em buckets GCS e tabelas BigQuery.\n'
                        '2. Validar que apenas contas de serviço e identidades estritamente necessárias possuem '
                        'permissão de leitura.',
        'how_to_maintain': '1. Ativar Uniform Bucket-Level Access (UBLA) em 100% dos buckets do Cloud Storage.\n'
                           '2. Utilizar tags de política de segurança (Policy Tags) para restringir colunas com dados '
                           'sensíveis no BigQuery.',
        'id': 'A.8.3',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.3): Ensure that access '
                                                     'to information and other application functions is restricted in '
                                                     'accordance with the established access control policy.',
                                      'name': 'Information access restriction',
                                      'question': 'Does the organization ensure that access to information and other '
                                                  'application functions is restricted in accordance with the '
                                                  'established access control policy?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.3): Asegurar que '
                                                     'el acceso a la información y funciones de aplicaciones se '
                                                     'restrinja de acuerdo con la política de control de acceso '
                                                     'establecida.',
                                      'name': 'Restricción de acceso a la información',
                                      'question': '¿Garantiza la organización que el acceso a la información y '
                                                  'funciones de aplicaciones se restrinja de acuerdo con la política '
                                                  'de control de acceso establecida?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.3): '
                                                     'Assegurar que o acesso a informações e outras funções de '
                                                     'aplicações seja restrito de acordo com a política de controle de '
                                                     'acesso estabelecida.',
                                      'name': 'Restrição de acesso à informação',
                                      'question': 'A organização garante que o acesso a informações e outras funções '
                                                  'de aplicações seja restrito de acordo com a política de controle de '
                                                  'acesso estabelecida?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Branch Protection Rules & Cloud Build Source Integrations',
        'how_to_check': '1. Inspecionar permissões de acesso em repositórios de código (GitHub / Cloud Source Repositories '
                        '/ GitLab).\n'
                        '2. Checar exigência de MFA para desenvolvedores e proteção de branches principais (`main`, '
                        '`master`).',
        'how_to_maintain': '1. Proibir commits diretos sem pull request aprovado e testes de CI concluídos.\n'
                           '2. Restringir acesso a repositórios sensíveis com controle baseado em equipes '
                           '(Teams/RBAC).',
        'id': 'A.8.4',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.4): Ensure that read and '
                                                     'write access to software source code, development tools, and '
                                                     'build libraries is strictly restricted to authorized personnel.',
                                      'name': 'Access to source code',
                                      'question': 'Does the organization ensure that read and write access to software '
                                                  'source code, development tools, and build libraries is strictly '
                                                  'restricted to authorized personnel?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.4): Asegurar que '
                                                     'el acceso de lectura y escritura al código fuente, herramientas '
                                                     'de desarrollo y bibliotecas esté estrictamente restringido.',
                                      'name': 'Acceso al código fuente',
                                      'question': '¿Garantiza la organización que el acceso de lectura y escritura al '
                                                  'código fuente, herramientas de desarrollo y bibliotecas esté '
                                                  'estrictamente restringido?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.4): '
                                                     'Assegurar que o acesso de leitura e gravação ao código-fonte do '
                                                     'software, ferramentas de desenvolvimento e bibliotecas seja '
                                                     'estritamente restrito.',
                                      'name': 'Acesso ao código-fonte',
                                      'question': 'A organização garante que o acesso de leitura e gravação ao '
                                                  'código-fonte do software, ferramentas de desenvolvimento e '
                                                  'bibliotecas seja estritamente restrito?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade e Acesso',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'FIDO2 Titan Security Keys & mTLS Zero Trust Architecture',
        'how_to_check': '1. Validar métodos de autenticação em uso no Cloud Identity: confirmar bloqueio de protocolos '
                        'legados (POP/IMAP, senhas simples).\n'
                        '2. Checar exigência de autenticação mTLS e chaves de segurança Titan FIDO2.',
        'how_to_maintain': '1. Enforçar política de organização `constraints/iam.enforceMfa` no Google Cloud.\n'
                           '2. Utilizar autenticação sem senha (Passkeys / FIDO2) para 100% das identidades '
                           'administrativas.',
        'id': 'A.8.5',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.5): Ensure that secure '
                                                     'authentication technologies and procedures, including '
                                                     'phishing-resistant multi-factor authentication (MFA/FIDO2), are '
                                                     'enforced.',
                                      'name': 'Secure authentication',
                                      'question': 'Does the organization ensure that secure authentication '
                                                  'technologies and procedures, including phishing-resistant '
                                                  'multi-factor authentication (MFA/FIDO2), are enforced?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.5): Asegurar que '
                                                     'se apliquen tecnologías y procedimientos de autenticación '
                                                     'segura, incluida la autenticación multifactor resistente a '
                                                     'phishing (MFA).',
                                      'name': 'Autenticación segura',
                                      'question': '¿Garantiza la organización que se apliquen tecnologías y '
                                                  'procedimientos de autenticación segura, incluida la autenticación '
                                                  'multifactor resistente a phishing (MFA)?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.5): '
                                                     'Assegurar que tecnologias e procedimentos de autenticação '
                                                     'segura, incluindo autenticação multifator resistente a phishing '
                                                     '(FIDO2/MFA), sejam aplicados.',
                                      'name': 'Autenticação segura',
                                      'question': 'A organização garante que tecnologias e procedimentos de '
                                                  'autenticação segura, incluindo autenticação multifator resistente a '
                                                  'phishing (FIDO2/MFA), sejam aplicados?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Ativos',
                          'concepts': 'Detectar',
                          'domains': 'Resiliência',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Cloud Monitoring Capacity Alerts & GKE Autoscaling',
        'how_to_check': '1. Inspecionar cotas de recursos e métricas de consumo de CPU, RAM e largura de banda no '
                        'Cloud Monitoring.\n'
                        '2. Checar alertas preventivos de aproximação de limite de cota (> 80%).',
        'how_to_maintain': '1. Configurar autoscaling em grupos de instâncias (MIGs) e clusters GKE.\n'
                           '2. Monitorar tendências de consumo com relatórios de capacidade e custos do FinOps.',
        'id': 'A.8.6',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.6): Ensure that use of '
                                                     'processing, storage, and networking resources is monitored and '
                                                     'adjusted to ensure required system performance and capacity.',
                                      'name': 'Capacity management',
                                      'question': 'Does the organization ensure that use of processing, storage, and '
                                                  'networking resources is monitored and adjusted to ensure required '
                                                  'system performance and capacity?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.6): Asegurar que '
                                                     'el uso de recursos de procesamiento, almacenamiento y red sea '
                                                     'monitoreado y ajustado para satisfacer los requisitos de '
                                                     'capacidad.',
                                      'name': 'Gestión de la capacidad',
                                      'question': '¿Garantiza la organización que el uso de recursos de procesamiento, '
                                                  'almacenamiento y red sea monitoreado y ajustado para satisfacer los '
                                                  'requisitos de capacidad?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.6): '
                                                     'Assegurar que a utilização de recursos de processamento, '
                                                     'armazenamento e rede seja monitorada e ajustada para atender aos '
                                                     'requisitos atuais e futuros.',
                                      'name': 'Gestão de capacidade',
                                      'question': 'A organização garante que a utilização de recursos de '
                                                  'processamento, armazenamento e rede seja monitorada e ajustada para '
                                                  'atender aos requisitos atuais e futuros?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Sistemas e Redes',
                          'concepts': 'Proteger, Detectar',
                          'domains': 'Defesa',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'EDR Integration & Automated GCS Anti-Malware Pipeline',
        'how_to_check': '1. Inspecionar proteção antimalware e EDR em máquinas virtuais Compute Engine e endpoints de '
                        'usuários.\n'
                        '2. Inspecionar varredura automática de malware em uploads de arquivos para buckets Cloud '
                        'Storage.',
        'how_to_maintain': '1. Integrar Cloud Storage com Cloud Functions e Cloud Workflows para varredura de vírus em '
                           'novos uploads.\n'
                           '2. Manter agentes de EDR corporativo (CrowdStrike / Defender) atualizados em todas as '
                           'instâncias.',
        'id': 'A.8.7',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.7): Ensure that '
                                                     'protection against malware is implemented and supported by '
                                                     'appropriate user awareness, automated scanning, and endpoint '
                                                     'protection.',
                                      'name': 'Protection against malware',
                                      'question': 'Does the organization ensure that protection against malware is '
                                                  'implemented and supported by appropriate user awareness, automated '
                                                  'scanning, and endpoint protection?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.7): Asegurar que '
                                                     'se implemente protección contra malware respaldada por análisis '
                                                     'automatizados y concienciación de los usuarios.',
                                      'name': 'Protección contra malware',
                                      'question': '¿Garantiza la organización que se implemente protección contra '
                                                  'malware respaldada por análisis automatizados y concienciación de '
                                                  'los usuarios?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.7): '
                                                     'Assegurar que proteção contra software malicioso seja '
                                                     'implementada e suportada por conscientização adequada dos '
                                                     'usuários e controles de segurança.',
                                      'name': 'Proteção contra malware',
                                      'question': 'A organização garante que proteção contra software malicioso seja '
                                                  'implementada e suportada por conscientização adequada dos usuários '
                                                  'e controles de segurança?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Vulnerabilidades',
                          'concepts': 'Identificar, Responder',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo, Corretivo'},
        'gcp_mapping': 'Security Command Center Vulnerability Management & Patching',
        'how_to_check': '1. Inspecionar descobertas de vulnerabilidades do Security Command Center (SCC) e Artifact '
                        'Registry Scanning.\n'
                        '2. Checar tempo médio de correção (SLA de correção para falhas críticas < 7 dias).',
        'how_to_maintain': '1. Automatizar escaneamento diário de vulnerabilidades em contêineres e imagens de SO.\n'
                           '2. Bloquear implantação de contêineres contendo CVEs críticas via Binary Authorization.',
        'id': 'A.8.8',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.8): Ensure that '
                                                     'information about technical vulnerabilities of information '
                                                     'systems in use is obtained, evaluated, and remediation measures '
                                                     'are applied.',
                                      'name': 'Management of technical vulnerabilities',
                                      'question': 'Does the organization ensure that information about technical '
                                                  'vulnerabilities of information systems in use is obtained, '
                                                  'evaluated, and remediation measures are applied?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.8): Asegurar que '
                                                     'se obtenga información sobre vulnerabilidades técnicas de los '
                                                     'sistemas en uso, se evalúe y se apliquen medidas de remediación.',
                                      'name': 'Gestión de vulnerabilidades técnicas',
                                      'question': '¿Garantiza la organización que se obtenga información sobre '
                                                  'vulnerabilidades técnicas de los sistemas en uso, se evalúe y se '
                                                  'apliquen medidas de remediación?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.8): '
                                                     'Assegurar que informações sobre vulnerabilidades técnicas de '
                                                     'sistemas de informação em uso sejam obtidas, avaliadas e medidas '
                                                     'de correção sejam tomadas.',
                                      'name': 'Gestão de vulnerabilidades técnicas',
                                      'question': 'A organização garante que informações sobre vulnerabilidades '
                                                  'técnicas de sistemas de informação em uso sejam obtidas, avaliadas '
                                                  'e medidas de correção sejam tomadas?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Gestão de Configuração',
                          'concepts': 'Identificar, Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Terraform IaC Drift Detection & Config Controller',
        'how_to_check': '1. Executar scanner de infraestrutura como código (IaC Scanner) em templates Terraform (.tf) '
                        'e manifestos Ansible.\n'
                        '2. Validar desvios de configuração (drift) contra a baseline aprovada.',
        'how_to_maintain': '1. Impor configuração via pipelines declarativos de GitOps (Terraform Cloud / Config '
                           'Controller).\n'
                           '2. Proibir modificações manuais no console de produção (ClickOps) revogando permissões de '
                           'escrita direta.',
        'id': 'A.8.9',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.9): Ensure that '
                                                     'configurations, including security baselines of hardware, '
                                                     'software, cloud services, and networks, are established, '
                                                     'monitored, and maintained.',
                                      'name': 'Configuration management',
                                      'question': 'Does the organization ensure that configurations, including '
                                                  'security baselines of hardware, software, cloud services, and '
                                                  'networks, are established, monitored, and maintained?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.9): Asegurar que '
                                                     'las configuraciones de hardware, software, servicios en la nube '
                                                     'y redes se establezcan, monitoreen y mantengan bajo líneas base.',
                                      'name': 'Gestión de configuraciones',
                                      'question': '¿Garantiza la organización que las configuraciones de hardware, '
                                                  'software, servicios en la nube y redes se establezcan, monitoreen y '
                                                  'mantengan bajo líneas base?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.9): '
                                                     'Assegurar que configurações, incluindo de segurança, de '
                                                     'hardware, software, serviços e redes sejam estabelecidas, '
                                                     'documentadas, monitoradas e mantidas.',
                                      'name': 'Gestão de configurações',
                                      'question': 'A organização garante que configurações, incluindo de segurança, de '
                                                  'hardware, software, serviços e redes sejam estabelecidas, '
                                                  'documentadas, monitoradas e mantidas?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'GCS Object Lifecycle Management & BigQuery Partition Expiration',
        'how_to_check': '1. Inspecionar políticas de ciclo de vida (Lifecycle Rules) em buckets Cloud Storage '
                        '(exclusão após N dias).\n'
                        '2. Validar expiração de partições e tabelas temporárias no BigQuery.',
        'how_to_maintain': '1. Enforçar regras de exclusão segura automática baseadas na sensibilidade e requisitos '
                           'regulatórios.\n'
                           '2. Conduzir revisão de limpeza de dados expirados semestralmente.',
        'id': 'A.8.10',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.10): Ensure that '
                                                     'information stored in information systems, cloud storage, or '
                                                     'devices is securely deleted when no longer required by law or '
                                                     'business.',
                                      'name': 'Information deletion',
                                      'question': 'Does the organization ensure that information stored in information '
                                                  'systems, cloud storage, or devices is securely deleted when no '
                                                  'longer required by law or business?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.10): Asegurar que '
                                                     'la información almacenada en sistemas, nube o dispositivos se '
                                                     'elimine de forma segura cuando ya no sea necesaria.',
                                      'name': 'Eliminación de información',
                                      'question': '¿Garantiza la organización que la información almacenada en '
                                                  'sistemas, nube o dispositivos se elimine de forma segura cuando ya '
                                                  'no sea necesaria?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.10): '
                                                     'Assegurar que informações armazenadas em sistemas de informação, '
                                                     'dispositivos ou outras mídias de armazenamento sejam excluídas '
                                                     'com segurança quando não mais necessárias.',
                                      'name': 'Exclusão de informações',
                                      'question': 'A organização garante que informações armazenadas em sistemas de '
                                                  'informação, dispositivos ou outras mídias de armazenamento sejam '
                                                  'excluídas com segurança quando não mais necessárias?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'BigQuery Dynamic Data Masking & Cloud DLP De-identification',
        'how_to_check': '1. Inspecionar regras de mascaramento de dados (Dynamic Data Masking) em datasets do '
                        'BigQuery.\n'
                        '2. Validar pseudonimização de dados pessoais via Cloud Sensitive Data Protection (DLP).',
        'how_to_maintain': '1. Ativar mascaramento automático de CPF, cartões de crédito e emails para usuários não '
                           'privilegiados no BigQuery.\n'
                           '2. Proibir acesso a dados brutos em ambientes de desenvolvimento e homologação.',
        'id': 'A.8.11',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.11): Ensure that data '
                                                     'masking, pseudonymization, or anonymization techniques are '
                                                     'applied in accordance with the organization access control '
                                                     'policy and privacy laws.',
                                      'name': 'Data masking',
                                      'question': 'Does the organization ensure that data masking, pseudonymization, '
                                                  'or anonymization techniques are applied in accordance with the '
                                                  'organization access control policy and privacy laws?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.11): Asegurar que '
                                                     'se apliquen técnicas de enmascaramiento, seudonimización o '
                                                     'anonimización de datos de acuerdo con las políticas y leyes de '
                                                     'privacidad.',
                                      'name': 'Enmascaramiento de datos',
                                      'question': '¿Garantiza la organización que se apliquen técnicas de '
                                                  'enmascaramiento, seudonimización o anonimización de datos de '
                                                  'acuerdo con las políticas y leyes de privacidad?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.11): '
                                                     'Assegurar que técnicas de mascaramento de dados, pseudonimização '
                                                     'ou anonimização sejam aplicadas de acordo com as políticas de '
                                                     'controle de acesso e requisitos legais.',
                                      'name': 'Mascaramento de dados',
                                      'question': 'A organização garante que técnicas de mascaramento de dados, '
                                                  'pseudonimização ou anonimização sejam aplicadas de acordo com as '
                                                  'políticas de controle de acesso e requisitos legais?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Prevenção contra Vazamento de Dados',
                          'concepts': 'Proteger, Detectar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'VPC Service Controls (VPC-SC) & Model Armor DLP',
        'how_to_check': '1. Inspecionar perímetros de segurança de VPC Service Controls (VPC-SC) ativos.\n'
                        '2. Validar que acessos a APIs do Cloud Storage e BigQuery são restritos à rede privada e '
                        'identidades autorizadas.',
        'how_to_maintain': '1. Ativar regras de egresso restritas para evitar exfiltração de dados para projetos '
                           'externos não autorizados.\n'
                           '2. Habilitar inspeção em tempo real de tráfego de saída com Cloud DLP e Model Armor.',
        'id': 'A.8.12',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.12): Ensure that data '
                                                     'leakage prevention (DLP) measures are applied to systems, '
                                                     'networks, and endpoints that process, store, or transmit '
                                                     'sensitive data.',
                                      'name': 'Data leakage prevention',
                                      'question': 'Does the organization ensure that data leakage prevention (DLP) '
                                                  'measures are applied to systems, networks, and endpoints that '
                                                  'process, store, or transmit sensitive data?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.12): Asegurar que '
                                                     'se apliquen medidas de prevención de fuga de datos (DLP) en '
                                                     'sistemas, redes y puntos finales que procesen información '
                                                     'confidencial.',
                                      'name': 'Prevención de fuga de datos (DLP)',
                                      'question': '¿Garantiza la organización que se apliquen medidas de prevención de '
                                                  'fuga de datos (DLP) en sistemas, redes y puntos finales que '
                                                  'procesen información confidencial?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.12): '
                                                     'Assegurar que medidas de prevenção de vazamento de dados (DLP) '
                                                     'sejam aplicadas a sistemas, redes e outros dispositivos que '
                                                     'processem dados sensíveis.',
                                      'name': 'Prevenção de vazamento de dados (DLP)',
                                      'question': 'A organização garante que medidas de prevenção de vazamento de '
                                                  'dados (DLP) sejam aplicadas a sistemas, redes e outros dispositivos '
                                                  'que processem dados sensíveis?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Continuidade do Negócio',
                          'concepts': 'Recuperar',
                          'domains': 'Resiliência',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo, Corretivo'},
        'gcp_mapping': 'Cloud SQL Automated Backups & Cross-Region Snapshots',
        'how_to_check': '1. Inspecionar agendamento de backups automáticos de bancos de dados Cloud SQL, Spanner e '
                        'snapshots de Compute Engine.\n'
                        '2. Checar relatórios de testes periódicos de restauração de backup com validação de '
                        'integridade.',
        'how_to_maintain': '1. Configurar retenção de backup multirregional com proteção contra exclusão prematura.\n'
                           '2. Realizar simulação trimestral de restauração de banco de dados a partir do zero.',
        'id': 'A.8.13',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.13): Ensure that backup '
                                                     'copies of information, software, and system images are taken and '
                                                     'regularly tested in accordance with the agreed backup policy.',
                                      'name': 'Information backup',
                                      'question': 'Does the organization ensure that backup copies of information, '
                                                  'software, and system images are taken and regularly tested in '
                                                  'accordance with the agreed backup policy?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.13): Asegurar que '
                                                     'se realicen y prueben copias de respaldo de información, '
                                                     'software e imágenes de sistemas según la política de respaldo '
                                                     'acordada.',
                                      'name': 'Respaldo de información',
                                      'question': '¿Garantiza la organización que se realicen y prueben copias de '
                                                  'respaldo de información, software e imágenes de sistemas según la '
                                                  'política de respaldo acordada?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.13): '
                                                     'Assegurar que cópias de backup de informações, software e '
                                                     'imagens de sistemas sejam realizadas e testadas regularmente de '
                                                     'acordo com a política definida.',
                                      'name': 'Backup de informações',
                                      'question': 'A organização garante que cópias de backup de informações, software '
                                                  'e imagens de sistemas sejam realizadas e testadas regularmente de '
                                                  'acordo com a política definida?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Continuidade do Negócio',
                          'concepts': 'Proteger, Recuperar',
                          'domains': 'Resiliência',
                          'properties': 'Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Global External Application Load Balancer & Multi-Zone MIGs',
        'how_to_check': '1. Verificar topologia de implantação: confirmar cargas de trabalho configuradas em modo '
                        'multizona ou multirregião.\n'
                        '2. Validar redundância de balanceadores de carga Cloud Load Balancing com endereçamento '
                        'Anycast global.',
        'how_to_maintain': '1. Proibir instâncias de produção em zona única (Single Zone) sem réplica ativa.\n'
                           '2. Configurar pools de failover automático entre regiões distintas (`us-central1` e '
                           '`us-east4`).',
        'id': 'A.8.14',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.14): Ensure that '
                                                     'information processing facilities are implemented with '
                                                     'redundancy across multi-regions/zones to meet availability '
                                                     'requirements.',
                                      'name': 'Redundancy of information processing facilities',
                                      'question': 'Does the organization ensure that information processing facilities '
                                                  'are implemented with redundancy across multi-regions/zones to meet '
                                                  'availability requirements?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.14): Asegurar que '
                                                     'las instalaciones de procesamiento de información se implementen '
                                                     'con redundancia multizona para cumplir los requisitos de '
                                                     'disponibilidad.',
                                      'name': 'Redundancia de las instalaciones de procesamiento de información',
                                      'question': '¿Garantiza la organización que las instalaciones de procesamiento '
                                                  'de información se implementen con redundancia multizona para '
                                                  'cumplir los requisitos de disponibilidad?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.14): '
                                                     'Assegurar que instalações de processamento de informações sejam '
                                                     'implementadas com redundância suficiente para atender aos '
                                                     'requisitos de disponibilidade.',
                                      'name': 'Redundância das instalações de processamento da informação',
                                      'question': 'A organização garante que instalações de processamento de '
                                                  'informações sejam implementadas com redundância suficiente para '
                                                  'atender aos requisitos de disponibilidade?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Monitoramento de Segurança',
                          'concepts': 'Detectar',
                          'domains': 'Defesa',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Cloud Audit Logs & Centralized Log Bucket Lock',
        'how_to_check': '1. Inspecionar se 100% dos serviços possuem Cloud Audit Logs ativados para Admin Read, Data '
                        'Read e Data Write.\n'
                        '2. Validar exportação de logs para bucket centralizado com Bucket Lock (WORM).',
        'how_to_maintain': '1. Enforçar Organization Policy que impede desativação de Cloud Audit Logs no Google '
                           'Cloud.\n'
                           '2. Configurar alertas no Cloud Monitoring para exclusão de sinks ou modificação de filtros '
                           'de log.',
        'id': 'A.8.15',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.15): Ensure that audit '
                                                     'logs recording activities, exceptions, faults, and other '
                                                     'security events are generated, securely stored, protected from '
                                                     'tampering, and reviewed.',
                                      'name': 'Logging',
                                      'question': 'Does the organization ensure that audit logs recording activities, '
                                                  'exceptions, faults, and other security events are generated, '
                                                  'securely stored, protected from tampering, and reviewed?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.15): Asegurar que '
                                                     'se generen, almacenen de forma segura y revisen registros de '
                                                     'Cloud Audit Logs que documenten actividades, fallos y eventos de '
                                                     'seguridad.',
                                      'name': 'Registro de logs',
                                      'question': '¿Garantiza la organización que se generen, almacenen de forma '
                                                  'segura y revisen registros de Cloud Audit Logs que documenten actividades, '
                                                  'fallos y eventos de seguridad?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.15): '
                                                     'Assegurar que logs que registram atividades, exceções, falhas e '
                                                     'outros eventos relevantes sejam produzidos, armazenados, '
                                                     'protegidos e analisados regularmente.',
                                      'name': 'Registro de logs',
                                      'question': 'A organização garante que logs que registram atividades, exceções, '
                                                  'falhas e outros eventos relevantes sejam produzidos, armazenados, '
                                                  'protegidos e analisados regularmente?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Monitoramento de Segurança',
                          'concepts': 'Detectar',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Security Command Center Event Threat Detection & Chronicle SIEM',
        'how_to_check': '1. Checar integração do Google Security Operations (Chronicle SIEM) com telemetria do GCP.\n'
                        '2. Inspecionar regras ativas de detecção de anomalias de login, ataques de força bruta e '
                        'exfiltração de dados.',
        'how_to_maintain': '1. Monitorar métricas de anomalia de tráfego de rede via VPC Flow Logs.\n'
                           '2. Configurar equipe de SOC com alertas 24x7 integrados ao PagerDuty.',
        'id': 'A.8.16',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.16): Ensure that '
                                                     'networks, systems, and applications are continuously monitored '
                                                     'for anomalous behavior and potential information security '
                                                     'events.',
                                      'name': 'Monitoring activities',
                                      'question': 'Does the organization ensure that networks, systems, and '
                                                  'applications are continuously monitored for anomalous behavior and '
                                                  'potential information security events?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.16): Asegurar que '
                                                     'las redes, sistemas y aplicaciones sean monitoreados '
                                                     'continuamente en busca de comportamientos anómalos o incidentes.',
                                      'name': 'Actividades de monitoreo',
                                      'question': '¿Garantiza la organización que las redes, sistemas y aplicaciones '
                                                  'sean monitoreados continuamente en busca de comportamientos '
                                                  'anómalos o incidentes?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.16): '
                                                     'Assegurar que redes, sistemas e aplicações sejam monitorados '
                                                     'para identificar comportamentos anômalos e possíveis incidentes '
                                                     'de segurança.',
                                      'name': 'Atividades de monitoramento',
                                      'question': 'A organização garante que redes, sistemas e aplicações sejam '
                                                  'monitorados para identificar comportamentos anômalos e possíveis '
                                                  'incidentes de segurança?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Sistemas e Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Google TrueTime API & Network Time Protocol (NTP)',
        'how_to_check': '1. Validar que todas as instâncias Compute Engine e nós de contêiner sincronizam com o '
                        'servidor NTP oficial do Google (`metadata.google.internal` / `time.google.com`).\n'
                        '2. Checar consistência de timestamps nos Cloud Audit Logs.',
        'how_to_maintain': '1. Enforçar configuração de NTP padrão via agente do SO e imagens base aprovadas.\n'
                           '2. Rejeitar logs com deriva temporal superior a 1 segundo.',
        'id': 'A.8.17',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.17): Ensure that clocks '
                                                     'of all information processing systems within the organization '
                                                     'are synchronized with an approved, accurate time source (NTP).',
                                      'name': 'Clock synchronisation',
                                      'question': 'Does the organization ensure that clocks of all information '
                                                  'processing systems within the organization are synchronized with an '
                                                  'approved, accurate time source (NTP)?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.17): Asegurar que '
                                                     'los relojes de todos los sistemas de procesamiento estén '
                                                     'sincronizados con una fuente horaria confiable y precisa (NTP).',
                                      'name': 'Sincronización de relojes (NTP)',
                                      'question': '¿Garantiza la organización que los relojes de todos los sistemas de '
                                                  'procesamiento estén sincronizados con una fuente horaria confiable '
                                                  'y precisa (NTP)?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.17): '
                                                     'Assegurar que os relógios de todos os sistemas de processamento '
                                                     'de informações da organização estejam sincronizados com uma '
                                                     'fonte de tempo oficial e confiável.',
                                      'name': 'Sincronização de relógios (NTP)',
                                      'question': 'A organização garante que os relógios de todos os sistemas de '
                                                  'processamento de informações da organização estejam sincronizados '
                                                  'com uma fonte de tempo oficial e confiável?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Sistemas e Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Distroless Container Images & GKE Node Shielded VM',
        'how_to_check': '1. Inspecionar se o uso de utilitários como `gcloud`, `kubectl` e scripts de diagnóstico '
                        'administrativos exige elevação temporária auditada.\n'
                        '2. Checar desativação de ferramentas administrativas desnecessárias em contêineres de '
                        'produção.',
        'how_to_maintain': '1. Utilizar imagens de contêiner do tipo `Distroless` sem shell (`/bin/sh`) ou utilitários '
                           'administrativos.\n'
                           '2. Proibir acesso SSH direto a nós GKE em produção.',
        'id': 'A.8.18',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.18): Ensure that use of '
                                                     'utility programs capable of overriding system and application '
                                                     'security controls is strictly restricted and tightly controlled.',
                                      'name': 'Use of privileged utility programs',
                                      'question': 'Does the organization ensure that use of utility programs capable '
                                                  'of overriding system and application security controls is strictly '
                                                  'restricted and tightly controlled?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.18): Asegurar que '
                                                     'el uso de programas de utilidad capaces de anular los controles '
                                                     'de seguridad del sistema esté estrictamente restringido y '
                                                     'controlado.',
                                      'name': 'Uso de programas de utilidad privilegiados',
                                      'question': '¿Garantiza la organización que el uso de programas de utilidad '
                                                  'capaces de anular los controles de seguridad del sistema esté '
                                                  'estrictamente restringido y controlado?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.18): '
                                                     'Assegurar que o uso de programas utilitários capazes de sobrepor '
                                                     'ou anular controles de sistema e aplicação seja estritamente '
                                                     'restrito e controlado.',
                                      'name': 'Uso de programas utilitários privilegiados',
                                      'question': 'A organização garante que o uso de programas utilitários capazes de '
                                                  'sobrepor ou anular controles de sistema e aplicação seja '
                                                  'estritamente restrito e controlado?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Sistemas e Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'VM Manager OS Config & Immutable Golden Images',
        'how_to_check': '1. Inspecionar bloqueio de instalação de pacotes não autorizados em instâncias Compute Engine.\n'
                        '2. Validar uso de VM Manager (OS Config) para gerenciar inventário e conformidade de pacotes.',
        'how_to_maintain': '1. Bloquear repositórios de pacotes externos não homologados via firewall e Cloud NAT.\n'
                           '2. Automatizar instalação exclusiva de software através de imagens douradas (Golden '
                           'Images) imutáveis.',
        'id': 'A.8.19',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.19): Ensure that '
                                                     'procedures and technical controls are implemented to securely '
                                                     'govern and restrict software installation on operational '
                                                     'systems.',
                                      'name': 'Installation of software on operational systems',
                                      'question': 'Does the organization ensure that procedures and technical controls '
                                                  'are implemented to securely govern and restrict software '
                                                  'installation on operational systems?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.19): Asegurar que '
                                                     'se implementen procedimientos y controles para gestionar de '
                                                     'forma segura la instalación de software en sistemas operativos.',
                                      'name': 'Instalación de software en sistemas operativos',
                                      'question': '¿Garantiza la organización que se implementen procedimientos y '
                                                  'controles para gestionar de forma segura la instalación de software '
                                                  'en sistemas operativos?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.19): '
                                                     'Assegurar que procedimentos e medidas de controle sejam '
                                                     'implementados para gerenciar com segurança a instalação de '
                                                     'softwares em sistemas operacionais.',
                                      'name': 'Instalação de software em sistemas operacionais',
                                      'question': 'A organização garante que procedimentos e medidas de controle sejam '
                                                  'implementados para gerenciar com segurança a instalação de '
                                                  'softwares em sistemas operacionais?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger, Detectar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Cloud Armor, VPC Firewall Rules & Cloud IDS',
        'how_to_check': '1. Inspecionar regras de firewall VPC: validar proibição de regras com porta `0.0.0.0/0` '
                        'aberta para portas administrativas (SSH 22, RDP 3389).\n'
                        '2. Checar isolamento de redes com Private Google Access.',
        'how_to_maintain': '1. Ativar política de organização `constraints/compute.restrictFirewallPolicies`.\n'
                           '2. Inspecionar fluxo de pacotes com Cloud IDS (Intrusion Detection System) e Cloud Armor.',
        'id': 'A.8.20',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.20): Ensure that '
                                                     'networks and network devices are established, managed, and '
                                                     'controlled to protect information in systems, cloud '
                                                     'environments, and applications.',
                                      'name': 'Networks security',
                                      'question': 'Does the organization ensure that networks and network devices are '
                                                  'established, managed, and controlled to protect information in '
                                                  'systems, cloud environments, and applications?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.20): Asegurar que '
                                                     'las redes y dispositivos de red se configuren, gestionen y '
                                                     'controlen para proteger la información en tránsito y sistemas.',
                                      'name': 'Seguridad de redes',
                                      'question': '¿Garantiza la organización que las redes y dispositivos de red se '
                                                  'configuren, gestionen y controlen para proteger la información en '
                                                  'tránsito y sistemas?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.20): '
                                                     'Assegurar que redes corporativas e de nuvem e dispositivos de '
                                                     'rede sejam estabelecidos, gerenciados e controlados para '
                                                     'proteger as informações em trânsito.',
                                      'name': 'Segurança de redes',
                                      'question': 'A organização garante que redes corporativas e de nuvem e '
                                                  'dispositivos de rede sejam estabelecidos, gerenciados e controlados '
                                                  'para proteger as informações em trânsito?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud Interconnect & High-Availability Cloud VPN',
        'how_to_check': '1. Inspecionar contratos e configurações de conexões corporativas dedicadas (Cloud Interconnect / '
                        'Cloud VPN IPsec).\n'
                        '2. Validar criptografia de túneis VPN e autenticação mTLS em serviços expostos.',
        'how_to_maintain': '1. Enforçar criptografia AES-256 em todas as conexões VPN IPsec.\n'
                           '2. Monitorar SLAs e latência de serviços de rede corporativos.',
        'id': 'A.8.21',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.21): Ensure that '
                                                     'security mechanisms, service levels, and management requirements '
                                                     'of all network services are identified, agreed upon, and '
                                                     'implemented.',
                                      'name': 'Security of network services',
                                      'question': 'Does the organization ensure that security mechanisms, service '
                                                  'levels, and management requirements of all network services are '
                                                  'identified, agreed upon, and implemented?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.21): Asegurar que '
                                                     'los mecanismos de seguridad, niveles de servicio y requisitos de '
                                                     'gestión de todos los servicios de red se identifiquen e '
                                                     'implementen.',
                                      'name': 'Seguridad de los servicios de red',
                                      'question': '¿Garantiza la organización que los mecanismos de seguridad, niveles '
                                                  'de servicio y requisitos de gestión de todos los servicios de red '
                                                  'se identifiquen e implementen?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.21): '
                                                     'Assegurar que mecanismos de segurança, níveis de serviço e '
                                                     'requisitos de gestão de todos os serviços de rede sejam '
                                                     'identificados, acordados e implementados.',
                                      'name': 'Segurança de serviços de rede',
                                      'question': 'A organização garante que mecanismos de segurança, níveis de '
                                                  'serviço e requisitos de gestão de todos os serviços de rede sejam '
                                                  'identificados, acordados e implementados?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Shared VPC & Kubernetes NetworkPolicies',
        'how_to_check': '1. Inspecionar segmentação de redes VPC: confirmar segregação entre ambientes de '
                        'desenvolvimento, homologação e produção.\n'
                        '2. Checar uso de Shared VPC para controle centralizado de redes.',
        'how_to_maintain': '1. Isolar workloads em sub-redes distintas com controles rígidos de firewall e Service '
                           'Accounts específicas.\n'
                           '2. Implementar microsegmentação em clusters GKE utilizando NetworkPolicies de Kubernetes.',
        'id': 'A.8.22',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.22): Ensure that groups '
                                                     'of information services, users, and systems are logically '
                                                     'segregated in networks into distinct security perimeters.',
                                      'name': 'Segregation of networks',
                                      'question': 'Does the organization ensure that groups of information services, '
                                                  'users, and systems are logically segregated in networks into '
                                                  'distinct security perimeters?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.22): Asegurar que '
                                                     'los grupos de servicios de información, usuarios y sistemas se '
                                                     'segreguen en redes y perímetros lógicos independientes.',
                                      'name': 'Segregación de redes',
                                      'question': '¿Garantiza la organización que los grupos de servicios de '
                                                  'información, usuarios y sistemas se segreguen en redes y perímetros '
                                                  'lógicos independientes?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.22): '
                                                     'Assegurar que grupos de serviços de informação, usuários e '
                                                     'sistemas de informação sejam segregados em redes e perímetros '
                                                     'lógicos de segurança diferentes.',
                                      'name': 'Segregação de redes',
                                      'question': 'A organização garante que grupos de serviços de informação, '
                                                  'usuários e sistemas de informação sejam segregados em redes e '
                                                  'perímetros lógicos de segurança diferentes?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger',
                          'domains': 'Defesa',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud Secure Web Proxy & DNS Armor',
        'how_to_check': '1. Inspecionar regras de proxy seguro e Cloud Secure Web Proxy (SWP) controlando saída para a '
                        'internet.\n'
                        '2. Validar bloqueio de categorias de sites maliciosos e domínios não homologados.',
        'how_to_maintain': '1. Forçar tráfego de saída através do Cloud Secure Web Proxy com inspeção de certificados '
                           'TLS.\n'
                           '2. Bloquear downloads de binários executáveis de domínios sem reputação.',
        'id': 'A.8.23',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.23): Ensure that access '
                                                     'to external websites and untrusted web domains is managed and '
                                                     'filtered to reduce exposure to malicious content and web '
                                                     'attacks.',
                                      'name': 'Web filtering',
                                      'question': 'Does the organization ensure that access to external websites and '
                                                  'untrusted web domains is managed and filtered to reduce exposure to '
                                                  'malicious content and web attacks?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.23): Asegurar que '
                                                     'el acceso a sitios web externos se gestione y filtre para '
                                                     'reducir la exposición a contenidos maliciosos y ataques web.',
                                      'name': 'Filtrado web',
                                      'question': '¿Garantiza la organización que el acceso a sitios web externos se '
                                                  'gestione y filtre para reducir la exposición a contenidos '
                                                  'maliciosos y ataques web?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.23): '
                                                     'Assegurar que o acesso a sites e domínios externos seja '
                                                     'gerenciado e filtrado para reduzir a exposição a conteúdos '
                                                     'maliciosos e ataques cibernéticos.',
                                      'name': 'Filtragem web',
                                      'question': 'A organização garante que o acesso a sites e domínios externos seja '
                                                  'gerenciado e filtrado para reduzir a exposição a conteúdos '
                                                  'maliciosos e ataques cibernéticos?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Criptografia',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud KMS HSM & Customer-Managed Encryption Keys (CMEK)',
        'how_to_check': '1. Inspecionar chaves Cloud KMS: validar uso de chaves gerenciadas pelo cliente (CMEK) com '
                        'proteção HSM (Hardware Security Module).\n'
                        '2. Checar período de rotação automática de chaves (<= 90 dias).',
        'how_to_maintain': '1. Enforçar política de organização `constraints/gcp.restrictCmekCryptoKeyProjects`.\n'
                           '2. Proibir uso de algoritmos criptográficos depreciados (ex: SHA-1, 3DES).',
        'id': 'A.8.24',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.24): Ensure that rules '
                                                     'for the effective use of cryptography in transit and at rest, '
                                                     'including cryptographic key management (KMS/HSM), are defined '
                                                     'and enforced.',
                                      'name': 'Use of cryptography',
                                      'question': 'Does the organization ensure that rules for the effective use of '
                                                  'cryptography in transit and at rest, including cryptographic key '
                                                  'management (KMS/HSM), are defined and enforced?',
                                      'recommended_evidence': '• Cloud KMS cryptographic key inventory (`gcloud kms '
                                                              'keys list --keyring=...`).\n'
                                                              '• Proof of automated key rotation enabled (period <= 90 '
                                                              'days).\n'
                                                              '• CMEK (Customer-Managed Encryption Keys) configured '
                                                              'across Cloud Storage buckets and BigQuery datasets.\n'
                                                              '• TLS 1.3 cipher suite enforcement on Google Cloud '
                                                              'HTTPS Load Balancers.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.24): Asegurar que '
                                                     'se apliquen normas para el uso eficaz de la criptografía en '
                                                     'reposo y en tránsito, incluida la gestión de claves '
                                                     'criptográficas (KMS).',
                                      'name': 'Uso de criptografía',
                                      'question': '¿Garantiza la organización que se apliquen normas para el uso '
                                                  'eficaz de la criptografía en reposo y en tránsito, incluida la '
                                                  'gestión de claves criptográficas (KMS)?',
                                      'recommended_evidence': '• Inventario de claves criptográficas en Cloud KMS '
                                                              '(`gcloud kms keys list --keyring=...`).\n'
                                                              '• Constancia de rotación automática de claves '
                                                              'habilitada (período <= 90 días).\n'
                                                              '• Configuración de CMEK en depósitos de Cloud Storage y '
                                                              'conjuntos de datos BigQuery.\n'
                                                              '• Políticas de cifrado TLS 1.3 activas en los '
                                                              'balanceadores de carga HTTPS de Google Cloud.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.24): '
                                                     'Assegurar que regras para o uso efetivo de criptografia em '
                                                     'repouso e em trânsito, incluindo gestão segura de chaves '
                                                     'criptográficas (KMS), sejam aplicadas.',
                                      'name': 'Uso de criptografia',
                                      'question': 'A organização garante que regras para o uso efetivo de criptografia '
                                                  'em repouso e em trânsito, incluindo gestão segura de chaves '
                                                  'criptográficas (KMS), sejam aplicadas?',
                                      'recommended_evidence': '• Inventário de chaves criptográficas no Cloud KMS '
                                                              '(`gcloud kms keys list --keyring=...`).\n'
                                                              '• Comprovação de rotação automática de chaves ativada '
                                                              '(período <= 90 dias).\n'
                                                              '• Configuração de CMEK (Customer-Managed Encryption '
                                                              'Keys) nos buckets de Cloud Storage e tabelas do '
                                                              'BigQuery.\n'
                                                              '• Políticas de TLS 1.3 enforce nos Google Cloud HTTPS '
                                                              'Load Balancers.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud Build Secure CI/CD Pipeline & SAST/DAST Gates',
        'how_to_check': '1. Inspecionar pipeline de CI/CD: checar presença de etapas de SAST, DAST, SCA e verificação de '
                        'segredos (Secret Scanning).\n'
                        '2. Inspecionar política de DevSecOps aprovada.',
        'how_to_maintain': '1. Integrar verificações de segurança obrigatórias no Cloud Build / GitHub Actions.\n'
                           '2. Bloquear merges de código que apresentem vulnerabilidades de severidade alta.',
        'id': 'A.8.25',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.25): Ensure that rules '
                                                     'for secure software and systems engineering are established and '
                                                     'applied throughout the full development lifecycle (DevSecOps).',
                                      'name': 'Secure development life cycle',
                                      'question': 'Does the organization ensure that rules for secure software and '
                                                  'systems engineering are established and applied throughout the full '
                                                  'development lifecycle (DevSecOps)?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.25): Asegurar que '
                                                     'se establezcan y apliquen reglas de desarrollo seguro de '
                                                     'software en todo el ciclo de vida de desarrollo (DevSecOps).',
                                      'name': 'Ciclo de vida de desarrollo seguro (SDLC)',
                                      'question': '¿Garantiza la organización que se establezcan y apliquen reglas de '
                                                  'desarrollo seguro de software en todo el ciclo de vida de '
                                                  'desarrollo (DevSecOps)?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.25): '
                                                     'Assegurar que regras para o desenvolvimento seguro de software e '
                                                     'sistemas sejam estabelecidas e aplicadas em todo o ciclo de vida '
                                                     '(DevSecOps).',
                                      'name': 'Ciclo de vida de desenvolvimento seguro (SDLC)',
                                      'question': 'A organização garante que regras para o desenvolvimento seguro de '
                                                  'software e sistemas sejam estabelecidas e aplicadas em todo o ciclo '
                                                  'de vida (DevSecOps)?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Identificar',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'OWASP Application Security Baseline & Architecture Review',
        'how_to_check': '1. Inspecionar especificações funcionais e de arquitetura de software: validar presença de '
                        'requisitos de autenticação, autorização e trilhas de rastreabilidade.\n'
                        '2. Checar conformidade com OWASP Top 10.',
        'how_to_maintain': '1. Realizar modelagem formal de ameaças (Threat Modeling) na fase de concepção de novos '
                           'sistemas.\n'
                           '2. Homologar requisitos de segurança com a equipe de cibersegurança antes do início do '
                           'desenvolvimento.',
        'id': 'A.8.26',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.26): Ensure that '
                                                     'information security requirements are identified, specified, and '
                                                     'approved when developing or acquiring new applications.',
                                      'name': 'Application security requirements',
                                      'question': 'Does the organization ensure that information security requirements '
                                                  'are identified, specified, and approved when developing or '
                                                  'acquiring new applications?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.26): Asegurar que '
                                                     'los requisitos de seguridad de la información se identifiquen, '
                                                     'especifiquen y aprueben al desarrollar o adquirir aplicaciones.',
                                      'name': 'Requisitos de seguridad de aplicaciones',
                                      'question': '¿Garantiza la organización que los requisitos de seguridad de la '
                                                  'información se identifiquen, especifiquen y aprueben al desarrollar '
                                                  'o adquirir aplicaciones?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.26): '
                                                     'Assegurar que requisitos de segurança da informação sejam '
                                                     'identificados, especificados e aprovados ao desenvolver ou '
                                                     'adquirir novas aplicações.',
                                      'name': 'Requisitos de segurança de aplicações',
                                      'question': 'A organização garante que requisitos de segurança da informação '
                                                  'sejam identificados, especificados e aprovados ao desenvolver ou '
                                                  'adquirir novas aplicações?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Sistemas e Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Google Cloud Architecture Framework (Security Pillar) & Zero Trust',
        'how_to_check': '1. Inspecionar projetos GCP contra princípios de arquitetura segura: Menor Privilégio, Defesa em '
                        'Profundidade e Falha Segura (Fail-Safe).\n'
                        '2. Validar arquitetura Zero Trust implementada.',
        'how_to_maintain': '1. Adotar os princípios do Google Cloud Architecture Framework (Security pillar).\n'
                           '2. Conduzir revisão técnica de arquitetura semestral para todos os sistemas críticos.',
        'id': 'A.8.27',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.27): Ensure that '
                                                     'principles for engineering secure systems are established, '
                                                     'documented, maintained, and applied to all information system '
                                                     'architectures.',
                                      'name': 'Secure system architecture and engineering principles',
                                      'question': 'Does the organization ensure that principles for engineering secure '
                                                  'systems are established, documented, maintained, and applied to all '
                                                  'information system architectures?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.27): Asegurar que '
                                                     'se establezcan, documenten y apliquen principios de arquitectura '
                                                     'e ingeniería de sistemas seguros en todas las implementaciones.',
                                      'name': 'Arquitectura y principios de ingeniería de sistemas seguros',
                                      'question': '¿Garantiza la organización que se establezcan, documenten y '
                                                  'apliquen principios de arquitectura e ingeniería de sistemas '
                                                  'seguros en todas las implementaciones?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.27): '
                                                     'Assegurar que princípios para a engenharia de sistemas seguros '
                                                     'sejam estabelecidos, documentados, mantidos e aplicados a '
                                                     'qualquer sistema implementado.',
                                      'name': 'Arquitetura de sistemas seguros e princípios de engenharia',
                                      'question': 'A organização garante que princípios para a engenharia de sistemas '
                                                  'seguros sejam estabelecidos, documentados, mantidos e aplicados a '
                                                  'qualquer sistema implementado?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Static Code Analysis (SAST) & Pre-Commit Security Linters',
        'how_to_check': '1. Inspecionar regras de validação estática de código (SAST) em busca de injeções SQL, XSS e '
                        'manipulação inadequada de memória.\n'
                        '2. Validar uso de bibliotecas homologadas e sanitização rigorosa de entradas de usuário.',
        'how_to_maintain': '1. Enforçar linters de segurança e verificadores automáticos de código em pré-commit '
                           'hooks.\n'
                           '2. Conduzir revisões de código focadas em segurança por pares para 100% dos pull requests.',
        'id': 'A.8.28',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'NON_COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.28): Ensure that secure '
                                                     'coding principles and static analysis (SAST) are applied to '
                                                     'software development to prevent common coding vulnerabilities.',
                                      'name': 'Secure coding',
                                      'question': 'Does the organization ensure that secure coding principles and '
                                                  'static analysis (SAST) are applied to software development to '
                                                  'prevent common coding vulnerabilities?',
                                      'recommended_evidence': '• Secure Coding Guidelines aligned with OWASP Top 10 '
                                                              'and CWE/SANS standards.\n'
                                                              '• CI/CD automated pipeline (Cloud Build / GitHub '
                                                              'Actions) integrating SAST and container vulnerability '
                                                              'scans.\n'
                                                              '• Branch protection rules enforcing mandatory '
                                                              '2-reviewer peer code reviews before merging to main.\n'
                                                              '• Software Bill of Materials (SBOM) and dependency '
                                                              'vulnerability scan reports.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.28): Asegurar que '
                                                     'se apliquen principios de codificación segura (SAST/OWASP) al '
                                                     'desarrollo de software para evitar vulnerabilidades de código.',
                                      'name': 'Codificación segura',
                                      'question': '¿Garantiza la organización que se apliquen principios de '
                                                  'codificación segura (SAST/OWASP) al desarrollo de software para '
                                                  'evitar vulnerabilidades de código?',
                                      'recommended_evidence': '• Guía de Codificación Segura alineada con estándares '
                                                              'OWASP Top 10 y CWE/SANS.\n'
                                                              '• Canal de CI/CD automatizado con escáneres SAST y '
                                                              'análisis de vulnerabilidades en contenedores.\n'
                                                              '• Reglas de protección de ramas que exigen revisión '
                                                              'obligatoria de código por pares antes del despliegue.\n'
                                                              '• Informes de análisis de dependencias (SBOM) y '
                                                              'remediación de vulnerabilidades críticas.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.28): '
                                                     'Assegurar que princípios de codificação segura sejam aplicados '
                                                     'ao desenvolvimento de software para prevenir vulnerabilidades de '
                                                     'código (OWASP Top 10).',
                                      'name': 'Codificação segura',
                                      'question': 'A organização garante que princípios de codificação segura sejam '
                                                  'aplicados ao desenvolvimento de software para prevenir '
                                                  'vulnerabilidades de código (OWASP Top 10)?',
                                      'recommended_evidence': '• Guia de Boas Práticas de Codificação Segura (alinhado '
                                                              'a OWASP Top 10 e CWE/SANS).\n'
                                                              '• Pipeline de CI/CD (Cloud Build / GitHub Actions) com '
                                                              'verificação automatizada de SAST (SonarQube/Trivy).\n'
                                                              '• Configuração de Branch Protection exigindo aprovação '
                                                              'obrigatória de 2 revisores (Code Owners).\n'
                                                              '• Registros de varredura de dependências e bloqueio de '
                                                              'vulnerabilidades críticas.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Detectar',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Automated DAST in Staging & Acceptance Criteria Validation',
        'how_to_check': '1. Inspecionar relatórios de testes de aceitação de segurança e testes de intrusão '
                        'automatizados executados nos ambientes de homologação.\n'
                        '2. Validar evidências de testes de estresse e resiliência.',
        'how_to_maintain': '1. Automatizar testes dinâmicos de segurança (DAST) em pipelines de homologação antes de '
                           'cada release.\n'
                           '2. Exigir aprovação formal de segurança no termo de homologação do sistema.',
        'id': 'A.8.29',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.29): Ensure that '
                                                     'security testing processes (DAST, SAST, vulnerability scans, '
                                                     'penetration tests) are conducted during development and '
                                                     'acceptance.',
                                      'name': 'Security testing in development and acceptance',
                                      'question': 'Does the organization ensure that security testing processes (DAST, '
                                                  'SAST, vulnerability scans, penetration tests) are conducted during '
                                                  'development and acceptance?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.29): Asegurar que '
                                                     'se realicen pruebas de seguridad (DAST, SAST, pentesting) '
                                                     'durante el desarrollo y los procesos de aceptación.',
                                      'name': 'Pruebas de seguridad en desarrollo y aceptación',
                                      'question': '¿Garantiza la organización que se realicen pruebas de seguridad '
                                                  '(DAST, SAST, pentesting) durante el desarrollo y los procesos de '
                                                  'aceptación?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.29): '
                                                     'Assegurar que processos de teste de segurança (DAST, SAST, '
                                                     'testes de invasão) sejam definidos e executados durante o '
                                                     'desenvolvimento e processo de homologação.',
                                      'name': 'Testes de segurança em desenvolvimento e aceite',
                                      'question': 'A organização garante que processos de teste de segurança (DAST, '
                                                  'SAST, testes de invasão) sejam definidos e executados durante o '
                                                  'desenvolvimento e processo de homologação?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Aplicações',
                          'concepts': 'Identificar, Proteger',
                          'domains': 'Governança e Ecossistema',
                          'properties': 'Integridade',
                          'type': 'Preventivo, Detectivo'},
        'gcp_mapping': 'Third-Party Code Quality Gate & SLA Enforcement',
        'how_to_check': '1. Inspecionar conformidade de código produzido por empresas terceirizadas e consultorias de '
                        'desenvolvimento.\n'
                        '2. Checar testes de segurança e validação de dependências antes da integração nos '
                        'repositórios internos.',
        'how_to_maintain': '1. Exigir assinatura de SLA de correção de vulnerabilidades em contratos de '
                           'desenvolvimento terceirizado.\n'
                           '2. Submeter todo código entregue por terceiros aos mesmos pipelines rigorosos de SAST e '
                           'aprovação interna.',
        'id': 'A.8.30',
        'severity': 'MEDIUM',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.30): Ensure that the '
                                                     'organization directs, monitors, and reviews activities related '
                                                     'to outsourced software development to ensure security standards.',
                                      'name': 'Outsourced development',
                                      'question': 'Does the organization ensure that the organization directs, '
                                                  'monitors, and reviews activities related to outsourced software '
                                                  'development to ensure security standards?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.30): Asegurar que '
                                                     'la organización dirija, supervise y revise las actividades '
                                                     'externalizadas de desarrollo de software para garantizar los '
                                                     'estándares.',
                                      'name': 'Desarrollo externalizado',
                                      'question': '¿Garantiza la organización que la organización dirija, supervise y '
                                                  'revise las actividades externalizadas de desarrollo de software '
                                                  'para garantizar los estándares?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.30): '
                                                     'Assegurar que a organização direcione, monitore e analise a '
                                                     'segurança das atividades terceirizadas de desenvolvimento de '
                                                     'software.',
                                      'name': 'Desenvolvimento terceirizado',
                                      'question': 'A organização garante que a organização direcione, monitore e '
                                                  'analise a segurança das atividades terceirizadas de desenvolvimento '
                                                  'de software?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Segurança de Sistemas e Redes',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'GCP Multi-Project Isolation & Resource Manager Hierarchy',
        'how_to_check': '1. Inspecionar segregação estrita de projetos GCP: projetos distintos na hierarquia do Cloud '
                        'Resource Manager para `dev`, `staging` e `prod`.\n'
                        '2. Validar que dados reais de clientes de produção não estão presentes em ambientes de '
                        'desenvolvimento.',
        'how_to_maintain': '1. Aplicar Organization Policies com isolamento de credenciais e permissões entre '
                           'projetos.\n'
                           '2. Bloquear comunicação de rede direta entre ambientes de desenvolvimento e produção.',
        'id': 'A.8.31',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.31): Ensure that '
                                                     'development, testing, and production environments are strictly '
                                                     'separated and secured in isolated cloud projects and perimeters.',
                                      'name': 'Separation of development, test and production environments',
                                      'question': 'Does the organization ensure that development, testing, and '
                                                  'production environments are strictly separated and secured in '
                                                  'isolated cloud projects and perimeters?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.31): Asegurar que '
                                                     'los entornos de desarrollo, pruebas y producción estén '
                                                     'estrictamente separados y asegurados en proyectos y redes '
                                                     'aisladas.',
                                      'name': 'Separación de entornos de desarrollo, pruebas y producción',
                                      'question': '¿Garantiza la organización que los entornos de desarrollo, pruebas '
                                                  'y producción estén estrictamente separados y asegurados en '
                                                  'proyectos y redes aisladas?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.31): '
                                                     'Assegurar que ambientes de desenvolvimento, teste e produção '
                                                     'sejam separados e protegidos em projetos e contas de nuvem '
                                                     'isoladas.',
                                      'name': 'Separação de ambientes de desenvolvimento, teste e produção',
                                      'question': 'A organização garante que ambientes de desenvolvimento, teste e '
                                                  'produção sejam separados e protegidos em projetos e contas de nuvem '
                                                  'isoladas?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'GitOps Change Management & Automated Rollback',
        'how_to_check': '1. Inspecionar trilha de rastreabilidade de mudanças: verificar aprovações em PRs de Terraform e '
                        'tíquetes de mudança (Change Requests) aprovados pelo CAB.\n'
                        '2. Checar logs de alterações na infraestrutura via Cloud Audit Logs.',
        'how_to_maintain': '1. Enforçar infraestrutura imutável e proibição de alterações manuais não rastreadas.\n'
                           '2. Implementar rollback automatizado em caso de falha nos testes de integridade '
                           'pós-deploy.',
        'id': 'A.8.32',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.32): Ensure that changes '
                                                     'to information processing facilities and information systems are '
                                                     'subject to formal change management and peer review procedures.',
                                      'name': 'Change management',
                                      'question': 'Does the organization ensure that changes to information processing '
                                                  'facilities and information systems are subject to formal change '
                                                  'management and peer review procedures?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.32): Asegurar que '
                                                     'los cambios en instalaciones y sistemas de información estén '
                                                     'sujetos a procedimientos formales de gestión de cambios.',
                                      'name': 'Gestión de cambios',
                                      'question': '¿Garantiza la organización que los cambios en instalaciones y '
                                                  'sistemas de información estén sujetos a procedimientos formales de '
                                                  'gestión de cambios?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.32): '
                                                     'Assegurar que mudanças em instalações de processamento de '
                                                     'informações e sistemas de informação estejam sujeitas a '
                                                     'procedimentos formais de gestão de mudanças.',
                                      'name': 'Gestão de mudanças',
                                      'question': 'A organização garante que mudanças em instalações de processamento '
                                                  'de informações e sistemas de informação estejam sujeitas a '
                                                  'procedimentos formais de gestão de mudanças?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Proteção da Informação',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Confidencialidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Synthetic Data Generators & Irreversible DLP Anonymization',
        'how_to_check': '1. Validar que dados de teste são gerados sinteticamente ou anonimizados/mascarados antes de '
                        'serem carregados em ambientes de teste.\n'
                        '2. Inspecionar bancos de teste com Sensitive Data Protection (Cloud DLP).',
        'how_to_maintain': '1. Proibir cópia de bases de dados de produção para homologação sem processo prévio de '
                           'mascaramento irreversível.\n'
                           '2. Utilizar ferramentas de geração de dados sintéticos para testes de carga e QA.',
        'id': 'A.8.33',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.33): Ensure that test '
                                                     'information is suitably selected, protected, and controlled, '
                                                     'prohibiting real production personal data in staging/test '
                                                     'environments.',
                                      'name': 'Test information',
                                      'question': 'Does the organization ensure that test information is suitably '
                                                  'selected, protected, and controlled, prohibiting real production '
                                                  'personal data in staging/test environments?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.33): Asegurar que '
                                                     'la información de prueba sea seleccionada y protegida, '
                                                     'prohibiendo datos personales reales de producción en entornos de '
                                                     'prueba.',
                                      'name': 'Información de prueba',
                                      'question': '¿Garantiza la organización que la información de prueba sea '
                                                  'seleccionada y protegida, prohibiendo datos personales reales de '
                                                  'producción en entornos de prueba?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.33): '
                                                     'Assegurar que informações de teste sejam selecionadas, '
                                                     'protegidas e controladas adequadamente, proibindo dados pessoais '
                                                     'reais de produção em ambientes de teste.',
                                      'name': 'Informações de teste',
                                      'question': 'A organização garante que informações de teste sejam selecionadas, '
                                                  'protegidas e controladas adequadamente, proibindo dados pessoais '
                                                  'reais de produção em ambientes de teste?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}},
    {   'attributes': {   'capabilities': 'Governança',
                          'concepts': 'Proteger',
                          'domains': 'Proteção',
                          'properties': 'Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Controlled Audit Windows & Test Isolation Protocols',
        'how_to_check': '1. Inspecionar procedimentos de avaliação técnica e testes de estresse: validar agendamento '
                        'prévio fora de horário de pico e janelas controladas.\n'
                        '2. Checar monitoramento em tempo real durante execuções de pentest para evitar '
                        'indisponibilidade.',
        'how_to_maintain': '1. Isolar testes intrusivos em réplicas de homologação idênticas a produção.\n'
                           '2. Definir protocolo de interrupção imediata (Kill Switch) para qualquer teste que ameace '
                           'a estabilidade do negócio.',
        'id': 'A.8.34',
        'severity': 'LOW',
        'soa_status': 'APLICÁVEL (INCLUÍDO NO SGSI)',
        'status': 'COMPLIANT',
        'theme_key': 'A.8',
        'translations': {   'en': {   'description': 'ISO/IEC 27001:2022 Annex A Control (A.8.34): Ensure that audit '
                                                     'tests and other assurance activities involving assessment of '
                                                     'operational systems are planned and agreed to minimize '
                                                     'disruption.',
                                      'name': 'Protection of information systems during audit testing',
                                      'question': 'Does the organization ensure that audit tests and other assurance '
                                                  'activities involving assessment of operational systems are planned '
                                                  'and agreed to minimize disruption?',
                                      'recommended_evidence': '1. IAM policy and role assignment exports (`gcloud '
                                                              'projects get-iam-policy`) with enforced multi-factor '
                                                              'authentication (MFA).\n'
                                                              '2. Encryption at rest and in transit configuration '
                                                              'using Cloud KMS managed keys (`gcloud kms keys list`).\n'
                                                              '3. VPC firewall rules, Cloud Armor policies, and '
                                                              'private network topologies with restricted public '
                                                              'endpoints.\n'
                                                              '4. Recent vulnerability scan reports (SAST/DAST, '
                                                              'Container Analysis) and third-party penetration test '
                                                              'reports.\n'
                                                              '5. Centralized Cloud Audit Logs and Security Command '
                                                              'Center event logs with at least 365-day retention.',
                                      'theme': 'A.8 Technological',
                                      'theme_title': 'A.8 — Technological Controls'},
                            'es': {   'description': 'Requisito del control ISO/IEC 27001:2022 (A.8.34): Asegurar que '
                                                     'las pruebas de auditoría en sistemas operativos se planifiquen y '
                                                     'acuerden para minimizar el impacto en las operaciones de '
                                                     'negocio.',
                                      'name': 'Protección de los sistemas de información durante las pruebas de '
                                              'auditoría',
                                      'question': '¿Garantiza la organización que las pruebas de auditoría en sistemas '
                                                  'operativos se planifiquen y acuerden para minimizar el impacto en '
                                                  'las operaciones de negocio?',
                                      'recommended_evidence': '1. Exportación de políticas IAM (`gcloud projects '
                                                              'get-iam-policy`) con autenticación multifactor (MFA) '
                                                              'obligatoria.\n'
                                                              '2. Configuración de cifrado en reposo y en tránsito con '
                                                              'gestión de claves Cloud KMS (`gcloud kms keys list`).\n'
                                                              '3. Reglas de cortafuegos VPC, políticas Cloud Armor y '
                                                              'topología de red privada sin IPs públicas '
                                                              'innecesarias.\n'
                                                              '4. Informes recientes de escaneo de vulnerabilidades '
                                                              '(SAST/DAST) y pruebas de penetración (pentest).\n'
                                                              '5. Registros de Cloud Audit Logs centralizados en Cloud '
                                                              'Logging / SIEM con política de retención de al menos '
                                                              '365 días.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'},
                            'pt': {   'description': 'Requisito normativo do controle ISO/IEC 27001:2022 (A.8.34): '
                                                     'Assegurar que testes de auditoria e outras atividades de '
                                                     'garantia que envolvam a avaliação de sistemas operacionais sejam '
                                                     'planejados para minimizar impactos.',
                                      'name': 'Proteção de sistemas de informação durante testes de auditoria',
                                      'question': 'A organização garante que testes de auditoria e outras atividades '
                                                  'de garantia que envolvam a avaliação de sistemas operacionais sejam '
                                                  'planejados para minimizar impactos?',
                                      'recommended_evidence': '1. Exportação de inventário e políticas de controle de '
                                                              'acesso IAM (`gcloud projects get-iam-policy`) com MFA '
                                                              'obrigatório.\n'
                                                              '2. Configuração de criptografia em repouso e em '
                                                              'trânsito com gerenciamento de chaves Cloud KMS (`gcloud '
                                                              'kms keys list`).\n'
                                                              '3. Regras de firewall VPC, Cloud Armor e topologia de '
                                                              'isolamento de rede sem IP público desnecessário.\n'
                                                              '4. Relatórios de varredura de vulnerabilidades '
                                                              '(SAST/DAST) e testes de intrusão (pentest) recentes.\n'
                                                              '5. Registros de Cloud Audit Logs centralizados no '
                                                              'Cloud Logging / Cloud Monitoring com retenção mínima de '
                                                              '365 dias.',
                                      'theme': 'A.8 Tecnológico',
                                      'theme_title': 'A.8 — Controles Tecnológicos'}}}]

# SOC 2 Criteria with Full Multilingual Specifications
SOC2_QUESTIONNAIRE_CATALOG = [   {   'attributes': {   'capabilities': 'Controle de Acesso',
                          'concepts': 'Proteger',
                          'domains': 'Segurança Lógica',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud IAM, Cloud Identity, Context-Aware Access',
        'how_to_check': '1. Inspecionar políticas IAM e RBAC no GCP e Google Workspace.\n'
                        '2. Verificar restrições de acesso por IP e Context-Aware Access.\n'
                        '3. Checar logs de autenticação no Cloud Identity.',
        'how_to_maintain': '1. Revisão trimestral de acessos com IAM Recommender.\n'
                           '2. Revogação automatizada de credenciais inativas > 90 dias.',
        'id': 'CC6.1',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (SOC 2 CRITERIA)',
        'status': 'COMPLIANT',
        'theme_key': 'SOC2_CC',
        'translations': {   'en': {   'description': 'SOC 2 CC6.1 Requirement: The entity implements logical access '
                                                     'security software, infrastructure, and architectures over '
                                                     'protected information assets.',
                                      'name': 'Logical Access Controls and Infrastructure Security',
                                      'question': 'Does the organization implement logical access software, network '
                                                  'infrastructure, and authentication controls to prevent unauthorized '
                                                  'access?',
                                      'recommended_evidence': '• Formal Logical Access Control Policy.\n'
                                                              '• GCP IAM policy exports and mandatory MFA '
                                                              'configuration logs.\n'
                                                              '• Quarterly privileged access review reports.',
                                      'theme': 'SOC 2 Security',
                                      'theme_title': 'SOC 2 — Trust Services Security Criteria'},
                            'es': {   'description': 'Requisito SOC 2 CC6.1: La entidad implementa controles de acceso '
                                                     'lógico sobre activos de información y componentes de '
                                                     'infraestructura.',
                                      'name': 'Controles de Acceso Lógico y Seguridad de Infraestructura',
                                      'question': '¿Implementa la organización controles de seguridad lógica, '
                                                  'arquitectura de red y autenticación para evitar el acceso no '
                                                  'autorizado?',
                                      'recommended_evidence': '• Política de Control de Acceso Lógico formalizada.\n'
                                                              '• Exportación de políticas IAM y registro de MFA '
                                                              'obligatorio en GCP.\n'
                                                              '• Informes de revisión periódica de accesos.',
                                      'theme': 'SOC 2 Seguridad',
                                      'theme_title': 'SOC 2 — Criterios de Seguridad (Common Criteria)'},
                            'pt': {   'description': 'Requisito SOC 2 CC6.1: A entidade implementa controles de acesso '
                                                     'lógico sobre dados protegidos e componentes de sistema.',
                                      'name': 'Controles de Acesso Lógico e Segurança de Infraestrutura',
                                      'question': 'A organização implementa controles de segurança lógica, arquitetura '
                                                  'de rede e autenticação para proteger ativos contra acessos não '
                                                  'autorizados?',
                                      'recommended_evidence': '• Política de Controle de Acesso Lógico formalizada.\n'
                                                              '• Exportação de configurações IAM e MFA obrigatório no '
                                                              'Google Workspace e GCP.\n'
                                                              '• Relatórios de revisão de acessos trimestrais.',
                                      'theme': 'SOC 2 Segurança',
                                      'theme_title': 'SOC 2 — Critérios de Segurança (Common Criteria)'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade',
                          'concepts': 'Identificar',
                          'domains': 'Segurança Lógica',
                          'properties': 'Integridade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'Cloud Identity, Google Workspace Admin Directory, Cloud Audit Logs',
        'how_to_check': '1. Verificar procedimento formal de aprovação de novos usuários via tickets de ITSM.\n'
                        '2. Checar provisionamento automático via Cloud Identity/SCIM.\n'
                        '3. Validar aplicação de MFA no primeiro acesso.',
        'how_to_maintain': '1. Integração HRIS com Cloud Identity para provisionamento automático.\n'
                           '2. Alertas imediatos de novas contas criadas fora do processo padrão.',
        'id': 'CC6.2',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (SOC 2 CRITERIA)',
        'status': 'COMPLIANT',
        'theme_key': 'SOC2_CC',
        'translations': {   'en': {   'description': 'SOC 2 CC6.2 Requirement: Prior to issuing system credentials, '
                                                     'the entity registers and authorizes new internal and external '
                                                     'users.',
                                      'name': 'User Registration and Access Management',
                                      'question': 'Does the organization register and formally authorize new internal '
                                                  'and external users prior to issuing credentials and granting '
                                                  'access?',
                                      'recommended_evidence': '• Documented user onboarding and access request tickets '
                                                              'with management sign-off.\n'
                                                              '• Directory provisioning logs from HRIS to Google '
                                                              'Workspace.\n'
                                                              '• User credential issuance audit trails.',
                                      'theme': 'SOC 2 Security',
                                      'theme_title': 'SOC 2 — Trust Services Security Criteria'},
                            'es': {   'description': 'Requisito SOC 2 CC6.2: Antes de emitir credenciales, la entidad '
                                                     'registra y autoriza a nuevos usuarios internos y externos.',
                                      'name': 'Registro de Usuarios y Gestión de Acceso',
                                      'question': '¿La organización registra y autoriza formalmente a los nuevos '
                                                  'usuarios antes de otorgar credenciales y accesos a los sistemas?',
                                      'recommended_evidence': '• Tickets documentados de solicitud y aprobación de '
                                                              'acceso de usuarios.\n'
                                                              '• Registros de aprovisionamiento de cuentas vinculados '
                                                              'a RRHH.\n'
                                                              '• Evidencias de asignación de privilegios según el rol.',
                                      'theme': 'SOC 2 Seguridad',
                                      'theme_title': 'SOC 2 — Criterios de Seguridad (Common Criteria)'},
                            'pt': {   'description': 'Requisito SOC 2 CC6.2: A entidade registra e autoriza novos '
                                                     'usuários antes de emitir credenciais de acesso ao sistema.',
                                      'name': 'Registro de Usuários e Gestão de Credenciais',
                                      'question': 'A organização autoriza e registra formalmente novos usuários '
                                                  'internos e externos antes de conceder credenciais e acessos aos '
                                                  'sistemas?',
                                      'recommended_evidence': '• Fluxo documentado de solicitação e aprovação de '
                                                              'credenciais via chamados (Jira/ServiceNow).\n'
                                                              '• Relatório de provisionamento de novos colaboradores e '
                                                              'contratados.\n'
                                                              '• Registros de concessão de acessos alinhados à função '
                                                              'do colaborador.',
                                      'theme': 'SOC 2 Segurança',
                                      'theme_title': 'SOC 2 — Critérios de Segurança (Common Criteria)'}}},
    {   'attributes': {   'capabilities': 'Gestão de Identidade',
                          'concepts': 'Responder',
                          'domains': 'Segurança Lógica',
                          'properties': 'Confidencialidade, Integridade',
                          'type': 'Corretivo'},
        'gcp_mapping': 'Cloud Identity Directory, Cloud Audit Logs Admin Activity',
        'how_to_check': '1. Testar revogação de acessos de colaboradores desligados nos últimos 90 dias.\n'
                        '2. Checar tempo de resposta entre notificação de desligamento e bloqueio de conta no Cloud '
                        'Identity (< 24h).',
        'how_to_maintain': '1. Webhook automatizado entre sistema de RH e Cloud Identity para desativação instantânea.',
        'id': 'CC6.3',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (SOC 2 CRITERIA)',
        'status': 'COMPLIANT',
        'theme_key': 'SOC2_CC',
        'translations': {   'en': {   'description': 'SOC 2 CC6.3 Requirement: The entity revokes access to protected '
                                                     'information assets when access is no longer required.',
                                      'name': 'Role-Based Access Modification and Revocation',
                                      'question': 'Does the organization timely modify or revoke access to protected '
                                                  'assets when access is no longer required or upon termination?',
                                      'recommended_evidence': '• Sample of terminated personnel compared against '
                                                              'account deactivation timestamps.\n'
                                                              '• Signed HR/IT offboarding checklist.\n'
                                                              '• Admin Activity audit logs confirming timely account '
                                                              'suspension.',
                                      'theme': 'SOC 2 Security',
                                      'theme_title': 'SOC 2 — Trust Services Security Criteria'},
                            'es': {   'description': 'Requisito SOC 2 CC6.3: La entidad revoca el acceso a la '
                                                     'información protegida cuando ya no es necesario.',
                                      'name': 'Modificación y Revocación Oportuna de Accesos',
                                      'question': '¿Revoca la organización oportunamente el acceso a los activos '
                                                  'protegidos cuando ya no es necesario o tras la desvinculación?',
                                      'recommended_evidence': '• Muestra de empleados desvinculados comparada con '
                                                              'registros de suspensión de cuentas.\n'
                                                              '• Listas de verificación de desvinculación '
                                                              'completadas.\n'
                                                              '• Registros de actividad de Admin que confirman el '
                                                              'bloqueo inmediato.',
                                      'theme': 'SOC 2 Seguridad',
                                      'theme_title': 'SOC 2 — Criterios de Seguridad (Common Criteria)'},
                            'pt': {   'description': 'Requisito SOC 2 CC6.3: A entidade revoga acessos imediatamente '
                                                     'após desligamento de colaboradores ou mudança de função.',
                                      'name': 'Modificação e Revogação Tempestiva de Acessos',
                                      'question': 'A organização revoga tempestivamente o acesso a ativos protegidos '
                                                  'quando o acesso não é mais necessário ou mediante desligamento?',
                                      'recommended_evidence': '• Lista de funcionários desligados no período auditado '
                                                              'cruzada com timestamps de desativação de conta.\n'
                                                              '• Checklist de desligamento de acessos assinado por RH '
                                                              'e TI.\n'
                                                              '• Logs de atividade do Google Workspace comprovando '
                                                              'bloqueio imediato.',
                                      'theme': 'SOC 2 Segurança',
                                      'theme_title': 'SOC 2 — Critérios de Segurança (Common Criteria)'}}},
    {   'attributes': {   'capabilities': 'Segurança de Redes',
                          'concepts': 'Proteger',
                          'domains': 'Segurança de Infraestrutura',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Preventivo'},
        'gcp_mapping': 'VPC Firewall Rules, Cloud Armor, VPC Service Controls, Cloud NAT',
        'how_to_check': '1. Validar ausência de regras de firewall `0.0.0.0/0:22` e `0.0.0.0/0:3389`.\n'
                        '2. Inspecionar políticas do Cloud Armor ativas nos balanceadores de carga externos.\n'
                        '3. Checar configuração de VPC Service Controls para isolamento de dados confidenciais.',
        'how_to_maintain': '1. Organization Policy constraints: `compute.restrictVpcPeering`, '
                           '`compute.requireOsLogin`.\n'
                           '2. Alertas automáticos do Security Command Center para portas sensíveis expostas.',
        'id': 'CC6.6',
        'severity': 'CRITICAL',
        'soa_status': 'APLICÁVEL (SOC 2 CRITERIA)',
        'status': 'COMPLIANT',
        'theme_key': 'SOC2_CC',
        'translations': {   'en': {   'description': 'SOC 2 CC6.6 Requirement: The entity implements logical '
                                                     'boundaries and firewalls to protect against unauthorized access.',
                                      'name': 'Perimeter and Boundary Protection',
                                      'question': 'Does the organization implement logical boundaries, security '
                                                  'perimeters, and firewalls to protect against unauthorized external '
                                                  'access?',
                                      'recommended_evidence': '• Network architecture diagram and VPC segmentation '
                                                              'topology.\n'
                                                              '• GCP VPC firewall rules export (`gcloud compute '
                                                              'firewall-rules list`).\n'
                                                              '• Cloud Armor WAF and DDoS protection rules '
                                                              'configuration.',
                                      'theme': 'SOC 2 Security',
                                      'theme_title': 'SOC 2 — Trust Services Security Criteria'},
                            'es': {   'description': 'Requisito SOC 2 CC6.6: La entidad implementa límites lógicos y '
                                                     'cortafuegos para proteger los sistemas contra amenazas externas.',
                                      'name': 'Protección de Perímetro y Límites de Red',
                                      'question': '¿Implementa la organización límites lógicos, perímetros de '
                                                  'seguridad y cortafuegos para proteger contra accesos no '
                                                  'autorizados?',
                                      'recommended_evidence': '• Diagrama de arquitectura de red y segmentación de '
                                                              'VPC.\n'
                                                              '• Exportación de reglas de cortafuegos en GCP (`gcloud '
                                                              'compute firewall-rules list`).\n'
                                                              '• Configuración de Cloud Armor WAF y protección DDoS.',
                                      'theme': 'SOC 2 Seguridad',
                                      'theme_title': 'SOC 2 — Criterios de Seguridad (Common Criteria)'},
                            'pt': {   'description': 'Requisito SOC 2 CC6.6: A entidade implementa limites lógicos e '
                                                     'firewalls para proteger contra acessos não autorizados a partir '
                                                     'de redes externas.',
                                      'name': 'Proteção de Perímetro e Fronteiras de Rede',
                                      'question': 'A organização implementa limites lógicos, perímetros de segurança e '
                                                  'firewalls para proteger sistemas contra acessos e ameaças externas?',
                                      'recommended_evidence': '• Diagrama de arquitetura de rede e topologia de VPCs.\n'
                                                              '• Exportação de regras de firewall do GCP (`gcloud '
                                                              'compute firewall-rules list`).\n'
                                                              '• Configuração de WAF (Cloud Armor) e políticas de '
                                                              'mitigação DDoS ativas.',
                                      'theme': 'SOC 2 Segurança',
                                      'theme_title': 'SOC 2 — Critérios de Segurança (Common Criteria)'}}},
    {   'attributes': {   'capabilities': 'Monitoramento e Resposta',
                          'concepts': 'Detectar',
                          'domains': 'Gestão de Vulnerabilidades',
                          'properties': 'Confidencialidade, Integridade, Disponibilidade',
                          'type': 'Detectivo'},
        'gcp_mapping': 'Security Command Center, Cloud Monitoring, Artifact Analysis, Event Threat Detection',
        'how_to_check': '1. Verificar ativação do Security Command Center (SCC) Premium em nível organizacional.\n'
                        '2. Inspecionar varreduras automáticas de vulnerabilidades de containers (Container '
                        'Analysis/Artifact Analysis).\n'
                        '3. Validar alertas em tempo real de detecção de ameaças (Event Threat Detection).',
        'how_to_maintain': '1. Dashboard centralizado no SCC com SLA de remediação para vulnerabilidades '
                           'High/Critical.\n'
                           '2. Relatórios semanais automáticos para liderança técnica.',
        'id': 'CC7.1',
        'severity': 'HIGH',
        'soa_status': 'APLICÁVEL (SOC 2 CRITERIA)',
        'status': 'COMPLIANT',
        'theme_key': 'SOC2_CC',
        'translations': {   'en': {   'description': 'SOC 2 CC7.1 Requirement: To meet its objectives, the entity uses '
                                                     'detection and monitoring procedures to identify changes to '
                                                     'configurations and new vulnerabilities.',
                                      'name': 'Vulnerability and Threat Monitoring',
                                      'question': 'Does the organization use detection and continuous monitoring '
                                                  'procedures to identify configuration drift, threats, and security '
                                                  'vulnerabilities?',
                                      'recommended_evidence': '• Security Command Center vulnerability and posture '
                                                              'dashboards.\n'
                                                              '• Container and artifact automated vulnerability scan '
                                                              'reports.\n'
                                                              '• Annual penetration test reports and remediation '
                                                              'evidence.',
                                      'theme': 'SOC 2 Security',
                                      'theme_title': 'SOC 2 — Trust Services Security Criteria'},
                            'es': {   'description': 'Requisito SOC 2 CC7.1: La entidad utiliza procedimientos de '
                                                     'detección y monitoreo para identificar cambios en '
                                                     'configuraciones y nuevas vulnerabilidades.',
                                      'name': 'Monitoreo de Vulnerabilidades y Amenazas',
                                      'question': '¿Utiliza la organización procedimientos de detección y monitoreo '
                                                  'continuo para identificar desviaciones de configuración y '
                                                  'vulnerabilidades?',
                                      'recommended_evidence': '• Informes periódicos de vulnerabilidades en Security '
                                                              'Command Center.\n'
                                                              '• Resultados de análisis automatizado de contenedores '
                                                              'en Artifact Registry.\n'
                                                              '• Informes de pruebas de intrusión y constancias de '
                                                              'corrección de hallazgos.',
                                      'theme': 'SOC 2 Seguridad',
                                      'theme_title': 'SOC 2 — Criterios de Seguridad (Common Criteria)'},
                            'pt': {   'description': 'Requisito SOC 2 CC7.1: A entidade utiliza procedimentos de '
                                                     'detecção e monitoramento para identificar alterações em '
                                                     'configurações e vulnerabilidades de segurança.',
                                      'name': 'Monitoramento de Vulnerabilidades e Ameaças',
                                      'question': 'A organização utiliza procedimentos de detecção e monitoramento '
                                                  'contínuo para identificar vulnerabilidades e alterações anômalas '
                                                  'nas configurações?',
                                      'recommended_evidence': '• Relatórios semanais de postura de segurança e '
                                                              'vulnerabilidades do Security Command Center.\n'
                                                              '• Logs de varredura automatizada de contêineres e '
                                                              'imagens (Artifact Analysis).\n'
                                                              '• Relatório de testes de invasão e comprovação de '
                                                              'correção de falhas críticas.',
                                      'theme': 'SOC 2 Segurança',
                                      'theme_title': 'SOC 2 — Critérios de Segurança (Common Criteria)'}}}]


def get_localized_catalog(framework: str = "ISO27001:2022", lang: str = "pt") -> List[Dict[str, Any]]:
    """Returns the questionnaire controls localized for the specified framework and language.
    
    Supported languages: 'pt' (Portuguese), 'en' (English), 'es' (Spanish).
    Default language fallback is 'pt'.
    """
    norm_lang = (lang or "pt").lower().strip()
    if norm_lang not in ("pt", "en", "es"):
        norm_lang = "pt"
        
    if framework == "SOC2":
        base_list = SOC2_QUESTIONNAIRE_CATALOG
    else:
        base_list = ISO_27001_QUESTIONNAIRE_CATALOG
        
    result = []
    for item in base_list:
        trans = item.get("translations", {}).get(norm_lang, {})
        result.append({
            "id": item["id"],
            "theme_key": item.get("theme_key", ""),
            "name": trans.get("name", item["id"]),
            "theme": trans.get("theme", ""),
            "theme_title": trans.get("theme_title", ""),
            "question": trans.get("question", ""),
            "description": trans.get("description", ""),
            "recommended_evidence": trans.get("recommended_evidence", ""),
            "how_to_check": item.get("how_to_check", ""),
            "how_to_maintain": item.get("how_to_maintain", ""),
            "gcp_mapping": item.get("gcp_mapping", ""),
            "attributes": item.get("attributes", {}),
            "status": item.get("status", "NOT_ANSWERED"),
            "severity": item.get("severity", "MEDIUM"),
            "soa_status": item.get("soa_status", "APLICÁVEL"),
            "translations": item.get("translations", {}),
        })
    return result


def get_localized_themes(framework: str = "ISO27001:2022", lang: str = "pt") -> List[Dict[str, Any]]:
    """Returns the accordion theme headers for the requested framework and language."""
    norm_lang = (lang or "pt").lower().strip()
    if norm_lang not in ("pt", "en", "es"):
        norm_lang = "pt"
        
    if framework == "SOC2":
        keys = ["SOC2_CC"]
    else:
        keys = ["A.5", "A.6", "A.7", "A.8"]
        
    themes = []
    for k in keys:
        t_meta = THEMES_I18N.get(k, {}).get(norm_lang, {})
        themes.append({
            "key": k,
            "title": t_meta.get("title", k),
            "subtitle": t_meta.get("subtitle", ""),
            "short": t_meta.get("short", k),
        })
    return themes
