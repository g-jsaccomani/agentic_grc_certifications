"""Standalone minimal client-facing questionnaire view.

Completely isolated from the main operator portal:
- No sidebar navigation
- No chat interface
- No project selector or admin controls
- Strictly scoped to the client associated with the questionnaire token
"""

def render_client_questionnaire_html(client_name: str, client_id: str, token: str, expires_at: str) -> str:
    """Returns self-contained HTML for the client questionnaire view."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Questionário de Conformidade ISO/IEC 27001 — {client_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto+Mono:wght@400;600&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0e1217;
            --bg-secondary: #171d24;
            --bg-tertiary: #1f2732;
            --border-color: #2b3644;
            --text-primary: #f0f4f9;
            --text-secondary: #9aa0a6;
            --text-tertiary: #5f6368;
            --gcp-blue: #8ab4f8;
            --gcp-green: #81c995;
            --gcp-yellow: #fdd663;
            --gcp-red: #f28b82;
            --gcp-purple: #c58af9;
            --primary: #8ab4f8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Google Sans', 'Roboto', sans-serif;
            min-height: 100vh;
            padding: 24px;
        }}
        .client-header {{
            max-width: 1000px;
            margin: 0 auto 24px auto;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .client-title h1 {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .client-title p {{
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 4px;
        }}
        .client-badge {{
            background: rgba(138, 180, 248, 0.12);
            color: var(--gcp-blue);
            border: 1px solid rgba(138, 180, 248, 0.3);
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
        }}
        .main-container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .progress-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 24px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .progress-bar-bg {{
            flex: 1;
            height: 10px;
            background: var(--bg-tertiary);
            border-radius: 5px;
            overflow: hidden;
            min-width: 200px;
        }}
        .progress-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--gcp-blue), var(--gcp-green));
            width: 0%;
            transition: width 0.4s ease;
        }}
        .theme-section {{
            margin-bottom: 24px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
        }}
        .theme-header {{
            padding: 16px 20px;
            background: var(--bg-tertiary);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }}
        .theme-header h2 {{
            font-size: 15px;
            font-weight: 600;
        }}
        .control-card {{
            padding: 20px;
            border-top: 1px solid var(--border-color);
        }}
        .control-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
            gap: 12px;
        }}
        .ctrl-id {{
            font-family: 'Roboto Mono', monospace;
            font-weight: 700;
            background: rgba(138, 180, 248, 0.15);
            color: var(--gcp-blue);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .ctrl-name {{
            font-weight: 600;
            font-size: 14px;
            flex: 1;
        }}
        .status-badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .status-badge.COMPLIANT {{ background: rgba(129, 201, 149, 0.15); color: var(--gcp-green); border: 1px solid var(--gcp-green); }}
        .status-badge.NON_COMPLIANT {{ background: rgba(242, 139, 130, 0.15); color: var(--gcp-red); border: 1px solid var(--gcp-red); }}
        .status-badge.VERIFICAR {{ background: rgba(253, 214, 99, 0.15); color: var(--gcp-yellow); border: 1px solid var(--gcp-yellow); }}
        .status-badge.NOT_ANSWERED {{ background: rgba(154, 160, 166, 0.15); color: var(--text-secondary); border: 1px solid var(--border-color); }}
        .question-box {{
            background: rgba(138, 180, 248, 0.05);
            border-left: 3px solid var(--gcp-blue);
            padding: 10px 14px;
            margin-bottom: 14px;
            font-size: 13px;
            line-height: 1.5;
        }}
        .form-row {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 12px;
        }}
        .form-row label {{
            font-size: 11.5px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        select, textarea, input[type="text"] {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 8px 12px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 13px;
        }}
        textarea {{ resize: vertical; min-height: 70px; }}
        select:focus, textarea:focus, input[type="text"]:focus {{
            outline: none;
            border-color: var(--gcp-blue);
        }}
        .actions-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
        }}
        .btn {{
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .btn-primary {{ background: var(--gcp-blue); color: #000; }}
        .btn-primary:hover {{ background: #aecbfa; }}
        .btn-secondary {{ background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border-color); }}
        .btn-secondary:hover {{ background: #2a3442; }}
        .btn-scan {{ background: rgba(197, 138, 249, 0.2); color: var(--gcp-purple); border: 1px solid var(--gcp-purple); }}
        .btn-scan:hover {{ background: rgba(197, 138, 249, 0.35); }}
        .btn-confirm-comp {{ background: rgba(129, 201, 149, 0.2); color: var(--gcp-green); border: 1px solid var(--gcp-green); }}
        .btn-confirm-nc {{ background: rgba(242, 139, 130, 0.2); color: var(--gcp-red); border: 1px solid var(--gcp-red); }}
        .verificar-panel {{
            background: rgba(253, 214, 99, 0.08);
            border: 1px solid var(--gcp-yellow);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 12px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .msg-toast {{
            font-size: 11px;
            margin-left: 8px;
        }}
        .evidence-preview {{
            font-size: 11px;
            color: var(--text-secondary);
            font-family: 'Roboto Mono', monospace;
            background: #090c10;
            padding: 8px;
            border-radius: 4px;
            margin-top: 6px;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <header class="client-header">
        <div class="client-title">
            <h1>
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--gcp-blue);"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                {client_name}
            </h1>
            <p>Portal de Auto-Declaração & Evidências — ISO/IEC 27001:2022</p>
        </div>
        <div>
            <span class="client-badge">Sessão Segura Scoped</span>
        </div>
    </header>

    <div class="main-container">
        <div class="progress-card">
            <div>
                <strong id="answeredText">Carregando questionário...</strong>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">Progresso de preenchimento dos 93 controles normativos</div>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="progressBar"></div>
            </div>
        </div>

        <div id="controlsContainer"></div>
    </div>

    <script>
        const TOKEN = "{token}";
        const CLIENT_ID = "{client_id}";
        let questionnaireData = null;

        async function fetchQuestionnaire() {{
            try {{
                const res = await fetch(`/api/questionnaire?lang=pt`, {{
                    headers: {{ "X-Questionnaire-Token": TOKEN }}
                }});
                if (!res.ok) {{
                    document.getElementById("controlsContainer").innerHTML = `<div style="text-align:center; padding: 40px; color: var(--gcp-red);">Erro ao carregar questionário: ${{res.statusText}}</div>`;
                    return;
                }}
                questionnaireData = await res.json();
                renderControls();
            }} catch (e) {{
                document.getElementById("controlsContainer").innerHTML = `<div style="text-align:center; padding: 40px; color: var(--gcp-red);">Erro de conexão ao servidor.</div>`;
            }}
        }}

        function updateProgress() {{
            if (!questionnaireData) return;
            const controls = questionnaireData.controls || [];
            const total = controls.length || 93;
            const answered = controls.filter(c => c.status && c.status !== 'NOT_ANSWERED').length;
            const pct = Math.round((answered / total) * 100);
            document.getElementById("answeredText").innerText = `${{answered}} de ${{total}} controles respondidos (${{pct}}%)`;
            document.getElementById("progressBar").style.width = `${{pct}}%`;
        }}

        function renderControls() {{
            const container = document.getElementById("controlsContainer");
            if (!container || !questionnaireData) return;
            updateProgress();

            const themes = questionnaireData.themes || [];
            const controls = questionnaireData.controls || [];
            let html = "";

            themes.forEach(thm => {{
                const themeCtrls = controls.filter(c => c.theme_key === thm.key || (c.id && c.id.startsWith(thm.key + '.')));
                if (themeCtrls.length === 0) return;

                html += `
                <div class="theme-section">
                    <div class="theme-header">
                        <h2>${{thm.title}}</h2>
                        <span style="font-size: 12px; color: var(--text-secondary);">${{themeCtrls.length}} controles</span>
                    </div>
                    <div>
                `;

                themeCtrls.forEach(c => {{
                    const st = c.status || "NOT_ANSWERED";
                    const ans = c.answer || {{}};
                    const just = ans.justification || "";
                    const uri = ans.evidence_uri || "";
                    const evText = ans.evidence_text || "";
                    const canScan = c.can_verify_scan || false;

                    html += `
                    <div class="control-card" id="card_${{c.id}}">
                        <div class="control-top">
                            <span class="ctrl-id">${{c.id}}</span>
                            <span class="ctrl-name">${{c.name}}</span>
                            <span class="status-badge ${{st}}" id="badge_${{c.id}}">${{st}}</span>
                        </div>
                        <div class="question-box">${{c.question || c.description}}</div>

                        ${{st === 'VERIFICAR' ? `
                        <div class="verificar-panel" id="verificarPanel_${{c.id}}">
                            <div>
                                <strong style="color: var(--gcp-yellow);">🔍 Telemetria Live Coletada (VERIFICAR)</strong>
                                <p style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;">Evidência verificada via Cloud Inspector. Confirme a conformidade:</p>
                                ${{evText ? `<div class="evidence-preview">${{evText}}</div>` : ''}}
                            </div>
                            <div style="display: flex; gap: 8px;">
                                <button class="btn btn-confirm-comp" onclick="confirmVerification('${{c.id}}', 'COMPLIANT')">✓ Confirmar Conforme</button>
                                <button class="btn btn-confirm-nc" onclick="confirmVerification('${{c.id}}', 'NON_COMPLIANT')">✗ Marcar Não Conforme</button>
                            </div>
                        </div>
                        ` : ''}}

                        <div class="form-row">
                            <label>Status de Conformidade</label>
                            <select id="status_${{c.id}}">
                                <option value="NOT_ANSWERED" ${{st==='NOT_ANSWERED'?'selected':''}}>Não Respondido</option>
                                <option value="COMPLIANT" ${{st==='COMPLIANT'?'selected':''}}>✓ Conforme</option>
                                <option value="NON_COMPLIANT" ${{st==='NON_COMPLIANT'?'selected':''}}>✗ Não Conforme</option>
                                <option value="PARTIAL" ${{st==='PARTIAL'?'selected':''}}>⚠ Parcial</option>
                                <option value="NOT_APPLICABLE" ${{st==='NOT_APPLICABLE'?'selected':''}}>— Não Aplicável</option>
                            </select>
                        </div>

                        <div class="form-row">
                            <label>Justificativa / Declaração da Organização</label>
                            <textarea id="just_${{c.id}}" placeholder="Descreva os processos e controles adotados...">${{just}}</textarea>
                        </div>

                        <div class="form-row">
                            <label>Link ou URI da Evidência</label>
                            <input type="text" id="uri_${{c.id}}" value="${{uri}}" placeholder="gs://... ou https://drive.google.com/...">
                        </div>

                        <div class="actions-row">
                            <div>
                                <input type="file" id="file_${{c.id}}" style="display:none;" onchange="uploadFile('${{c.id}}', this)">
                                <button class="btn btn-secondary" onclick="document.getElementById('file_${{c.id}}').click()">📎 Anexar Evidência</button>
                                ${{canScan ? `<button class="btn btn-scan" onclick="triggerScanVerify('${{c.id}}')">🔍 Verificar via Scan</button>` : ''}}
                            </div>
                            <div>
                                <button class="btn btn-primary" onclick="saveAnswer('${{c.id}}')">Salvar Resposta</button>
                                <span id="toast_${{c.id}}" class="msg-toast"></span>
                            </div>
                        </div>
                    </div>
                    `;
                }});

                html += `</div></div>`;
            }});

            container.innerHTML = html;
        }}

        async function saveAnswer(controlId) {{
            const status = document.getElementById(`status_${{controlId}}`).value;
            const justification = document.getElementById(`just_${{controlId}}`).value;
            const uri = document.getElementById(`uri_${{controlId}}`).value;
            const toast = document.getElementById(`toast_${{controlId}}`);

            toast.innerText = "Salvando...";
            toast.style.color = "var(--text-secondary)";

            try {{
                const res = await fetch(`/api/questionnaire/${{controlId}}/answer`, {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json",
                        "X-Questionnaire-Token": TOKEN
                    }},
                    body: JSON.stringify({{
                        control_id: controlId,
                        status: status,
                        justification: justification,
                        evidence_uri: uri
                    }})
                }});
                const data = await res.json();
                if (!res.ok) {{
                    toast.innerText = data.detail || "Erro ao salvar";
                    toast.style.color = "var(--gcp-red)";
                    return;
                }}
                toast.innerText = "✓ Salvo";
                toast.style.color = "var(--gcp-green)";
                const badge = document.getElementById(`badge_${{controlId}}`);
                if (badge) {{
                    badge.className = `status-badge ${{data.status}}`;
                    badge.innerText = data.status;
                }}
                const c = questionnaireData.controls.find(x => x.id === controlId);
                if (c) {{ c.status = data.status; c.answer = data; }}
                updateProgress();
            }} catch (e) {{
                toast.innerText = "Erro ao enviar";
                toast.style.color = "var(--gcp-red)";
            }}
        }}

        async function triggerScanVerify(controlId) {{
            const toast = document.getElementById(`toast_${{controlId}}`);
            toast.innerText = "Executando scan...";
            toast.style.color = "var(--gcp-purple)";

            try {{
                const res = await fetch(`/api/questionnaire/${{controlId}}/verify_scan`, {{
                    method: "POST",
                    headers: {{ "X-Questionnaire-Token": TOKEN }}
                }});
                const data = await res.json();
                if (!res.ok) {{
                    toast.innerText = data.detail || "Scan falhou";
                    toast.style.color = "var(--gcp-red)";
                    return;
                }}
                toast.innerText = "✓ Scan concluído (Status: VERIFICAR)";
                toast.style.color = "var(--gcp-yellow)";
                const c = questionnaireData.controls.find(x => x.id === controlId);
                if (c) {{ c.status = data.status; c.answer = data; }}
                renderControls();
            }} catch (e) {{
                toast.innerText = "Erro ao executar scan";
                toast.style.color = "var(--gcp-red)";
            }}
        }}

        async function confirmVerification(controlId, decision) {{
            try {{
                const res = await fetch(`/api/questionnaire/${{controlId}}/confirm_verification`, {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json",
                        "X-Questionnaire-Token": TOKEN
                    }},
                    body: JSON.stringify({{ decision: decision }})
                }});
                const data = await res.json();
                if (!res.ok) {{
                    alert(data.detail || "Erro ao confirmar");
                    return;
                }}
                const c = questionnaireData.controls.find(x => x.id === controlId);
                if (c) {{ c.status = data.status; c.answer = data; }}
                renderControls();
            }} catch (e) {{
                alert("Erro ao confirmar verificação.");
            }}
        }}

        async function uploadFile(controlId, inputEl) {{
            if (!inputEl.files || inputEl.files.length === 0) return;
            const file = inputEl.files[0];
            const toast = document.getElementById(`toast_${{controlId}}`);
            toast.innerText = "Enviando arquivo...";

            const fd = new FormData();
            fd.append("file", file);

            try {{
                const res = await fetch(`/api/questionnaire/${{controlId}}/evidence-file`, {{
                    method: "POST",
                    headers: {{ "X-Questionnaire-Token": TOKEN }},
                    body: fd
                }});
                const data = await res.json();
                if (!res.ok) {{
                    toast.innerText = data.detail || "Upload rejeitado";
                    toast.style.color = "var(--gcp-red)";
                    return;
                }}
                toast.innerText = "✓ Arquivo validado e anexado";
                toast.style.color = "var(--gcp-green)";
            }} catch (e) {{
                toast.innerText = "Erro no upload";
                toast.style.color = "var(--gcp-red)";
            }}
        }}

        fetchQuestionnaire();
    </script>
</body>
</html>
"""
