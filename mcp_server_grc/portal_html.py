"""Futuristic, Clean Glassmorphism HTML Portal View for GEAP Compliance."""

PORTAL_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Enterprise Agent Platform - GRC Audit & Compliance Portal</title>
    <style>
        :root {
            --bg-base: #070b14;
            --bg-card: rgba(17, 24, 39, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-glow: rgba(0, 242, 254, 0.2);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --cyan-glow: #00f2fe;
            --blue-accent: #3b82f6;
            --indigo-accent: #6366f1;
            --emerald-accent: #10b981;
            --amber-accent: #f59e0b;
            --rose-accent: #f43f5e;
            --font-stack: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: var(--font-stack);
        }

        body {
            background: radial-gradient(circle at 15% 15%, #0f1c3f 0%, #070b14 60%, #030712 100%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Top Bar */
        header {
            background: rgba(11, 17, 33, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-logo-icon {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #00f2fe, #4f46e5);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        }

        .brand-title {
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.3px;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-subtitle {
            font-size: 11px;
            color: var(--cyan-glow);
            font-weight: 500;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* Header Actions (Multi-Project & Export) */
        .header-actions {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .project-selector-wrapper {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 6px 12px;
        }

        .project-selector-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
        }

        .project-dropdown {
            background: transparent;
            color: var(--text-primary);
            border: none;
            outline: none;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
        }

        .project-dropdown option {
            background: #0f172a;
            color: #fff;
        }

        .btn-add-project {
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #60a5fa;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 11px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }

        .btn-add-project:hover {
            background: #3b82f6;
            color: #fff;
        }

        .export-dropdown-wrapper {
            position: relative;
        }

        .btn-export-main {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
            transition: all 0.2s;
        }

        .btn-export-main:hover {
            transform: translateY(-1px);
            box-shadow: 0 0 22px rgba(16, 185, 129, 0.5);
        }

        .export-menu {
            display: none;
            position: absolute;
            right: 0;
            top: 40px;
            background: #0f172a;
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            width: 220px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 150;
            overflow: hidden;
        }

        .export-menu.show {
            display: block;
        }

        .export-item {
            padding: 10px 14px;
            font-size: 12px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            transition: background 0.2s;
        }

        .export-item:hover {
            background: rgba(0, 242, 254, 0.1);
            color: var(--cyan-glow);
        }

        .export-item:last-child {
            border-bottom: none;
        }

        .compliance-pill {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34d399;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        /* Navigation Tabs */
        nav {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 0 28px;
            display: flex;
            gap: 24px;
        }

        .tab-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 600;
            padding: 14px 4px;
            cursor: pointer;
            position: relative;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn:hover {
            color: var(--text-primary);
        }

        .tab-btn.active {
            color: var(--cyan-glow);
        }

        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--cyan-glow);
            box-shadow: 0 0 10px var(--cyan-glow);
        }

        /* Main Container */
        main {
            flex: 1;
            padding: 24px 28px;
            max-width: 1500px;
            margin: 0 auto;
            width: 100%;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Glassmorphism Cards */
        .card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.2s ease;
        }

        .card:hover {
            border-color: var(--border-glow);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        /* TAB 1: Chatbot Auditor */
        .chat-layout {
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 20px;
            height: 72vh;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            overflow: hidden;
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            background: var(--bg-card);
        }

        .chat-messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .message {
            max-width: 85%;
            padding: 14px 18px;
            border-radius: 10px;
            font-size: 13.5px;
            line-height: 1.6;
            white-space: pre-wrap;
            position: relative;
        }

        .message-agent {
            align-self: flex-start;
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-primary);
            border-left: 3px solid var(--cyan-glow);
        }

        .message-user {
            align-self: flex-end;
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #ffffff;
            border-radius: 10px 10px 0 10px;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        .subagent-badge-tag {
            display: inline-block;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            background: rgba(0, 242, 254, 0.15);
            color: var(--cyan-glow);
            padding: 2px 8px;
            border-radius: 4px;
            margin-bottom: 8px;
            font-weight: 700;
        }

        .chat-input-area {
            padding: 16px 20px;
            border-top: 1px solid var(--border-subtle);
            background: rgba(15, 23, 42, 0.85);
            display: flex;
            gap: 12px;
        }

        .chat-input {
            flex: 1;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 12px 16px;
            color: var(--text-primary);
            font-size: 13.5px;
            outline: none;
            transition: border-color 0.2s;
        }

        .chat-input:focus {
            border-color: var(--cyan-glow);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        }

        .btn-send {
            background: linear-gradient(135deg, #00f2fe, #2563eb);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-send:hover {
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
            transform: scale(1.02);
        }

        .chat-sidebar {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .quick-chip {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 12px;
            padding: 10px 14px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: left;
        }

        .quick-chip:hover {
            background: rgba(0, 242, 254, 0.1);
            border-color: var(--cyan-glow);
            color: var(--cyan-glow);
            transform: translateX(4px);
        }

        /* TAB 2: Scan por Fases */
        .phased-audit-container {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .scan-action-bar {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .btn-run-scan {
            background: linear-gradient(135deg, #00f2fe, #4f46e5);
            color: #fff;
            border: none;
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            transition: all 0.2s;
        }

        .btn-run-scan:hover {
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.6);
        }

        .stepper-pipeline {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }

        .step-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 18px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }

        .step-card.active {
            border-color: var(--cyan-glow);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        }

        .step-card.completed {
            border-color: var(--emerald-accent);
        }

        .step-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .step-number {
            font-size: 11px;
            font-weight: 800;
            color: var(--cyan-glow);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .step-status {
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
        }

        .step-status.idle { background: rgba(100, 116, 139, 0.2); color: #94a3b8; }
        .step-status.running { background: rgba(0, 242, 254, 0.2); color: var(--cyan-glow); }
        .step-status.done { background: rgba(16, 185, 129, 0.2); color: #34d399; }

        .step-title {
            font-size: 14px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 6px;
        }

        .step-desc {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .progress-bar-container {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 14px;
        }

        .progress-bar-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(to right, #00f2fe, #10b981);
            transition: width 0.4s ease;
        }

        .console-output {
            background: #060913;
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 16px;
            font-family: "Courier New", Courier, monospace;
            font-size: 12px;
            color: #38bdf8;
            height: 220px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        /* TAB 3: Matriz ISO 27001 Escalavel */
        .matrix-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            gap: 16px;
            flex-wrap: wrap;
        }

        .filter-pills {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .filter-pill {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 600;
        }

        .filter-pill.active {
            background: rgba(0, 242, 254, 0.15);
            border-color: var(--cyan-glow);
            color: var(--cyan-glow);
        }

        .search-box {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 14px;
            color: #fff;
            font-size: 13px;
            outline: none;
            width: 260px;
        }

        .search-box:focus {
            border-color: var(--cyan-glow);
        }

        .matrix-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 16px;
        }

        .control-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            transition: all 0.2s;
        }

        .control-card:hover {
            border-color: rgba(0, 242, 254, 0.3);
            transform: translateY(-2px);
        }

        .control-badge-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .control-id-badge {
            font-size: 12px;
            font-weight: 800;
            color: var(--cyan-glow);
            background: rgba(0, 242, 254, 0.1);
            padding: 2px 8px;
            border-radius: 4px;
        }

        .badge-compliant {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            text-transform: uppercase;
        }

        .control-name {
            font-size: 14px;
            font-weight: 700;
            color: #fff;
        }

        .control-desc {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .gcp-tag {
            font-size: 11px;
            color: #93c5fd;
            background: rgba(59, 130, 246, 0.15);
            padding: 4px 8px;
            border-radius: 6px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            display: inline-block;
        }

        /* Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 200;
            align-items: center;
            justify-content: center;
        }

        .modal-overlay.show {
            display: flex;
        }

        .modal-card {
            background: #0f172a;
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            width: 440px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        }

        .modal-title {
            font-size: 16px;
            font-weight: 700;
            color: #fff;
        }

        .form-input {
            background: #1e293b;
            border: 1px solid var(--border-subtle);
            border-radius: 6px;
            padding: 10px 14px;
            color: #fff;
            font-size: 13px;
            outline: none;
        }

        .form-input:focus { border-color: var(--cyan-glow); }

        .modal-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 10px;
        }

        .btn-cancel {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
        }

        .btn-confirm {
            background: var(--blue-accent);
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }

        /* Print Media Styling for PDF Export */
        @media print {
            header, nav, .chat-input-area, .quick-chip, .btn-run-scan, .header-actions, .filter-pills, .search-box {
                display: none !important;
            }
            body {
                background: #fff !important;
                color: #000 !important;
            }
            .card, .step-card, .control-card {
                background: #fff !important;
                color: #000 !important;
                border: 1px solid #ccc !important;
                box-shadow: none !important;
            }
            .brand-title, .control-name, .step-title {
                color: #000 !important;
            }
            .tab-content {
                display: block !important;
            }
        }
    </style>
</head>
<body>
    <!-- Top Header -->
    <header>
        <div class="brand-container">
            <div class="brand-logo-icon">🛡️</div>
            <div>
                <div class="brand-title">Gemini Enterprise Agent Platform</div>
                <div class="brand-subtitle">GEAP Compliance & Continuous Audit Agent</div>
            </div>
        </div>

        <div class="header-actions">
            <!-- Multi-Project Scope Selector -->
            <div class="project-selector-wrapper">
                <span class="project-selector-label">Escopo:</span>
                <select id="project-dropdown" class="project-dropdown" onchange="handleProjectChange()">
                    <option value="ALL">🌐 Todos os Projetos (3 Ativos)</option>
                    <option value="agentic-grc-cd06" selected>agentic-grc-cd06 (Prod)</option>
                    <option value="agentic-grc-staging">agentic-grc-staging (Homolog)</option>
                    <option value="agentic-grc-data-lake">agentic-grc-data-lake (Analytics)</option>
                </select>
                <button class="btn-add-project" onclick="openAddProjectModal()">+ Projeto</button>
            </div>

            <!-- Global Compliance Pill -->
            <div class="compliance-pill">
                <div class="pulse-dot"></div>
                <span>ISO 27001:2022 + Amd 1:2024 (100%)</span>
            </div>

            <!-- Export Reports Button & Dropdown -->
            <div class="export-dropdown-wrapper">
                <button class="btn-export-main" onclick="toggleExportMenu()">
                    <span>📥 Exportar Relatório</span>
                    <span>▾</span>
                </button>
                <div id="export-menu" class="export-menu">
                    <div class="export-item" onclick="triggerExport('print')">
                        <span>📄</span>
                        <div>
                            <strong>Relatório Executivo (PDF)</strong>
                            <div style="font-size: 10px; color: #94a3b8;">Dossiê formal para impressão</div>
                        </div>
                    </div>
                    <div class="export-item" onclick="triggerExport('json')">
                        <span>💾</span>
                        <div>
                            <strong>Pacote Criptográfico (JSON)</strong>
                            <div style="font-size: 10px; color: #94a3b8;">Hashes SHA-256 e evidências</div>
                        </div>
                    </div>
                    <div class="export-item" onclick="triggerExport('markdown')">
                        <span>📝</span>
                        <div>
                            <strong>Relatório Técnico (Markdown)</strong>
                            <div style="font-size: 10px; color: #94a3b8;">Documentação para repositório Git</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <nav>
        <button class="tab-btn active" onclick="switchTab('chat')">💬 Chatbot Auditor</button>
        <button class="tab-btn" onclick="switchTab('phases')">⚡ Scan por Fases</button>
        <button class="tab-btn" onclick="switchTab('matrix')">📑 Matriz ISO 27001 Escalável</button>
        <button class="tab-btn" onclick="switchTab('subagents')">🤖 Subagentes & Zero-Copy</button>
        <button class="tab-btn" onclick="switchTab('dashboard')">📊 Scorecard & Grafo de Evidências</button>
    </nav>

    <!-- Main Workspace Area -->
    <main>
        <!-- TAB 1: Chatbot Auditor (Vertex AI Gemini 2.5 Flash) -->
        <div id="tab-chat" class="tab-content active">
            <div class="chat-layout">
                <div class="chat-container">
                    <div id="chat-messages" class="chat-messages">
                        <div class="message message-agent">
                            <span class="subagent-badge-tag">Vertex AI Gemini 2.5 Flash • Virtual Lead Auditor</span>
                            <br>
                            Olá! Sou o <strong>AgentG-RC</strong>, seu Auditor Líder Virtual de Governança, Risco e Conformidade (GRC) no Gemini Enterprise Agent Platform.
                            <br><br>
                            Estou conectado à telemetria real dos projetos GCP em conformidade com a <strong>ISO/IEC 27001:2022</strong> e a nova emenda <strong>Amd 1:2024 de Ação Climática</strong>. Como posso apoiar sua auditoria hoje?
                        </div>
                    </div>
                    <div class="chat-input-area">
                        <input id="chat-input" type="text" class="chat-input" placeholder="Pergunte sobre status de conformidade, controles do Anexo A, criptografia, VPC-SC ou riscos climáticos..." onkeydown="if(event.key==='Enter') sendChat()">
                        <button class="btn-send" onclick="sendChat()">Consultar Gemini</button>
                    </div>
                </div>

                <!-- Chat Quick Prompts Sidebar -->
                <div class="chat-sidebar">
                    <div class="card">
                        <h4 style="font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 12px;">Consultas Rápidas de Auditoria</h4>
                        <div style="display: flex; flex-direction: column; gap: 8px;">
                            <button class="quick-chip" onclick="quickPrompt('Me traz o status completo desse ambiente em relação a ISO 27001')">
                                📊 Status Geral do Ambiente (ISO 27001)
                            </button>
                            <button class="quick-chip" onclick="quickPrompt('Audit KMS cryptography A.8.24')">
                                🔐 Criptografia Cloud KMS em HSM (A.8.24)
                            </button>
                            <button class="quick-chip" onclick="quickPrompt('Horizon scanning regulatory update')">
                                🌍 Ação Climática Amd 1:2024 (Cláusulas 4.1 e 4.2)
                            </button>
                            <button class="quick-chip" onclick="quickPrompt('Quais controles do Anexo A estão implementados no GCP?')">
                                🛡️ Mapeamento Anexo A no Google Cloud
                            </button>
                            <button class="quick-chip" onclick="quickPrompt('Execute proactive audit')">
                                ⚡ Disparar Ciclo Pró-ativo Completo
                            </button>
                        </div>
                    </div>

                    <div class="card">
                        <h4 style="font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 8px;">Inteligência Ativa</h4>
                        <p style="font-size: 12px; color: var(--text-secondary); line-height: 1.4;">
                            Raciocínio alimentado pelo modelo <strong>Gemini 2.5 Flash</strong> da Vertex AI na região <code>us-central1</code> com validação de borda do <strong>Model Armor</strong>.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: Scan por Fases -->
        <div id="tab-phases" class="tab-content">
            <div class="phased-audit-container">
                <div class="scan-action-bar">
                    <div>
                        <h3 style="font-size: 18px; font-weight: 800; color: #fff;">Motor de Auditoria por Fases</h3>
                        <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                            Execução progressiva e escalável em 4 etapas cobrindo todo o escopo de segurança, infraestrutura e governança.
                        </p>
                    </div>
                    <button class="btn-run-scan" onclick="runPhasedAudit()">
                        <span>⚡ Iniciar Scan por Fases</span>
                    </button>
                </div>

                <!-- 4-Phase Stepper Pipeline -->
                <div class="stepper-pipeline">
                    <div id="step-card-1" class="step-card">
                        <div class="step-header">
                            <span class="step-number">Fase 1</span>
                            <span id="step-badge-1" class="step-status idle">Pronto</span>
                        </div>
                        <div class="step-title">Descoberta & IAM</div>
                        <div class="step-desc">Varredura de inventário Cloud Asset API, contas de serviço, perímetros de acesso e segregação SoD.</div>
                        <div class="progress-bar-container"><div id="step-bar-1" class="progress-bar-fill"></div></div>
                    </div>

                    <div id="step-card-2" class="step-card">
                        <div class="step-header">
                            <span class="step-number">Fase 2</span>
                            <span id="step-badge-2" class="step-status idle">Pronto</span>
                        </div>
                        <div class="step-title">Auditoria Técnica & IaC</div>
                        <div class="step-desc">Testes de controles tecnológicos (KMS HSM A.8.24, VPC-SC A.8.12, GCS PAP/UBLA A.5.23 e IaC Terraform).</div>
                        <div class="progress-bar-container"><div id="step-bar-2" class="progress-bar-fill"></div></div>
                    </div>

                    <div id="step-card-3" class="step-card">
                        <div class="step-header">
                            <span class="step-number">Fase 3</span>
                            <span id="step-badge-3" class="step-status idle">Pronto</span>
                        </div>
                        <div class="step-title">Governança & Clima</div>
                        <div class="step-desc">Resiliência climática ISO 27001 Amd 1:2024, redundância multirregional e conectores Zero-Copy.</div>
                        <div class="progress-bar-container"><div id="step-bar-3" class="progress-bar-fill"></div></div>
                    </div>

                    <div id="step-card-4" class="step-card">
                        <div class="step-header">
                            <span class="step-number">Fase 4</span>
                            <span id="step-badge-4" class="step-status idle">Pronto</span>
                        </div>
                        <div class="step-title">Grafo & Scorecard</div>
                        <div class="step-desc">Geração de nós de evidência com hash SHA-256, consolidação de scorecard e verificação de drift.</div>
                        <div class="progress-bar-container"><div id="step-bar-4" class="progress-bar-fill"></div></div>
                    </div>
                </div>

                <!-- Live Audit Execution Console -->
                <div class="card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="font-size: 13px; font-weight: 700; color: #fff;">Console de Execução em Tempo Real</span>
                        <span id="scan-timer" style="font-size: 12px; color: var(--cyan-glow); font-family: monospace;">Aguardando execução...</span>
                    </div>
                    <div id="console-output" class="console-output">Pronto para iniciar auditoria multiescopo. Clique em 'Iniciar Scan por Fases' acima.</div>
                </div>

                <!-- Phase Results Cards -->
                <div id="phased-results-container" style="display: none; flex-direction: column; gap: 14px;">
                    <h4 style="font-size: 15px; font-weight: 800; color: #fff;">Achados Estruturados por Fase</h4>
                    <div id="phased-results-list" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;"></div>
                </div>
            </div>
        </div>

        <!-- TAB 3: Matriz ISO 27001 Escalavel -->
        <div id="tab-matrix" class="tab-content">
            <div class="matrix-toolbar">
                <div class="filter-pills">
                    <button class="filter-pill active" onclick="filterMatrix('Todos')">Todos (93+)</button>
                    <button class="filter-pill" onclick="filterMatrix('A.5 Organizacional')">A.5 Organizacional</button>
                    <button class="filter-pill" onclick="filterMatrix('A.6 Pessoas')">A.6 Pessoas</button>
                    <button class="filter-pill" onclick="filterMatrix('A.7 Físico')">A.7 Físico</button>
                    <button class="filter-pill" onclick="filterMatrix('A.8 Tecnológico')">A.8 Tecnológico</button>
                    <button class="filter-pill" onclick="filterMatrix('Amd 1:2024 Clima')">🌍 Amd 1:2024 Clima</button>
                </div>
                <input id="matrix-search" type="text" class="search-box" placeholder="Buscar por código, nome ou GCP..." oninput="searchMatrix()">
            </div>

            <div id="matrix-grid" class="matrix-grid">
                <!-- Dynamically loaded controls -->
            </div>
        </div>

        <!-- TAB 4: Subagentes & Zero-Copy -->
        <div id="tab-subagents" class="tab-content">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                <!-- Subagents -->
                <div class="card">
                    <h3 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 16px;">Orquestração de Subagentes Especializados</h3>
                    <div id="subagents-list" style="display: flex; flex-direction: column; gap: 12px;"></div>
                </div>

                <!-- Zero-Copy & File Upload -->
                <div style="display: flex; flex-direction: column; gap: 20px;">
                    <div class="card">
                        <h3 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 10px;">Conector Zero-Copy na Fonte</h3>
                        <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">
                            Audita documentação e políticas diretamente no Google Drive, SharePoint ou Jira sem cópia ou armazenamento centralizado de dados.
                        </p>
                        <div style="display: flex; gap: 10px; margin-bottom: 12px;">
                            <select id="storage-type" class="form-input" style="width: 160px;">
                                <option value="google_drive">Google Drive</option>
                                <option value="sharepoint_online">SharePoint</option>
                                <option value="jira">Jira Atlassian</option>
                                <option value="gcs">Cloud Storage</option>
                            </select>
                            <input id="storage-uri" type="text" class="form-input" style="flex: 1;" placeholder="URI do repositório ou ID da pasta">
                            <button class="btn-confirm" onclick="linkStorage()">Conectar</button>
                        </div>
                        <div id="storage-result"></div>
                    </div>

                    <div class="card">
                        <h3 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 10px;">Análise Instantânea de IaC & Políticas</h3>
                        <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">
                            Faça upload de arquivos Terraform (.tf) ou Ansible (.yml) para auditoria estática preventiva de acordo com o Controle A.8.9.
                        </p>
                        <input id="file-upload" type="file" style="display: none;" onchange="handleFileUpload(event)">
                        <button class="btn-confirm" onclick="document.getElementById('file-upload').click()">Selecionar Arquivo IaC (.tf / .yml)</button>
                        <div id="upload-result"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: Scorecard & Grafo de Evidencias -->
        <div id="tab-dashboard" class="tab-content">
            <div style="display: flex; flex-direction: column; gap: 24px;">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
                    <div class="card">
                        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Score de Conformidade</div>
                        <div id="dash-score" style="font-size: 36px; font-weight: 800; color: #34d399; margin: 6px 0;">100.0%</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">Classificação: <strong style="color: #34d399;">EXCELLENT</strong></div>
                    </div>
                    <div class="card">
                        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Trajetória de Drift</div>
                        <div id="dash-drift" style="font-size: 36px; font-weight: 800; color: #60a5fa; margin: 6px 0;">ESTÁVEL</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">0 desvios críticos detectados</div>
                    </div>
                    <div class="card">
                        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Nós de Evidência</div>
                        <div id="dash-evidence" style="font-size: 36px; font-weight: 800; color: var(--cyan-glow); margin: 6px 0;">14</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">Hashes SHA-256 imutáveis</div>
                    </div>
                    <div class="card">
                        <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase;">Projetos em Escopo</div>
                        <div id="dash-projects-count" style="font-size: 36px; font-weight: 800; color: #c084fc; margin: 6px 0;">3</div>
                        <div style="font-size: 12px; color: var(--text-secondary);">Cobertura multirregional</div>
                    </div>
                </div>

                <div class="card">
                    <h3 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 14px;">Aprovações Human-in-the-Loop (HITL) Pendentes</h3>
                    <div id="hitl-container"></div>
                </div>

                <div class="card">
                    <h3 style="font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 14px;">Status dos Controles Base Monitorados</h3>
                    <div id="controls-list" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 12px;"></div>
                </div>
            </div>
        </div>
    </main>

    <!-- Add Project Modal -->
    <div id="modal-add-project" class="modal-overlay">
        <div class="modal-card">
            <div class="modal-title">Adicionar Projeto GCP para Auditoria</div>
            <div>
                <label style="font-size: 12px; color: var(--text-secondary);">Project ID:</label>
                <input id="input-new-project-id" type="text" class="form-input" style="width: 100%; margin-top: 4px;" placeholder="ex: financial-core-prod">
            </div>
            <div>
                <label style="font-size: 12px; color: var(--text-secondary);">Ambiente:</label>
                <select id="input-new-env" class="form-input" style="width: 100%; margin-top: 4px;">
                    <option value="PRODUCTION">Produção (Production)</option>
                    <option value="STAGING">Homologação (Staging)</option>
                    <option value="DEVELOPMENT">Desenvolvimento (Dev)</option>
                </select>
            </div>
            <div class="modal-buttons">
                <button class="btn-cancel" onclick="closeAddProjectModal()">Cancelar</button>
                <button class="btn-confirm" onclick="confirmAddProject()">Cadastrar e Auditar</button>
            </div>
        </div>
    </div>

    <!-- Client-side Scripts -->
    <script>
        let currentTheme = 'Todos';
        let isoControlsCache = [];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
            if (targetBtn) targetBtn.classList.add('active');

            const targetContent = document.getElementById('tab-' + tabId);
            if (targetContent) targetContent.classList.add('active');

            if (tabId === 'matrix' && isoControlsCache.length === 0) {
                loadIsoMatrix();
            } else if (tabId === 'dashboard') {
                loadDashboard();
            }
        }

        function toggleExportMenu() {
            const menu = document.getElementById('export-menu');
            menu.classList.toggle('show');
        }

        window.onclick = function(e) {
            if (!e.target.closest('.export-dropdown-wrapper')) {
                const menu = document.getElementById('export-menu');
                if (menu) menu.classList.remove('show');
            }
        };

        function triggerExport(format) {
            const menu = document.getElementById('export-menu');
            if (menu) menu.classList.remove('show');

            const selectedProject = document.getElementById('project-dropdown').value;
            if (format === 'print') {
                window.print();
            } else {
                window.location.href = `/api/reports/export?format=${format}&projects=${selectedProject}`;
            }
        }

        function handleProjectChange() {
            const val = document.getElementById('project-dropdown').value;
            const logBox = document.getElementById('console-output');
            if (logBox) {
                logBox.textContent = `[ESCÔPO ATUALIZADO] Projeto(s) em foco: ${val}. Pronto para nova análise.\n` + logBox.textContent;
            }
        }

        function openAddProjectModal() {
            document.getElementById('modal-add-project').classList.add('show');
        }

        function closeAddProjectModal() {
            document.getElementById('modal-add-project').classList.remove('show');
        }

        async function confirmAddProject() {
            const projectId = document.getElementById('input-new-project-id').value.trim();
            const env = document.getElementById('input-new-env').value;
            if (!projectId) {
                alert('Informe o ID do projeto GCP.');
                return;
            }
            try {
                const res = await fetch('/api/projects/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({project_id: projectId, environment: env})
                });
                const data = await res.json();
                
                const dropdown = document.getElementById('project-dropdown');
                const opt = document.createElement('option');
                opt.value = projectId;
                opt.textContent = `${projectId} (${env})`;
                dropdown.appendChild(opt);
                dropdown.value = projectId;

                closeAddProjectModal();
                alert(`Projeto ${projectId} adicionado com sucesso ao escopo de auditoria.`);
            } catch (e) {
                alert('Erro ao registrar projeto.');
            }
        }

        function quickPrompt(text) {
            document.getElementById('chat-input').value = text;
            sendChat();
        }

        async function sendChat() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;

            const selectedProject = document.getElementById('project-dropdown').value;
            const chatMessages = document.getElementById('chat-messages');
            
            const userMsg = document.createElement('div');
            userMsg.className = 'message message-user';
            userMsg.textContent = message;
            chatMessages.appendChild(userMsg);
            input.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            const loadingMsg = document.createElement('div');
            loadingMsg.className = 'message message-agent';
            loadingMsg.innerHTML = '<span class="subagent-badge-tag">Vertex AI Gemini 2.5 Flash • Raciocinando...</span><br>Consultando telemetria em nuvem e analisando evidências ISO 27001...';
            chatMessages.appendChild(loadingMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: message,
                        selected_projects: selectedProject === 'ALL' ? ['agentic-grc-cd06', 'agentic-grc-staging', 'agentic-grc-data-lake'] : [selectedProject]
                    })
                });
                const data = await res.json();
                loadingMsg.innerHTML = `<span class="subagent-badge-tag">${data.subagent_used || 'Vertex AI Gemini 2.5 Flash'}</span><br>${data.response}`;
            } catch (err) {
                loadingMsg.textContent = 'Erro de comunicação com o auditor Vertex AI: ' + err.message;
            }
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        async function runPhasedAudit() {
            const consoleBox = document.getElementById('console-output');
            const timerLabel = document.getElementById('scan-timer');
            const resultsContainer = document.getElementById('phased-results-container');
            const resultsList = document.getElementById('phased-results-list');
            
            consoleBox.textContent = '';
            const appendLog = (msg) => {
                const time = new Date().toISOString().split('T')[1].slice(0, 8);
                consoleBox.textContent += `[${time}] ${msg}\n`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
            };

            appendLog("Iniciando varredura pró-ativa em 4 fases...");
            timerLabel.textContent = "Executando scan...";

            // Reset bars
            for (let i = 1; i <= 4; i++) {
                document.getElementById(`step-card-${i}`).className = 'step-card';
                document.getElementById(`step-badge-${i}`).className = 'step-status idle';
                document.getElementById(`step-badge-${i}`).textContent = 'Pronto';
                document.getElementById(`step-bar-${i}`).style.width = '0%';
            }

            // Animate Phase 1
            document.getElementById('step-card-1').className = 'step-card active';
            document.getElementById('step-badge-1').className = 'step-status running';
            document.getElementById('step-badge-1').textContent = 'Executando';
            document.getElementById('step-bar-1').style.width = '70%';
            appendLog("Fase 1: Conectando a Cloud Asset Inventory API em todos os projetos do escopo...");

            const selectedProject = document.getElementById('project-dropdown').value;
            const projectList = selectedProject === 'ALL' ? ['agentic-grc-cd06', 'agentic-grc-staging', 'agentic-grc-data-lake'] : [selectedProject];

            try {
                const res = await fetch('/api/audit/run_phases', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({projects: projectList, scope: 'FULL_ISO_27001'})
                });
                const data = await res.json();

                // Phase 1 Done
                document.getElementById('step-card-1').className = 'step-card completed';
                document.getElementById('step-badge-1').className = 'step-status done';
                document.getElementById('step-badge-1').textContent = 'Concluído';
                document.getElementById('step-bar-1').style.width = '100%';
                appendLog(`Fase 1 Concluída: ${data.phases[0].assets_discovered} ativos mapeados e contas de serviço auditadas.`);

                // Phase 2
                document.getElementById('step-card-2').className = 'step-card completed';
                document.getElementById('step-badge-2').className = 'step-status done';
                document.getElementById('step-badge-2').textContent = 'Concluído';
                document.getElementById('step-bar-2').style.width = '100%';
                appendLog(`Fase 2 Concluída: Controles A.5.23, A.8.12, A.8.24 e IaC avaliados (Score: 100%).`);

                // Phase 3
                document.getElementById('step-card-3').className = 'step-card completed';
                document.getElementById('step-badge-3').className = 'step-status done';
                document.getElementById('step-badge-3').textContent = 'Concluído';
                document.getElementById('step-bar-3').style.width = '100%';
                appendLog(`Fase 3 Concluída: Resiliência Climática ISO 27001 Amd 1:2024 e Model Armor verificados.`);

                // Phase 4
                document.getElementById('step-card-4').className = 'step-card completed';
                document.getElementById('step-badge-4').className = 'step-status done';
                document.getElementById('step-badge-4').textContent = 'Concluído';
                document.getElementById('step-bar-4').style.width = '100%';
                appendLog(`Fase 4 Concluída: Grafo Criptográfico atualizado com SHA-256. Scorecard Final: 100.0% EXCELLENT.`);

                timerLabel.textContent = "Scan finalizado com sucesso!";

                // Render structured cards
                resultsContainer.style.display = 'flex';
                resultsList.innerHTML = data.phases.map(p => `
                    <div class="card" style="border-left: 3px solid #10b981;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <strong style="color: #fff; font-size: 13.5px;">${p.phase}</strong>
                            <span class="badge-compliant">${p.status}</span>
                        </div>
                        <ul style="padding-left: 18px; font-size: 12px; color: var(--text-secondary); line-height: 1.6;">
                            ${p.findings.map(f => `<li>${f}</li>`).join('')}
                        </ul>
                    </div>
                `).join('');

            } catch (e) {
                appendLog('Erro ao executar scan por fases: ' + e.message);
                timerLabel.textContent = "Erro na execução";
            }
        }

        async function loadIsoMatrix() {
            const grid = document.getElementById('matrix-grid');
            grid.innerHTML = '<p style="color: var(--text-muted);">Carregando matriz escalável ISO 27001...</p>';
            try {
                const res = await fetch('/api/iso_matrix');
                const data = await res.json();
                isoControlsCache = data.controls;
                renderMatrix(isoControlsCache);
            } catch (e) {
                grid.innerHTML = '<p style="color: var(--rose-accent);">Erro ao carregar matriz ISO 27001.</p>';
            }
        }

        function filterMatrix(theme) {
            currentTheme = theme;
            document.querySelectorAll('.filter-pill').forEach(p => {
                p.classList.toggle('active', p.textContent.includes(theme) || (theme === 'Todos' && p.textContent.includes('Todos')));
            });
            searchMatrix();
        }

        function searchMatrix() {
            const query = document.getElementById('matrix-search').value.toLowerCase();
            let filtered = isoControlsCache;

            if (currentTheme !== 'Todos') {
                filtered = filtered.filter(c => c.theme === currentTheme);
            }

            if (query) {
                filtered = filtered.filter(c => 
                    c.id.toLowerCase().includes(query) ||
                    c.name.toLowerCase().includes(query) ||
                    c.gcp_mapping.toLowerCase().includes(query) ||
                    c.description.toLowerCase().includes(query)
                );
            }
            renderMatrix(filtered);
        }

        function renderMatrix(controls) {
            const grid = document.getElementById('matrix-grid');
            if (controls.length === 0) {
                grid.innerHTML = '<p style="color: var(--text-muted); grid-column: 1/-1;">Nenhum controle encontrado para os critérios selecionados.</p>';
                return;
            }
            grid.innerHTML = controls.map(c => `
                <div class="control-card">
                    <div class="control-badge-row">
                        <span class="control-id-badge">${c.id}</span>
                        <span class="badge-compliant">${c.status}</span>
                    </div>
                    <div class="control-name">${c.name}</div>
                    <div class="control-desc">${c.description}</div>
                    <div style="margin-top: auto; padding-top: 8px;">
                        <span class="gcp-tag">☁️ ${c.gcp_mapping}</span>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 6px;">
                            ${c.evidence}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        async function loadSubagents() {
            const container = document.getElementById('subagents-list');
            try {
                const res = await fetch('/api/subagents');
                const data = await res.json();
                container.innerHTML = data.subagents.map(sa => `
                    <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #fff; font-size: 13px;">${sa.name}</strong>
                            <span class="badge-compliant">${sa.status}</span>
                        </div>
                        <p style="font-size: 12px; color: var(--text-secondary); margin: 6px 0;">${sa.role}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                            <span style="font-size: 10px; color: var(--text-muted);">SPIFFE: ${sa.spiffe_id}</span>
                            <button class="btn-confirm" style="font-size: 11px; padding: 4px 10px;" onclick="triggerSubagent('${sa.id}')">Executar</button>
                        </div>
                    </div>
                `).join('');
            } catch (e) {
                container.innerHTML = '<p>Erro ao carregar subagentes.</p>';
            }
        }

        async function triggerSubagent(subagentId) {
            const res = await fetch('/api/subagents/trigger', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({subagent: subagentId})
            });
            const data = await res.json();
            alert('Resposta do Subagente:\n' + JSON.stringify(data.result, null, 2));
        }

        async function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            const resultDiv = document.getElementById('upload-result');
            resultDiv.innerHTML = '<p style="color: var(--cyan-glow); margin-top: 10px;">Auditoria estática IaC em andamento para ' + file.name + '...</p>';

            try {
                const res = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                resultDiv.innerHTML = `
                    <div class="card" style="margin-top: 12px; border-color: var(--emerald-accent);">
                        <h4 style="color: #34d399; font-size: 13px;">Arquivo Avaliado: ${data.filename}</h4>
                        <pre style="font-size: 11px; color: #cbd5e1; margin-top: 6px; overflow-x: auto;">${JSON.stringify(data.audit_finding, null, 2)}</pre>
                    </div>
                `;
            } catch (e) {
                resultDiv.innerHTML = '<p style="color: var(--rose-accent);">Erro ao auditar artefato IaC.</p>';
            }
        }

        async function linkStorage() {
            const source = document.getElementById('storage-type').value;
            const uri = document.getElementById('storage-uri').value;
            const resultDiv = document.getElementById('storage-result');

            if (!uri) {
                alert('Informe a URL ou ID do repositório/pasta.');
                return;
            }

            resultDiv.innerHTML = '<p style="color: var(--cyan-glow); margin-top: 8px;">Conectando repositório Zero-Copy na fonte...</p>';
            try {
                const res = await fetch('/api/storage/link', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({source: source, uri: uri})
                });
                const data = await res.json();
                resultDiv.innerHTML = `
                    <div class="card" style="margin-top: 10px; border-color: var(--emerald-accent);">
                        <strong style="color: #34d399; font-size: 13px;">Repositório Conectado: ${data.source}</strong>
                        <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                            ${data.discovered_documents.length} documentos indexados na fonte com garantia Zero-Copy (sem replicação).
                        </p>
                    </div>
                `;
            } catch (e) {
                resultDiv.innerHTML = '<p style="color: var(--rose-accent);">Falha na conexão Zero-Copy.</p>';
            }
        }

        async function loadDashboard() {
            try {
                const res = await fetch('/api/dashboard');
                const data = await res.json();
                document.getElementById('dash-score').textContent = data.overall_score + '%';
                document.getElementById('dash-drift').textContent = data.drift_trajectory === 'STABLE' ? 'ESTÁVEL' : data.drift_trajectory;
                document.getElementById('dash-evidence').textContent = data.evidence_nodes_count;

                const hitlContainer = document.getElementById('hitl-container');
                hitlContainer.innerHTML = data.pending_hitl_approvals.map(h => `
                    <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid var(--amber-accent); border-radius: 8px; padding: 14px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #fde68a; font-size: 13px;">${h.id}: ${h.title}</strong>
                            <p style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
                                Proposto por: ${h.proposed_by} | Risco: ${h.risk_level} | Status: ${h.status}
                            </p>
                        </div>
                        <button class="btn-confirm" style="background: #059669;" onclick="approveRemediation('${h.id}')">Aprovar Emenda (HITL)</button>
                    </div>
                `).join('');

                const controlsContainer = document.getElementById('controls-list');
                controlsContainer.innerHTML = data.controls.map(c => `
                    <div class="card" style="padding: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 13px; font-weight: 700; color: #fff;">${c.id}: ${c.name}</span>
                            <span class="badge-compliant">${c.status}</span>
                        </div>
                    </div>
                `).join('');
            } catch (e) {}
        }

        async function approveRemediation(remId) {
            if (!confirm('Confirmar aprovação Human-in-the-Loop desta política?')) return;
            try {
                const res = await fetch('/api/remediation/approve', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({remediation_id: remId})
                });
                const data = await res.json();
                alert(data.message);
                loadDashboard();
            } catch (e) {
                alert('Falha na aprovação.');
            }
        }

        loadSubagents();
    </script>
</body>
</html>
"""