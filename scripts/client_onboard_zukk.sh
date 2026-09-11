#!/usr/bin/env bash
# ==============================================================================
# AGENTIC GRC: ONBOARDING READ-ONLY PARA AVALIAÇÃO DE CONFORMIDADE ISO 27001
# Cliente:              zukk.com.br
# Mandato de Segurança: STRICTLY READ-ONLY (Princípio do Menor Privilégio)
# Nenhuma permissão de escrita, alteração ou deleção de recursos é concedida.
#
# Como executar:
# Abra o Google Cloud Shell (https://shell.cloud.google.com) ou seu terminal com gcloud
# e execute este script.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m"

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}   AGENTIC GRC: CONCESSÃO DE ACESSO READ-ONLY (AVALIAÇÃO GRC)   ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "Organização/Cliente: ${BOLD}${GREEN}zukk.com.br${NC}"
echo -e "Finalidade:          Auditoria Automatizada de Conformidade ISO 27001 / SOC 2"
echo -e "Nível de Acesso:     ${BOLD}${GREEN}SOMENTE LEITURA (Least Privilege)${NC}"
echo -e "Perfis Concedidos:   roles/viewer, roles/iam.securityReviewer"
echo -e "----------------------------------------------------------------\n"

# Identidades autorizadas para a auditoria:
# 1. Service Account da plataforma Cloud Run (para varreduras automáticas de conformidade)
SA_PLATAFORMA="938078169010-compute@developer.gserviceaccount.com"

# 2. Usuário auditor/consultor responsável (para login delegado no portal)
CONSULTOR_USER="jsaccomani@google.com"

# Projetos do cliente no escopo da avaliação:
PROJECTS=(
    "hale-tractor-508012-e2"
    "projeto-vivo-viabilidade"
)

# [1/3] Verificar se gcloud está autenticado
echo -e "[1/3] Verificando sessão ativa do gcloud..."
ACTIVE_ACCOUNT=$(gcloud config get-value account 2>/dev/null || echo "")
if [ -z "${ACTIVE_ACCOUNT}" ]; then
    echo -e "${YELLOW}Nenhuma conta ativa detectada. Por favor, execute: gcloud auth login${NC}"
    exit 1
fi
echo -e "  ✓ Autenticado como: ${BOLD}${ACTIVE_ACCOUNT}${NC}\n"

# [2/3] Conceder permissões de leitura nos projetos
echo -e "[2/3] Concedendo permissões de leitura nos projetos..."

ROLES=(
    "roles/viewer"
    "roles/iam.securityReviewer"
)

for proj in "${PROJECTS[@]}"; do
    echo -e "\n  ${CYAN}▶ Configurando projeto: ${BOLD}${proj}${NC}"

    # 1. Permissões para a Service Account da Plataforma Agentic GRC
    for r in "${ROLES[@]}"; do
        echo -n "    - Concedendo ${r} para a Plataforma Cloud Run... "
        if gcloud projects add-iam-policy-binding "${proj}" \
            --member="serviceAccount:${SA_PLATAFORMA}" \
            --role="${r}" \
            --quiet >/dev/null 2>&1; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${YELLOW}Aviso: verifique se você tem permissão de Admin de IAM no projeto.${NC}"
        fi
    done

    # 2. Permissões para o Consultor/Auditor
    for r in "${ROLES[@]}"; do
        echo -n "    - Concedendo ${r} para o Consultor (${CONSULTOR_USER})... "
        if gcloud projects add-iam-policy-binding "${proj}" \
            --member="user:${CONSULTOR_USER}" \
            --role="${r}" \
            --quiet >/dev/null 2>&1; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${YELLOW}Aviso: verifique se você tem permissão de Admin de IAM no projeto.${NC}"
        fi
    done
done

# [3/3] Resumo e Comandos de Revogação Futura
echo -e "\n[3/3] Gerando recibo de onboarding..."
RECIBO="grc_onboarding_zukk_recibo.txt"
cat <<EOF > "${RECIBO}"
=================================================================
AGENTIC GRC - RECIBO DE CONCESSÃO DE ACESSO READ-ONLY
=================================================================
Cliente:             zukk.com.br
Data:                $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Projetos:            ${PROJECTS[*]}
Service Account GRC: ${SA_PLATAFORMA}
Auditor Responsável: ${CONSULTOR_USER}
Permissões:          roles/viewer, roles/iam.securityReviewer (READ-ONLY)
=================================================================
EOF

echo -e "\n${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}     ACESSO READ-ONLY CONFIGURADO COM SUCESSO!                  ${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "A plataforma Agentic GRC já está autorizada a realizar a leitura das"
echo -e "configurações de segurança e matriz de controles dos projetos informados."
echo -e "Recibo gerado: ${BOLD}${RECIBO}${NC}"

echo -e "\n${BOLD}${YELLOW}>>> COMO REVOGAR O ACESSO NO FINAL DOS TESTES: <<<${NC}"
echo -e "Quando o período de testes terminar, basta rodar o comando abaixo para remover"
echo -e "integralmente os acessos concedidos:"
echo -e "${CYAN}"
for proj in "${PROJECTS[@]}"; do
    echo "gcloud projects remove-iam-policy-binding ${proj} --member=\"serviceAccount:${SA_PLATAFORMA}\" --role=\"roles/viewer\" --quiet"
    echo "gcloud projects remove-iam-policy-binding ${proj} --member=\"serviceAccount:${SA_PLATAFORMA}\" --role=\"roles/iam.securityReviewer\" --quiet"
    echo "gcloud projects remove-iam-policy-binding ${proj} --member=\"user:${CONSULTOR_USER}\" --role=\"roles/viewer\" --quiet"
    echo "gcloud projects remove-iam-policy-binding ${proj} --member=\"user:${CONSULTOR_USER}\" --role=\"roles/iam.securityReviewer\" --quiet"
done
echo -e "${NC}================================================================\n"
