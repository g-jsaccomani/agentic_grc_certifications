# Guia de POC — Agentic GRC Auditor (ISO/IEC 27001:2022)

## 0. Antes de começar

- [ ] Ambiente populado com dados **mascarados/simulados** do cliente (nomes de projeto, buckets,
      chaves — nunca dados reais de produção do cliente numa POC).
- [ ] Login Google Workspace configurado para o domínio real usado na POC (não `client.corp`) —
      confirme em Google Cloud Console → Credenciais OAuth → Origens JavaScript autorizadas.
- [ ] `min-instances=1` no Cloud Run, pra evitar cold start e perda de estado em memória durante
      a sessão de POC.
- [ ] Um projeto GCP real (mesmo que só com dados simulados) conectado, pra mostrar a inspeção
      viva funcionando de ponta a ponta.

## 1. Login

1. Acesse a URL do portal.
2. Clique em "Sign in" — confirme que loga com uma conta real do domínio Workspace da POC.
3. **Verificação de segurança a fazer na frente do cliente, se quiser demonstrar confiança**:
   tente acessar o chat em uma aba anônima, sem logar. Isso deveria ser barrado (ver nota de
   correção pendente — hoje não é, é o primeiro ajuste antes de qualquer POC real).

## 2. Primeira exploração — tela inicial

1. Mostre a tela inicial simplificada: caixa de pergunta + 3 sugestões em linguagem simples.
2. Faça uma pergunta informal, tipo "meus dados estão criptografados?" — mostre que a IA
   responde de forma conversacional, mas baseada em ferramenta real, não em texto pronto.
3. Aponte o badge do módulo ativo ("ISO/IEC 27001:2022") e, se quiser, abra o seletor de
   frameworks pra mostrar SOC2/PCI/CMMI como roadmap — é honesto e mostra visão de produto.

## 3. Preenchimento do questionário

1. Abra "Questionário" no menu principal.
2. Escolha 3-5 controles representativos de temas diferentes (ex: um de A.5, um de A.8).
3. Para cada um: selecione o status, escreva uma justificativa curta, e anexe uma evidência
   (imagem, PDF ou texto — mostre a validação de tipo de arquivo rejeitando algo fora da lista
   permitida, se quiser reforçar o argumento de segurança).
4. Aponte o veredito de IA (`ai_consistency_verdict`) aparecendo ao lado do que o usuário
   declarou — essa é a peça que prova que a ferramenta não aceita afirmação sem checagem.

## 4. Inspeção viva (se o projeto GCP estiver conectado)

1. No chat, pergunte sobre um recurso real do projeto conectado (ex: "audite o bucket X").
2. Mostre a resposta trazendo dado real (PAP, UBLA) — não simulado.
3. Se por algum motivo a credencial falhar, mostre que o sistema diz "não consegui verificar",
   nunca inventa um resultado — esse é o argumento central de confiança da ferramenta.

## 5. Scorecard e dashboard

1. Abra "Relatórios" → aba Scorecard.
2. Mostre a distinção entre achados **verificados por telemetria** e **autodeclarados via
   questionário** — isso é o diferencial da ferramenta frente a um questionário de Excel comum.

## 6. Exportação do relatório

1. Abra "Relatórios" → Dossiê Executivo (para o C-level do cliente) e Relatório Técnico
   (para o time de segurança do cliente).
2. Aponte o hash SHA-256 de evidência em cada achado — isso é o "selo de autenticidade" que
   prova que o relatório não foi editado à mão depois de gerado.
3. Exporte e envie o PDF/documento gerado.

## O que dizer com transparência durante a POC

- Multi-cloud (AWS/Azure/OCI): "está no roadmap, a arquitetura já foi pensada pra isso, ainda
  não está ativo."
- Outras certificações (SOC2/PCI/CMMI): mesma resposta — roadmap, não recurso hoje.
- A inspeção viva do GCP é uma capacidade nova — se ainda não foi validada em escala,
  não prometa cobertura de 100% dos serviços GCP ainda.

## Pendência de segurança a resolver antes de uma POC com qualquer dado sensível

O chat hoje responde sem exigir login. Antes de rodar a POC com qualquer coisa além de dados
100% sintéticos, aplicar a correção de autenticação (ver prompt em anexo na conversa).
