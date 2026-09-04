"""Official Google Cloud Security PSO - Agentic GRC Auditor Web Portal."""

PORTAL_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Cloud Security PSO - Agentic GRC Auditor</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <!-- Marked.js for Executive Markdown Rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg-canvas: #131314;
            --bg-sidebar: #1e1f20;
            --bg-surface: #282a2c;
            --bg-surface-hover: #333538;
            --bg-input: #1e1f20;
            --border-subtle: #2d2f31;
            --border-focus: #444746;
            --text-primary: #e3e3e3;
            --text-secondary: #9ea3a8;
            --text-tertiary: #5e6266;
            --gcp-blue: #8ab4f8;
            --gcp-blue-dark: #1a73e8;
            --gcp-green: #81c995;
            --gcp-yellow: #fdd663;
            --gcp-red: #f28b82;
            --gcp-purple: #c58af9;
            --sidebar-width: 290px;
            --sidebar-collapsed-width: 68px;
            --font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --transition-smooth: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: var(--font-family);
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            overflow: hidden;
        }

        .icon-svg {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            stroke-width: 1.8;
        }

        /* ------------------------------------------------------------------ */
        /* Left Sidebar */
        /* ------------------------------------------------------------------ */
        .sidebar {
            width: var(--sidebar-width);
            background-color: var(--bg-sidebar);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            border-right: 1px solid var(--border-subtle);
            transition: var(--transition-smooth);
            z-index: 50;
            height: 100vh;
            overflow: hidden;
            position: relative;
        }

        .sidebar.collapsed { width: var(--sidebar-collapsed-width); }

        .sidebar-top {
            padding: 16px 14px 8px 14px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
        }

        .sidebar-top::-webkit-scrollbar { width: 4px; }
        .sidebar-top::-webkit-scrollbar-thumb { background: var(--border-subtle); border-radius: 4px; }

        /* Brand Header */
        .brand-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 4px;
        }

        .brand-left {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
        }

        .gcp-pso-logo-icon {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .brand-text-col {
            display: flex;
            flex-direction: column;
            gap: 1px;
            overflow: hidden;
        }

        .brand-title {
            font-size: 15.5px;
            font-weight: 600;
            letter-spacing: -0.2px;
            color: #ffffff;
            white-space: nowrap;
        }

        .brand-subtitle-badge {
            font-size: 10px;
            font-weight: 600;
            color: var(--gcp-blue);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .btn-collapse {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 6px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition-smooth);
        }
        .btn-collapse:hover { background: var(--bg-surface); color: var(--text-primary); }

        /* Nav Actions */
        .nav-actions { display: flex; flex-direction: column; gap: 4px; }

        .nav-action-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 9px 12px;
            border-radius: 10px;
            color: var(--text-secondary);
            font-size: 13.5px;
            cursor: pointer;
            transition: var(--transition-smooth);
            text-decoration: none;
            border: none;
            background: transparent;
            width: 100%;
            text-align: left;
        }

        .nav-action-item:hover { background-color: var(--bg-surface); color: var(--text-primary); }
        .nav-action-item.active { background-color: var(--bg-surface-hover); color: var(--gcp-blue); font-weight: 500; }

        .sidebar.collapsed .label,
        .sidebar.collapsed .brand-text-col,
        .sidebar.collapsed .section-header,
        .sidebar.collapsed .agent-pin,
        .sidebar.collapsed .recent-list,
        .sidebar.collapsed .scope-box,
        .sidebar.collapsed .user-meta { display: none !important; }

        .sidebar.collapsed .nav-action-item,
        .sidebar.collapsed .agent-item { justify-content: center; padding: 12px; }

        /* Section Header */
        .section-header {
            font-size: 11.5px;
            font-weight: 600;
            color: var(--text-tertiary);
            padding: 8px 12px 4px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .agent-list { display: flex; flex-direction: column; gap: 2px; }

        .agent-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 12px;
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 13.5px;
            cursor: pointer;
            transition: var(--transition-smooth);
            border: none;
            background: transparent;
            width: 100%;
            text-align: left;
        }
        .agent-item:hover { background-color: var(--bg-surface); }
        .agent-item.active { background-color: var(--bg-surface-hover); color: var(--gcp-blue); font-weight: 500; }

        .agent-left-wrap { display: flex; align-items: center; gap: 10px; min-width: 0; }

        .agent-avatar {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-surface);
            color: var(--text-primary);
            flex-shrink: 0;
            border: 1px solid var(--border-subtle);
        }

        .agent-item.active .agent-avatar {
            background: rgba(138, 180, 248, 0.15);
            color: var(--gcp-blue);
            border-color: var(--gcp-blue);
        }

        .agent-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .agent-pin { color: var(--text-tertiary); opacity: 0.6; transition: var(--transition-smooth); }
        .agent-item:hover .agent-pin { opacity: 1; color: var(--text-secondary); }

        .recent-list { display: flex; flex-direction: column; gap: 2px; padding-left: 2px; }
        .recent-item {
            padding: 7px 12px;
            font-size: 13px;
            color: var(--text-secondary);
            border-radius: 8px;
            cursor: pointer;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transition: var(--transition-smooth);
        }
        .recent-item:hover { background-color: var(--bg-surface); color: var(--text-primary); }

        /* ------------------------------------------------------------------ */
        /* Bottom Left: Scope Box & Profile */
        /* ------------------------------------------------------------------ */
        .sidebar-bottom {
            padding: 12px 14px 16px 14px;
            border-top: 1px solid var(--border-subtle);
            background: var(--bg-sidebar);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .scope-box {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .scope-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-add-scope {
            background: transparent;
            border: none;
            color: var(--gcp-blue);
            cursor: pointer;
            font-size: 11px;
            display: flex;
            align-items: gap;
            padding: 2px 4px;
            border-radius: 4px;
        }
        .btn-add-scope:hover { background: rgba(138, 180, 248, 0.15); }

        .scope-projects-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            max-height: 110px;
            overflow-y: auto;
        }
        .scope-projects-list::-webkit-scrollbar { width: 3px; }
        .scope-projects-list::-webkit-scrollbar-thumb { background: var(--border-focus); border-radius: 3px; }

        .project-pill-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--bg-canvas);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 5px 8px;
            font-size: 12px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .project-pill-item:hover { border-color: var(--border-focus); }
        .project-pill-left { display: flex; align-items: center; gap: 6px; overflow: hidden; }
        .project-checkbox { accent-color: var(--gcp-blue); cursor: pointer; }
        .project-id-text {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: var(--text-primary);
            font-family: var(--font-mono);
            font-size: 11.5px;
        }

        .env-badge {
            font-size: 9px;
            font-weight: 700;
            padding: 1px 4px;
            border-radius: 4px;
            background: rgba(129, 201, 149, 0.15);
            color: var(--gcp-green);
        }

        .user-profile-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 4px 2px 0 2px;
            cursor: pointer;
        }

        .user-left { display: flex; align-items: center; gap: 10px; overflow: hidden; }
        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1a73e8, #4285f4);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .user-meta { display: flex; flex-direction: column; overflow: hidden; }
        .user-name {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .user-plan { font-size: 10.5px; color: var(--gcp-blue); font-weight: 500; }

        .btn-settings {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 6px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition-smooth);
        }
        .btn-settings:hover { background: var(--bg-surface); color: var(--text-primary); }

        /* ------------------------------------------------------------------ */
        /* Main Container */
        /* ------------------------------------------------------------------ */
        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
            background-color: var(--bg-canvas);
            position: relative;
        }

        /* Top Navbar */
        .top-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 24px;
            border-bottom: 1px solid var(--border-subtle);
            background: rgba(19, 19, 20, 0.85);
            backdrop-filter: blur(12px);
            z-index: 40;
        }

        .nav-breadcrumb { display: flex; align-items: center; gap: 8px; font-size: 13.5px; }
        .top-org-badge { display: flex; align-items: center; gap: 6px; color: var(--text-secondary); }
        .top-active-agent { font-weight: 600; color: var(--text-primary); }
        .top-right-actions { display: flex; align-items: center; gap: 12px; }

        .top-status-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--gcp-green);
            background: rgba(129, 201, 149, 0.1);
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid rgba(129, 201, 149, 0.2);
        }
        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--gcp-green);
            box-shadow: 0 0 8px var(--gcp-green);
        }

        .dropdown { position: relative; display: inline-block; }
        .btn-action-primary {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition-smooth);
        }
        .btn-action-primary:hover { background: var(--bg-surface-hover); border-color: var(--border-focus); }

        .dropdown-menu {
            display: none;
            position: absolute;
            right: 0;
            top: 110%;
            background: var(--bg-sidebar);
            border: 1px solid var(--border-focus);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            min-width: 250px;
            z-index: 100;
            overflow: hidden;
            padding: 6px 0;
        }
        .dropdown.show .dropdown-menu { display: block; }
        .dropdown-item {
            padding: 10px 16px;
            font-size: 13px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: var(--transition-smooth);
            text-decoration: none;
        }
        .dropdown-item:hover { background: var(--bg-surface); color: var(--gcp-blue); }

        /* Viewport */
        .views-viewport {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
        }

        .view-pane {
            display: none;
            flex-direction: column;
            height: 100%;
            padding: 24px 32px;
            animation: fadeIn 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .view-pane.active { display: flex; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ------------------------------------------------------------------ */
        /* View 1: Chatbot Auditor */
        /* ------------------------------------------------------------------ */
        .chat-view-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            max-width: 920px;
            margin: 0 auto;
            width: 100%;
            position: relative;
        }

        .chat-messages-area {
            flex: 1;
            overflow-y: auto;
            padding: 16px 0 120px 0;
            display: flex;
            flex-direction: column;
            gap: 28px;
        }

        .chat-messages-area::-webkit-scrollbar { width: 6px; }
        .chat-messages-area::-webkit-scrollbar-thumb { background: var(--border-subtle); border-radius: 6px; }

        .gemini-hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin: auto 0;
            padding: 30px 20px;
            gap: 16px;
        }

        .hero-avatar {
            width: 68px;
            height: 68px;
            border-radius: 50%;
            background: radial-gradient(circle, #25282c 0%, #1e1f20 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border-focus);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }

        .hero-title { font-size: 32px; font-weight: 600; letter-spacing: -0.5px; color: #ffffff; }
        .hero-badge-pso {
            font-size: 12px;
            font-weight: 600;
            color: var(--gcp-blue);
            text-transform: uppercase;
            letter-spacing: 1px;
            background: rgba(138, 180, 248, 0.1);
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(138, 180, 248, 0.25);
        }

        .hero-subtitle { font-size: 14.5px; color: var(--text-secondary); max-width: 620px; line-height: 1.6; }
        .hero-suggestions-stack { display: flex; flex-direction: column; gap: 10px; width: 100%; max-width: 620px; margin-top: 12px; }
        .hero-suggestion-card {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 13px 18px;
            text-align: left;
            font-size: 13.5px;
            color: var(--text-primary);
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .hero-suggestion-card:hover { background: var(--bg-surface); border-color: var(--gcp-blue); transform: translateX(4px); }

        .msg-row { display: flex; gap: 16px; width: 100%; animation: fadeIn 0.25s ease; }
        .msg-row.user { justify-content: flex-end; }
        .msg-avatar { width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
        .msg-avatar.gemini { background: radial-gradient(circle, #25282c 0%, #1e1f20 100%); border: 1px solid var(--border-subtle); }
        .msg-avatar.user-av { background: var(--gcp-blue); color: #131314; font-weight: 700; font-size: 12px; }

        .msg-content { max-width: 86%; line-height: 1.7; font-size: 14.5px; color: var(--text-primary); }
        .msg-row.user .msg-content { background: var(--bg-surface); padding: 12px 18px; border-radius: 18px 18px 4px 18px; border: 1px solid var(--border-subtle); }
        .msg-row.bot .msg-content { padding: 4px 0; }

        .msg-content h1 { font-size: 20px; font-weight: 600; color: #ffffff; margin: 22px 0 10px 0; padding-bottom: 6px; border-bottom: 1px solid var(--border-subtle); }
        .msg-content h2 { font-size: 17px; font-weight: 600; color: var(--gcp-blue); margin: 18px 0 8px 0; }
        .msg-content h3 { font-size: 15px; font-weight: 600; color: #ffffff; margin: 14px 0 6px 0; }
        .msg-content p { margin-bottom: 12px; color: #d1d5db; }
        .msg-content ul, .msg-content ol { margin: 10px 0 14px 22px; }
        .msg-content li { margin-bottom: 6px; color: #e5e7eb; }
        .msg-content blockquote {
            border-left: 4px solid var(--gcp-blue);
            background: rgba(138, 180, 248, 0.08);
            padding: 12px 18px;
            border-radius: 0 10px 10px 0;
            margin: 14px 0;
            font-size: 14px;
            color: var(--text-primary);
        }
        .msg-content hr { border: none; border-top: 1px solid var(--border-subtle); margin: 20px 0; }
        .msg-content strong { color: #ffffff; font-weight: 600; }
        .msg-content code { background: #282a2c; color: var(--gcp-blue); padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono); font-size: 12.5px; }
        .msg-content pre { background: #0d0e0f; border: 1px solid var(--border-subtle); border-radius: 10px; padding: 14px; overflow-x: auto; margin: 14px 0; }
        .msg-content pre code { background: transparent; padding: 0; color: #f3f4f6; }

        .msg-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            font-size: 13.5px;
            border: 1px solid var(--border-focus);
            border-radius: 8px;
            overflow: hidden;
        }
        .msg-content th {
            background-color: #202224;
            color: var(--gcp-blue);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 12px;
            padding: 10px 14px;
            border: 1px solid var(--border-subtle);
            text-align: left;
        }
        .msg-content td { padding: 10px 14px; border: 1px solid var(--border-subtle); color: #e5e7eb; vertical-align: top; line-height: 1.5; }
        .msg-content tr:nth-child(even) td { background-color: rgba(255, 255, 255, 0.02); }
        .msg-content tr:hover td { background-color: rgba(138, 180, 248, 0.05); }

        .chat-input-wrapper {
            position: absolute;
            bottom: 20px;
            left: 0;
            right: 0;
            max-width: 920px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 30;
            padding: 0 12px;
        }
        .chat-input-box {
            background: var(--bg-input);
            border: 1px solid var(--border-subtle);
            border-radius: 28px;
            padding: 8px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
            transition: var(--transition-smooth);
        }
        .chat-input-box:focus-within { border-color: var(--border-focus); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 0 1px var(--border-focus); }
        .btn-input-icon {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition-smooth);
            flex-shrink: 0;
        }
        .btn-input-icon:hover { background: var(--bg-surface); color: var(--text-primary); }
        .chat-textarea {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-primary);
            font-size: 14.5px;
            outline: none;
            resize: none;
            height: 24px;
            max-height: 120px;
            padding: 2px 4px;
            line-height: 20px;
        }
        .chat-textarea::placeholder { color: var(--text-tertiary); }
        .btn-send {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--bg-surface);
            border: none;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition-smooth);
            flex-shrink: 0;
        }
        .btn-send.active { background: var(--gcp-blue); color: #131314; }
        .chat-disclaimer { font-size: 11px; color: var(--text-tertiary); text-align: center; }

        /* ------------------------------------------------------------------ */
        /* View 2: Scan por Fases */
        /* ------------------------------------------------------------------ */
        .section-header-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-subtle);
        }
        .view-title-group h2 { font-size: 22px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
        .view-title-group p { font-size: 13.5px; color: var(--text-secondary); }

        .phases-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .phase-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            transition: var(--transition-smooth);
        }
        .phase-card.active { border-color: var(--gcp-blue); background: rgba(138, 180, 248, 0.05); }
        .phase-badge-row { display: flex; align-items: center; justify-content: space-between; }
        .phase-step-num { font-size: 11px; font-weight: 700; color: var(--gcp-blue); text-transform: uppercase; }
        .phase-status-tag { font-size: 11px; padding: 2px 6px; border-radius: 4px; background: var(--bg-canvas); color: var(--text-secondary); }
        .phase-status-tag.completed { background: rgba(129, 201, 149, 0.15); color: var(--gcp-green); }
        .phase-name { font-size: 15px; font-weight: 500; color: var(--text-primary); }
        .phase-desc { font-size: 12px; color: var(--text-secondary); line-height: 1.4; }
        .phase-progress-bar { height: 4px; background: var(--bg-canvas); border-radius: 4px; overflow: hidden; margin-top: auto; }
        .phase-progress-fill { height: 100%; background: var(--gcp-blue); width: 0%; transition: width 0.4s ease; }

        .audit-console-panel {
            flex: 1;
            background: #0d0e0f;
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            font-family: var(--font-mono);
            font-size: 12.5px;
            min-height: 240px;
            overflow: hidden;
        }
        .console-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 12px;
            margin-bottom: 12px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            font-size: 12px;
        }
        .console-logs { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; line-height: 1.5; }
        .log-entry { display: flex; gap: 12px; }
        .log-ts { color: var(--text-tertiary); flex-shrink: 0; }
        .log-msg { color: var(--text-primary); }
        .log-msg.success { color: var(--gcp-green); }
        .log-msg.info { color: var(--gcp-blue); }

        /* ------------------------------------------------------------------ */
        /* View 3: Matriz ISO 27001 Escalável (With Themes Summary & Rich Drawer) */
        /* ------------------------------------------------------------------ */
        .themes-summary-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }

        .theme-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 14px;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .theme-card:hover, .theme-card.active {
            border-color: var(--gcp-blue);
            background: rgba(138, 180, 248, 0.05);
            transform: translateY(-2px);
        }

        .theme-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .theme-card-title {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .theme-count-badge {
            font-size: 11px;
            font-weight: 700;
            font-family: var(--font-mono);
            color: var(--gcp-blue);
            background: rgba(138, 180, 248, 0.15);
            padding: 2px 7px;
            border-radius: 10px;
        }

        .theme-card-scope {
            font-size: 11.5px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .matrix-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }

        .matrix-filter-pills { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .btn-filter-pill {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12.5px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-filter-pill:hover, .btn-filter-pill.active {
            background: var(--bg-surface-hover);
            color: var(--text-primary);
            border-color: var(--gcp-blue);
        }

        .search-box-wrap { position: relative; min-width: 280px; }
        .search-input {
            width: 100%;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 7px 14px 7px 34px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
            transition: var(--transition-smooth);
        }
        .search-input:focus { border-color: var(--border-focus); }
        .search-icon-pos { position: absolute; left: 11px; top: 50%; transform: translateY(-50%); color: var(--text-tertiary); pointer-events: none; }

        .table-container {
            flex: 1;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            overflow: auto;
        }

        .data-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
        .data-table th {
            position: sticky;
            top: 0;
            background: #202224;
            padding: 12px 16px;
            font-weight: 500;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border-subtle);
            z-index: 10;
        }
        .data-table td { padding: 12px 16px; border-bottom: 1px solid var(--border-subtle); color: var(--text-primary); vertical-align: middle; }
        .data-table tr.ctrl-main-row { cursor: pointer; transition: var(--transition-smooth); }
        .data-table tr.ctrl-main-row:hover td { background: var(--bg-surface-hover); }

        .ctrl-id-badge {
            font-family: var(--font-mono);
            font-size: 11.5px;
            color: var(--gcp-blue);
            background: rgba(138, 180, 248, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }

        .status-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; display: inline-block; }
        .status-badge.compliant { background: rgba(129, 201, 149, 0.15); color: var(--gcp-green); }

        .btn-expand-ctrl {
            background: transparent;
            border: 1px solid var(--border-subtle);
            color: var(--gcp-blue);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11.5px;
            display: flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-expand-ctrl:hover { background: rgba(138, 180, 248, 0.15); }

        /* Expandable Details Drawer */
        .ctrl-detail-row { display: none; }
        .ctrl-detail-row.open { display: table-row; }

        .ctrl-detail-container {
            background: #191b1d;
            padding: 20px 24px;
            border-left: 3px solid var(--gcp-blue);
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .ctrl-detail-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .detail-box {
            background: var(--bg-canvas);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .detail-box-title {
            font-size: 12px;
            font-weight: 700;
            color: var(--gcp-blue);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .detail-box-content {
            font-size: 13px;
            color: #d1d5db;
            line-height: 1.6;
            white-space: pre-line;
        }

        .tag-pill {
            font-size: 10.5px;
            background: var(--bg-surface);
            color: var(--text-secondary);
            padding: 2px 7px;
            border-radius: 6px;
            border: 1px solid var(--border-subtle);
            display: inline-block;
            margin: 2px 3px 2px 0;
        }

        /* ------------------------------------------------------------------ */
        
        /* Phase Action Buttons & Findings */
        .phase-actions-row {
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }
        .btn-phase-exec {
            flex: 1;
            background: rgba(138, 180, 248, 0.15);
            color: var(--gcp-blue);
            border: 1px solid rgba(138, 180, 248, 0.3);
            padding: 6px 8px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }
        .btn-phase-exec:hover {
            background: var(--gcp-blue);
            color: #fff;
        }
        .btn-phase-treat {
            flex: 1;
            background: rgba(234, 67, 53, 0.12);
            color: #f28b82;
            border: 1px solid rgba(234, 67, 53, 0.25);
            padding: 6px 8px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }
        .btn-phase-treat:hover {
            background: rgba(234, 67, 53, 0.22);
            border-color: var(--gcp-red);
        }
        .phase-findings-box {
            margin-top: 10px;
            padding: 8px 10px;
            background: var(--bg-canvas);
            border-radius: 6px;
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.4;
            border-left: 3px solid var(--gcp-blue);
            max-height: 80px;
            overflow-y: auto;
        }

        /* Custom Subagents Section */
        .subagent-section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 24px 0 14px 0;
        }
        .subagent-section-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .badge-custom {
            background: rgba(138, 180, 248, 0.15);
            color: var(--gcp-blue);
            font-size: 10.5px;
            padding: 2px 7px;
            border-radius: 10px;
            border: 1px solid rgba(138, 180, 248, 0.3);
        }
        .subagent-prompt-preview {
            font-size: 11px;
            color: var(--text-tertiary);
            background: var(--bg-canvas);
            padding: 8px 10px;
            border-radius: 6px;
            line-height: 1.4;
            max-height: 52px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
        .subagent-card-actions {
            display: flex;
            gap: 8px;
            margin-top: auto;
        }
        .btn-subagent-run {
            flex: 1;
            background: var(--gcp-blue);
            color: #fff;
            border: none;
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-subagent-run:hover { background: var(--gcp-blue-hover); }
        .btn-subagent-delete {
            background: rgba(234, 67, 53, 0.15);
            color: #f28b82;
            border: 1px solid rgba(234, 67, 53, 0.3);
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-subagent-delete:hover { background: rgba(234, 67, 53, 0.3); }

        /* Form styling for Modals */
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
            margin-bottom: 12px;
        }
        .form-label {
            font-size: 12px;
            font-weight: 500;
            color: var(--text-secondary);
        }
        .form-control {
            background: var(--bg-canvas);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 12px;
            color: var(--text-primary);
            font-size: 12.5px;
            outline: none;
            width: 100%;
            transition: var(--transition-smooth);
        }
        .form-control:focus { border-color: var(--border-focus); }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .tools-checkbox-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            background: var(--bg-canvas);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
        }
        .tool-checkbox-label {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--text-secondary);
            cursor: pointer;
        }

        /* View 4: Subagentes & Zero-Copy */
        /* ------------------------------------------------------------------ */
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
        .card-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: var(--transition-smooth);
        }
        .card-panel:hover { border-color: var(--border-focus); }
        .card-panel-header { display: flex; align-items: center; gap: 12px; }
        .card-icon-avatar {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: var(--bg-canvas);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--gcp-blue);
            border: 1px solid var(--border-subtle);
        }
        .card-title { font-size: 15px; font-weight: 500; color: var(--text-primary); }
        .card-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }

        /* ------------------------------------------------------------------ */
        /* View 5: Scorecard */
        /* ------------------------------------------------------------------ */
        .scorecard-stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .stat-val { font-size: 36px; font-weight: 700; color: var(--text-primary); font-family: var(--font-mono); }
        .stat-label { font-size: 13px; color: var(--text-secondary); }

        /* ------------------------------------------------------------------ */
        /* View 6: Relatório Executivo PSO */
        /* ------------------------------------------------------------------ */
        .report-preview-sheet {
            background: #ffffff;
            color: #1f2937;
            border-radius: 12px;
            padding: 48px;
            max-width: 960px;
            margin: 0 auto;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            line-height: 1.6;
        }
        .report-header-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid #1a73e8;
            padding-bottom: 20px;
            margin-bottom: 24px;
        }
        .report-brand-pso { display: flex; align-items: center; gap: 16px; }
        .report-title-meta h1 { font-size: 22px; font-weight: 700; color: #111827; margin-bottom: 4px; }
        .report-title-meta .pso-subtitle { font-size: 12px; font-weight: 600; color: #1a73e8; text-transform: uppercase; letter-spacing: 0.8px; }
        .report-meta-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
            font-size: 13px;
        }
        .report-meta-item { display: flex; flex-direction: column; }
        .report-meta-label { font-size: 11px; text-transform: uppercase; color: #6b7280; font-weight: 600; }
        .report-meta-value { font-weight: 600; color: #111827; }
        .report-score-box {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 8px;
            padding: 18px 24px;
            margin-bottom: 28px;
        }
        .report-score-num { font-size: 38px; font-weight: 700; color: #065f46; font-family: var(--font-mono); }
        .report-score-label { font-size: 15px; font-weight: 600; color: #065f46; }
        .report-section-title { font-size: 16px; font-weight: 700; color: #111827; margin: 24px 0 12px 0; padding-bottom: 6px; border-bottom: 1px solid #e5e7eb; }
        .report-table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-bottom: 24px; }
        .report-table th { background: #f3f4f6; color: #374151; font-weight: 600; padding: 10px 12px; border: 1px solid #e5e7eb; text-align: left; }
        .report-table td { padding: 10px 12px; border: 1px solid #e5e7eb; color: #1f2937; }
        .report-signature-block {
            margin-top: 40px;
            padding-top: 24px;
            border-top: 2px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            font-size: 12px;
        }
        .sig-seal { border: 2px dashed #1a73e8; padding: 12px 18px; border-radius: 8px; color: #1a73e8; font-weight: 600; text-align: center; }

        /* Modals */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-overlay.active { display: flex; }
        .modal-window {
            background: var(--bg-sidebar);
            border: 1px solid var(--border-focus);
            border-radius: 16px;
            width: 100%;
            max-width: 480px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 18px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
        }
        .modal-header { display: flex; align-items: center; justify-content: space-between; }
        .modal-title { font-size: 18px; font-weight: 600; color: var(--text-primary); }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        .form-label { font-size: 12.5px; color: var(--text-secondary); }
        .form-input {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 10px 12px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
        }
        .form-input:focus { border-color: var(--gcp-blue); }
        .modal-actions { display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-top: 8px; }
        .btn-cancel { background: transparent; border: 1px solid var(--border-subtle); color: var(--text-secondary); padding: 8px 16px; border-radius: 8px; cursor: pointer; }
        .btn-confirm { background: var(--gcp-blue); border: none; color: #131314; font-weight: 600; padding: 8px 18px; border-radius: 8px; cursor: pointer; }

        @media print {
            body { background: #ffffff !important; color: #000000 !important; overflow: visible !important; }
            .sidebar, .top-navbar, .chat-input-wrapper, .modal-overlay, .matrix-toolbar, .btn-confirm, .btn-action-primary { display: none !important; }
            .main-container { height: auto !important; }
            .views-viewport { overflow: visible !important; }
            .view-pane { display: none !important; }
            #view-report-exec { display: block !important; padding: 0 !important; }
            .report-preview-sheet { box-shadow: none !important; border-radius: 0 !important; max-width: 100% !important; padding: 0 !important; }
        }
    </style>
</head>
<body>

    <!-- Left Sidebar -->
    <aside class="sidebar" id="appSidebar">
        <div class="sidebar-top">
            <!-- Brand Header: Google Cloud Security PSO & Agentic GRC Auditor -->
            <div class="brand-header">
                <a href="#" class="brand-left" onclick="switchView('view-chat')">
                    <div class="gcp-pso-logo-icon">
                        <svg viewBox="0 0 32 32" width="30" height="30" fill="none">
                            <path d="M16 3L28 8.5V17.5C28 23.5 22.8 28.5 16 30C9.2 28.5 4 23.5 4 17.5V8.5L16 3Z" fill="#1a73e8" fill-opacity="0.2" stroke="#8ab4f8" stroke-width="2"/>
                            <path d="M16 7L24 10.8V17C24 21.2 20.6 24.8 16 26C11.4 24.8 8 21.2 8 17V10.8L16 7Z" fill="url(#pso-shield-grad)"/>
                            <path d="M14 17L19 12" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                            <path d="M12 15L14 17" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                            <defs>
                                <linearGradient id="pso-shield-grad" x1="8" y1="7" x2="24" y2="26">
                                    <stop stop-color="#4285F4"/>
                                    <stop offset="0.5" stop-color="#1A73E8"/>
                                    <stop offset="1" stop-color="#34A853"/>
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                    <div class="brand-text-col">
                        <span class="brand-title">Agentic GRC Auditor</span>
                        <span class="brand-subtitle-badge">Google Cloud Security PSO</span>
                    </div>
                </a>
                <button class="btn-collapse" onclick="toggleSidebar()" title="Recolher menu lateral">
                    <svg class="icon-svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <line x1="9" y1="3" x2="9" y2="21"/>
                    </svg>
                </button>
            </div>

            <!-- Primary Nav Actions -->
            <div class="nav-actions">
                <button class="nav-action-item active" id="navNewChat" onclick="startNewConversation()">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                    </span>
                    <span class="label">Nova conversa</span>
                </button>
                <button class="nav-action-item" onclick="openExecutiveReport()">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                            <line x1="16" y1="13" x2="8" y2="13"/>
                            <line x1="16" y1="17" x2="8" y2="17"/>
                        </svg>
                    </span>
                    <span class="label">Dossiê Executivo PSO</span>
                </button>
                <button class="nav-action-item" onclick="switchView('view-scorecard')">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/>
                            <path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>
                        </svg>
                    </span>
                    <span class="label">Caixa de entrada</span>
                </button>
                <button class="nav-action-item" onclick="switchView('view-matrix')">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <circle cx="11" cy="11" r="8"/>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                        </svg>
                    </span>
                    <span class="label">Pesquisar controles</span>
                </button>
                <button class="nav-action-item" onclick="switchView('view-connectors')">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                        </svg>
                    </span>
                    <span class="label">Habilidades PSO</span>
                </button>
            </div>

            <!-- Specialized Sub-Agents Group -->
            <div class="section-header">
                <span>Agentes Especializados</span>
                <span class="icon-svg">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                        <polyline points="9 18 15 12 9 6"/>
                    </svg>
                </span>
            </div>
            <div class="agent-list">
                <button class="agent-item active" id="agentBtnChat" onclick="switchView('view-chat')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                            </svg>
                        </div>
                        <span class="agent-name">Chatbot Auditor</span>
                    </div>
                    <span class="agent-pin">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor">
                            <line x1="12" y1="17" x2="12" y2="22"/>
                            <path d="M5 17h14l-2-6V4h1V2H6v2h1v7l-2 6z"/>
                        </svg>
                    </span>
                </button>

                <button class="agent-item" id="agentBtnPhases" onclick="switchView('view-phases')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                            </svg>
                        </div>
                        <span class="agent-name">Scan por Fases</span>
                    </div>
                    <span class="agent-pin">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor">
                            <line x1="12" y1="17" x2="12" y2="22"/>
                            <path d="M5 17h14l-2-6V4h1V2H6v2h1v7l-2 6z"/>
                        </svg>
                    </span>
                </button>

                <button class="agent-item" id="agentBtnMatrix" onclick="switchView('view-matrix')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                            </svg>
                        </div>
                        <span class="agent-name">Matriz ISO 27001 Escalável</span>
                    </div>
                    <span class="agent-pin">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor">
                            <line x1="12" y1="17" x2="12" y2="22"/>
                            <path d="M5 17h14l-2-6V4h1V2H6v2h1v7l-2 6z"/>
                        </svg>
                    </span>
                </button>

                <button class="agent-item" id="agentBtnConnectors" onclick="switchView('view-connectors')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <circle cx="18" cy="5" r="3"/>
                                <circle cx="6" cy="12" r="3"/>
                                <circle cx="18" cy="19" r="3"/>
                                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
                            </svg>
                        </div>
                        <span class="agent-name">Subagentes & Zero-Copy</span>
                    </div>
                    <span class="agent-pin">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor">
                            <line x1="12" y1="17" x2="12" y2="22"/>
                            <path d="M5 17h14l-2-6V4h1V2H6v2h1v7l-2 6z"/>
                        </svg>
                    </span>
                </button>

                <button class="agent-item" id="agentBtnScorecard" onclick="switchView('view-scorecard')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                            </svg>
                        </div>
                        <span class="agent-name">Scorecard & Grafo de Evidências</span>
                    </div>
                    <span class="agent-pin">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor">
                            <line x1="12" y1="17" x2="12" y2="22"/>
                            <path d="M5 17h14l-2-6V4h1V2H6v2h1v7l-2 6z"/>
                        </svg>
                    </span>
                </button>
            </div>

            <!-- Recentes -->
            <div class="section-header" style="margin-top: 8px;">
                <span>Histórico de Auditorias</span>
            </div>
            <div class="recent-list">
                <div class="recent-item" onclick="promptPreFill('Gerar parecer executivo formal de conformidade para agentic-grc-cd06')">Parecer ISO 27001 - agentic-grc-cd06</div>
                <div class="recent-item" onclick="promptPreFill('Executar auditoria técnica em 4 fases no ambiente multi-projeto')">Scan Fases 1 a 4 - Staging & Prod</div>
                <div class="recent-item" onclick="promptPreFill('Avaliar conformidade dos 93 controles da ISO/IEC 27001:2022')">Auditoria 93 Controles</div>
            </div>
        </div>

        <!-- Bottom Left: Escopo de Projetos & Perfil PSO -->
        <div class="sidebar-bottom">
            <div class="scope-box" id="scopeContainer">
                <div class="scope-header">
                    <span>Escopo de Projetos</span>
                    <button class="btn-add-scope" onclick="openProjectModal()">
                        <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5">
                            <line x1="12" y1="5" x2="12" y2="19"/>
                            <line x1="5" y1="12" x2="19" y2="12"/>
                        </svg>
                        Adicionar
                    </button>
                </div>
                <div class="scope-projects-list" id="scopeProjectsList">
                    <!-- Dynamic project list -->
                </div>
            </div>

            <div class="user-profile-row">
                <div class="user-left">
                    <div class="user-avatar">JS</div>
                    <div class="user-meta">
                        <span class="user-name">Joabson Saccomani</span>
                        <span class="user-plan">Google Cloud Security PSO</span>
                    </div>
                </div>
                <button class="btn-settings" title="Configurações">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="3"/>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                    </svg>
                </button>
            </div>
        </div>
    </aside>

    <!-- Main Container -->
    <main class="main-container">
        <!-- Top Navbar -->
        <header class="top-navbar">
            <div class="nav-breadcrumb">
                <span class="top-org-badge">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none">
                        <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="#8ab4f8"/>
                    </svg>
                    <span>Gemini Enterprise Agent Platform</span>
                </span>
                <span style="color: var(--text-tertiary)">/</span>
                <span class="top-active-agent" id="topActiveTitle">Chatbot Auditor</span>
                <span style="color: var(--text-tertiary)">•</span>
                <span style="color: var(--gcp-blue); font-size: 13px;" id="topProjectCountBadge">1 projeto ativo</span>
            </div>

            <div class="top-right-actions">
                <div class="top-status-indicator">
                    <span class="status-dot"></span>
                    <span>Vertex AI gemini-2.5-flash (PSO Certified)</span>
                </div>

                <div class="dropdown" id="exportDropdown">
                    <button class="btn-action-primary" onclick="toggleExportMenu()">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                        Exportar Relatório PSO
                    </button>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="javascript:void(0)" onclick="openExecutiveReport()">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <line x1="16" y1="13" x2="8" y2="13"/>
                                <line x1="16" y1="17" x2="8" y2="17"/>
                            </svg>
                            Visualizar Dossiê Executivo PSO
                        </a>
                        <a class="dropdown-item" href="javascript:void(0)" onclick="printExecutiveReport()">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <polyline points="6 9 6 2 18 2 18 9"/>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                                <rect x="6" y="14" width="12" height="8"/>
                            </svg>
                            Imprimir / Salvar PDF Oficial
                        </a>
                        <a class="dropdown-item" href="/api/reports/export?format=json" target="_blank">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                            </svg>
                            Pacote Criptográfico JSON (SHA-256)
                        </a>
                        <a class="dropdown-item" href="/api/reports/export?format=markdown" target="_blank">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <line x1="16" y1="13" x2="8" y2="13"/>
                                <line x1="16" y1="17" x2="8" y2="17"/>
                            </svg>
                            Relatório Técnico Markdown
                        </a>
                    </div>
                </div>
            </div>
        </header>

        <!-- Dynamic Views Viewport -->
        <div class="views-viewport">

            <!-- View 1: Chatbot Auditor -->
            <section class="view-pane active" id="view-chat">
                <div class="chat-view-container">
                    <div class="chat-messages-area" id="chatArea">
                        <div class="gemini-hero" id="geminiHero">
                            <div class="hero-avatar">
                                <svg viewBox="0 0 36 36" width="36" height="36" fill="none">
                                    <path d="M18 4L30 9.5V19.5C30 26.5 24.8 31.8 18 33.5C11.2 31.8 6 26.5 6 19.5V9.5L18 4Z" fill="url(#hero-shield-grad)"/>
                                    <path d="M15.5 20L21 14.5" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
                                    <path d="M13.5 18L15.5 20" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
                                    <defs>
                                        <linearGradient id="hero-shield-grad" x1="6" y1="4" x2="30" y2="33.5">
                                            <stop stop-color="#4285F4"/>
                                            <stop offset="0.5" stop-color="#1A73E8"/>
                                            <stop offset="1" stop-color="#34A853"/>
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <span class="hero-badge-pso">Google Cloud Security PSO</span>
                            <h1 class="hero-title">Agentic GRC Auditor</h1>
                            <p class="hero-subtitle">
                                Auditoria contínua autônoma, governança e certificação para <strong>ISO/IEC 27001:2022</strong> (93 Controles do Anexo A) integrada à telemetria real do Google Cloud e Grafo de Evidências imutável.
                            </p>

                            <div class="hero-suggestions-stack">
                                <div class="hero-suggestion-card" onclick="promptPreFill('Gerar Parecer Executivo de Conformidade para a ISO/IEC 27001:2022 nos projetos no escopo')">
                                    <span>Gerar Parecer Executivo de Conformidade para a ISO/IEC 27001:2022 nos projetos no escopo</span>
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                        <polyline points="9 18 15 12 9 6"/>
                                    </svg>
                                </div>
                                <div class="hero-suggestion-card" onclick="promptPreFill('Executar Auditoria Técnica Completa em 4 Fases e selar o Grafo de Evidências')">
                                    <span>Executar Auditoria Técnica Completa em 4 Fases e selar o Grafo de Evidências</span>
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                        <polyline points="9 18 15 12 9 6"/>
                                    </svg>
                                </div>
                                <div class="hero-suggestion-card" onclick="promptPreFill('Auditar controles de Criptografia Cloud KMS (A.8.24) e Prevenção de Fuga de Dados DLP (A.8.12)')">
                                    <span>Auditar controles de Criptografia Cloud KMS (A.8.24) e Prevenção de Fuga de Dados DLP (A.8.12)</span>
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                        <polyline points="9 18 15 12 9 6"/>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="chat-input-wrapper">
                        <div class="chat-input-box">
                            <button class="btn-input-icon" onclick="openUploadModal()" title="Anexar arquivo de infraestrutura / IaC">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                                    <line x1="12" y1="5" x2="12" y2="19"/>
                                    <line x1="5" y1="12" x2="19" y2="12"/>
                                </svg>
                            </button>
                            <button class="btn-input-icon" onclick="openStorageModal()" title="Conectar repositório Zero-Copy (Drive/SharePoint)">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                                </svg>
                            </button>
                            <textarea id="chatInput" class="chat-textarea" placeholder="Consulte o Agentic GRC Auditor (Google Cloud Security PSO)..." rows="1" onkeydown="handleChatKey(event)" oninput="handleChatInput(this)"></textarea>
                            <button id="sendBtn" class="btn-send" onclick="sendChatMessage()" title="Enviar mensagem">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5">
                                    <line x1="12" y1="19" x2="12" y2="5"/>
                                    <polyline points="5 12 12 5 19 12"/>
                                </svg>
                            </button>
                        </div>
                        <div class="chat-disclaimer">
                            Google Cloud Security PSO • As evidências e pareceres de conformidade são validados no Grafo Criptográfico SHA-256 e protegidos por Model Armor.
                        </div>
                    </div>
                </div>
            </section>

            <!-- View 2: Scan por Fases -->
            <section class="view-pane" id="view-phases">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Scan de Auditoria por Fases (Google Cloud PSO)</h2>
                        <p>Pipeline estruturado de 4 fases para auditoria técnica, governança de dados e ancoragem criptográfica.</p>
                    </div>
                    <button class="btn-confirm" onclick="triggerPhasedAudit()">
                        Executar Scan nas 4 Fases
                    </button>
                </div>

                <div class="phases-grid">
                    <div class="phase-card" id="cardPhase1">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 1</span>
                            <span class="phase-status-tag" id="statusPhase1">Pronto</span>
                        </div>
                        <div class="phase-name">Descoberta & IAM</div>
                        <div class="phase-desc">Cloud Asset Inventory, service accounts e privilégio mínimo (A.5.2, A.5.15, A.8.2).</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase1"></div></div>
                        <div class="phase-actions-row">
                            <button class="btn-phase-exec" onclick="runSinglePhase(1)">
                                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                                Executar Fase 1
                            </button>
                            <button class="btn-phase-treat" onclick="openRemediationModal(1)">Tratar Desvios</button>
                        </div>
                        <div class="phase-findings-box" id="findingsPhase1" style="display:none;"></div>
                    </div>

                    <div class="phase-card" id="cardPhase2">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 2</span>
                            <span class="phase-status-tag" id="statusPhase2">Pronto</span>
                        </div>
                        <div class="phase-name">Auditoria Técnica & IaC</div>
                        <div class="phase-desc">Scan de templates Terraform, portas abertas, VPC Service Controls e Cloud KMS (A.8.9, A.8.24).</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase2"></div></div>
                        <div class="phase-actions-row">
                            <button class="btn-phase-exec" onclick="runSinglePhase(2)">
                                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                                Executar Fase 2
                            </button>
                            <button class="btn-phase-treat" onclick="openRemediationModal(2)">Tratar Desvios</button>
                        </div>
                        <div class="phase-findings-box" id="findingsPhase2" style="display:none;"></div>
                    </div>

                    <div class="phase-card" id="cardPhase3">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 3</span>
                            <span class="phase-status-tag" id="statusPhase3">Pronto</span>
                        </div>
                        <div class="phase-name">Governança & Políticas</div>
                        <div class="phase-desc">Auditoria de Organization Policies e políticas corporativas do SGSI (A.5).</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase3"></div></div>
                        <div class="phase-actions-row">
                            <button class="btn-phase-exec" onclick="runSinglePhase(3)">
                                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                                Executar Fase 3
                            </button>
                            <button class="btn-phase-treat" onclick="openRemediationModal(3)">Tratar Desvios</button>
                        </div>
                        <div class="phase-findings-box" id="findingsPhase3" style="display:none;"></div>
                    </div>

                    <div class="phase-card" id="cardPhase4">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 4</span>
                            <span class="phase-status-tag" id="statusPhase4">Pronto</span>
                        </div>
                        <div class="phase-name">Grafo & Assinatura</div>
                        <div class="phase-desc">Consolidação e ancoragem de evidências com hashes SHA-256 no grafo imutável.</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase4"></div></div>
                        <div class="phase-actions-row">
                            <button class="btn-phase-exec" onclick="runSinglePhase(4)">
                                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                                Executar Fase 4
                            </button>
                            <button class="btn-phase-treat" onclick="openRemediationModal(4)">Tratar Desvios</button>
                        </div>
                        <div class="phase-findings-box" id="findingsPhase4" style="display:none;"></div>
                    </div>
                </div>

                <div class="audit-console-panel">
                    <div class="console-header">
                        <span>Terminal de Auditoria em Tempo Real</span>
                        <span id="auditExecId">Exec ID: Standby</span>
                    </div>
                    <div class="console-logs" id="auditLogsContainer">
                        <div class="log-entry">
                            <span class="log-ts">--:--:--</span>
                            <span class="log-msg">Motor de auditoria PSO pronto para inicialização das 4 fases nos projetos selecionados.</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- View 3: Matriz ISO 27001 Escalável (With Themes Summary & Rich Drawer) -->
            <section class="view-pane" id="view-matrix">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Matriz de Controles ISO/IEC 27001:2022 & Declaração de Aplicabilidade (SoA)</h2>
                        <p>Catálogo consolidado de 93 controles do Anexo A estruturado rigorosamente nos 4 temas da ISO/IEC 27001:2022 com taxonomia de 5 atributos.</p>
                    </div>
                </div>

                <!-- Resumo dos 4 Temas Principais da ISO/IEC 27001:2022 -->
                <div class="themes-summary-grid" id="themesSummaryGrid">
                    <div class="theme-card active" onclick="filterMatrixByTheme('Todos')">
                        <div class="theme-card-top">
                            <span class="theme-card-title">Todos os Controles</span>
                            <span class="theme-count-badge">93</span>
                        </div>
                        <div class="theme-card-scope">Visão consolidada dos 93 controles do Anexo A para a Declaração de Aplicabilidade (SoA).</div>
                    </div>
                    <div class="theme-card" onclick="filterMatrixByTheme('A.5 Organizacional')">
                        <div class="theme-card-top">
                            <span class="theme-card-title">A.5 Organizacionais</span>
                            <span class="theme-count-badge">37</span>
                        </div>
                        <div class="theme-card-scope">Políticas, governança, fornecedores, gestão de ativos e resposta a incidentes.</div>
                    </div>
                    <div class="theme-card" onclick="filterMatrixByTheme('A.6 Pessoas')">
                        <div class="theme-card-top">
                            <span class="theme-card-title">A.6 Pessoas</span>
                            <span class="theme-count-badge">8</span>
                        </div>
                        <div class="theme-card-scope">Segurança em RH, triagem, termos de contratação, conscientização e desligamento.</div>
                    </div>
                    <div class="theme-card" onclick="filterMatrixByTheme('A.7 Físico')">
                        <div class="theme-card-top">
                            <span class="theme-card-title">A.7 Físicos</span>
                            <span class="theme-count-badge">14</span>
                        </div>
                        <div class="theme-card-scope">Perímetros de segurança, instalações, proteção contra ameaças e descarte seguro.</div>
                    </div>
                    <div class="theme-card" onclick="filterMatrixByTheme('A.8 Tecnológico')">
                        <div class="theme-card-top">
                            <span class="theme-card-title">A.8 Tecnológicos</span>
                            <span class="theme-count-badge">34</span>
                        </div>
                        <div class="theme-card-scope">Autenticação, criptografia, redes, desenvolvimento seguro (DevSecOps) e logs.</div>
                    </div>
                </div>

                <div class="matrix-toolbar">
                    <div class="matrix-filter-pills" id="matrixFilterPills">
                        <button class="btn-filter-pill active" onclick="filterMatrixByTheme('Todos')">Todos</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.5 Organizacional')">A.5 Organizacional</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.6 Pessoas')">A.6 Pessoas</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.7 Físico')">A.7 Físico</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.8 Tecnológico')">A.8 Tecnológico</button>
                    </div>

                    <div class="search-box-wrap">
                        <span class="search-icon-pos">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <circle cx="11" cy="11" r="8"/>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                            </svg>
                        </span>
                        <input type="text" id="matrixSearchInput" class="search-input" placeholder="Buscar por controle, serviço GCP ou comando..." oninput="searchMatrix(this.value)">
                    </div>
                </div>

                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="width: 90px;">Código</th>
                                <th style="width: 200px;">Nome do Controle</th>
                                <th style="width: 140px;">Tema</th>
                                <th>Mapeamento GCP</th>
                                <th style="width: 110px;">Status</th>
                                <th style="width: 90px;">Severidade</th>
                                <th style="width: 150px; text-align: center;">Ações</th>
                            </tr>
                        </thead>
                        <tbody id="matrixTableBody">
                            <!-- Populated via JS -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- View 4: Subagentes & Zero-Copy -->
            <section class="view-pane" id="view-connectors">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Subagentes Especializados & Conectores Zero-Copy</h2>
                        <p>Crie, customize e execute subagentes com instruções especializadas e integre repositórios sem replicação de dados.</p>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn-confirm" onclick="openCreateSubagentModal()" style="background: var(--gcp-blue);">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align: middle; margin-right: 4px;">
                                <line x1="12" y1="5" x2="12" y2="19"/>
                                <line x1="5" y1="12" x2="19" y2="12"/>
                            </svg>
                            Criar Novo Subagente
                        </button>
                        <button class="btn-confirm" onclick="openStorageModal()">Conectar Repositório</button>
                    </div>
                </div>

                <div class="subagent-section-header">
                    <span class="subagent-section-title">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                            <line x1="8" y1="21" x2="16" y2="21"/>
                            <line x1="12" y1="17" x2="12" y2="21"/>
                        </svg>
                        Subagentes Customizados pelo Usuário
                    </span>
                    <span style="font-size: 12px; color: var(--text-tertiary)" id="customCountDisplay">Carregando...</span>
                </div>
                <div class="cards-grid" id="customSubagentsGrid" style="margin-bottom: 24px;">
                    <!-- Preenchido dinamicamente via API -->
                </div>

                <div class="subagent-section-header">
                    <span class="subagent-section-title">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        </svg>
                        Subagentes Nativos (Google Cloud Security PSO)
                    </span>
                </div>
                <div class="cards-grid">
                    <div class="card-panel">
                        <div class="card-panel-header">
                            <div class="card-icon-avatar">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                </svg>
                            </div>
                            <div>
                                <div class="card-title">Annex A Auditor Agent</div>
                                <div style="font-size: 11px; color: var(--gcp-green)">Online</div>
                            </div>
                        </div>
                        <div class="card-desc">Inspeciona controles do Anexo A (A.5 a A.8) contra telemetria em tempo real do Cloud Asset Inventory.</div>
                        <button class="btn-action-primary" onclick="triggerSubagent('annex_a', 'kms')" style="margin-top: auto;">Auditar Anexo A</button>
                    </div>

                    <div class="card-panel">
                        <div class="card-panel-header">
                            <div class="card-icon-avatar">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
                                    <circle cx="12" cy="12" r="10"/>
                                    <line x1="2" y1="12" x2="22" y2="12"/>
                                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                                </svg>
                            </div>
                            <div>
                                <div class="card-title">Horizon Scanner Agent</div>
                                <div style="font-size: 11px; color: var(--gcp-green)">Online</div>
                            </div>
                        </div>
                        <div class="card-desc">Monitora atualizações normativas globais, novas ameaças e propõe melhorias contínuas para o SGSI.</div>
                        <button class="btn-action-primary" onclick="triggerSubagent('horizon_scanner', 'regulatory_updates')" style="margin-top: auto;">Executar Horizon Scan</button>
                    </div>

                    <div class="card-panel">
                        <div class="card-panel-header">
                            <div class="card-icon-avatar">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
                                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                                    <line x1="9" y1="3" x2="9" y2="21"/>
                                </svg>
                            </div>
                            <div>
                                <div class="card-title">Google Drive (Zero-Copy)</div>
                                <div style="font-size: 11px; color: var(--gcp-green)">Conectado</div>
                            </div>
                        </div>
                        <div class="card-desc">Auditoria contínua de políticas corporativas armazenadas no Google Workspace via delegação SPIFFE.</div>
                        <button class="btn-action-primary" onclick="openStorageModal()" style="margin-top: auto;">Sincronizar Políticas</button>
                    </div>

                    <div class="card-panel">
                        <div class="card-panel-header">
                            <div class="card-icon-avatar">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
                                    <polygon points="12 2 2 7 12 12 22 7 12 2"/>
                                    <polyline points="2 17 12 22 22 17"/>
                                    <polyline points="2 12 12 17 22 12"/>
                                </svg>
                            </div>
                            <div>
                                <div class="card-title">IaC Scanner (Terraform/Ansible)</div>
                                <div style="font-size: 11px; color: var(--gcp-green)">Online</div>
                            </div>
                        </div>
                        <div class="card-desc">Varredura estática de templates de infraestrutura como código para validação prévia de conformidade.</div>
                        <button class="btn-action-primary" onclick="openUploadModal()" style="margin-top: auto;">Analisar Template IaC</button>
                    </div>
                </div>
            </section>

            <!-- View 5: Scorecard -->
            <section class="view-pane" id="view-scorecard">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Scorecard Contínuo & Grafo de Evidências</h2>
                        <p>Métricas consolidadas de conformidade, drift de segurança e aprovações humanas pendentes.</p>
                    </div>
                </div>

                <div class="scorecard-stats-row">
                    <div class="stat-card">
                        <div class="stat-label">Conformidade Global</div>
                        <div class="stat-val" style="color: var(--gcp-green);" id="scoreDisplay">100.0%</div>
                        <div style="font-size: 12px; color: var(--text-secondary)">Opinião do Auditor: LIMPA / EXCELLENT</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Nós no Grafo de Evidências</div>
                        <div class="stat-val" id="evidenceNodesDisplay">24</div>
                        <div style="font-size: 12px; color: var(--gcp-green)">Assinatura Criptográfica: SHA-256</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Proteção de Borda IA</div>
                        <div class="stat-val" style="color: var(--gcp-blue);">Ativo</div>
                        <div style="font-size: 12px; color: var(--text-secondary)">Model Armor (Anti-Jailbreak / DLP)</div>
                    </div>
                </div>

                <div class="card-panel" style="margin-top: 16px;">
                    <div class="card-title">Aprovações Humanas Pendentes (Human-in-the-Loop)</div>
                    <div class="card-desc">
                        Atualização Semestral de Política de Controle de Acesso IAM (A.5.15) proposta pelo subagente de Governança.
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 12px;">
                        <button class="btn-confirm" onclick="approveRemediation('HITL-AMENDMENT-001')">
                            Aprovar Aditamento à Política
                        </button>
                    </div>
                </div>
            </section>

            <!-- View 6: Relatório Executivo PSO -->
            <section class="view-pane" id="view-report-exec" style="background: var(--bg-canvas); overflow-y: auto;">
                <div class="report-preview-sheet">
                    <div class="report-header-banner">
                        <div class="report-brand-pso">
                            <svg viewBox="0 0 32 32" width="40" height="40" fill="none">
                                <path d="M16 3L28 8.5V17.5C28 23.5 22.8 28.5 16 30C9.2 28.5 4 23.5 4 17.5V8.5L16 3Z" fill="#1a73e8" fill-opacity="0.15" stroke="#1a73e8" stroke-width="2"/>
                                <path d="M16 7L24 10.8V17C24 21.2 20.6 24.8 16 26C11.4 24.8 8 21.2 8 17V10.8L16 7Z" fill="#1a73e8"/>
                                <path d="M14 17L19 12" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                                <path d="M12 15L14 17" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                            <div class="report-title-meta">
                                <h1>Google Cloud Security PSO</h1>
                                <div class="pso-subtitle">Professional Services Organization • Cybersecurity & Regulatory Practice</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: #e0e7ff; color: #3730a3; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 4px; text-transform: uppercase;">
                                Confidencial / Parecer Formal
                            </span>
                        </div>
                    </div>

                    <div class="report-meta-grid">
                        <div class="report-meta-item">
                            <span class="report-meta-label">Título do Documento</span>
                            <span class="report-meta-value">Dossiê Executivo de Auditoria & Conformidade Contínua</span>
                        </div>
                        <div class="report-meta-item">
                            <span class="report-meta-label">ID de Registro PSO</span>
                            <span class="report-meta-value" id="docReportId">PSO-GRC-ISO27001-2026-FINAL</span>
                        </div>
                        <div class="report-meta-item">
                            <span class="report-meta-label">Norma & Emendas</span>
                            <span class="report-meta-value">ABNT NBR ISO/IEC 27001:2022 (Anexo A - 93 Controles)</span>
                        </div>
                        <div class="report-meta-item">
                            <span class="report-meta-label">Auditor Líder Responsável</span>
                            <span class="report-meta-value">Agentic GRC Auditor (GEAP Cognitive Autonomous Lead)</span>
                        </div>
                        <div class="report-meta-item">
                            <span class="report-meta-label">Projetos GCP no Escopo</span>
                            <span class="report-meta-value" id="docProjectsAudited">agentic-grc-cd06</span>
                        </div>
                        <div class="report-meta-item">
                            <span class="report-meta-label">Integridade da Evidência</span>
                            <span class="report-meta-value" style="font-family: var(--font-mono); color: #059669;">SHA-256 Merkle Root Sealed</span>
                        </div>
                    </div>

                    <div class="report-score-box">
                        <div>
                            <div class="report-score-label">Opinião do Auditor PSO: LIMPA E SEM RESSALVAS</div>
                            <div style="font-size: 13px; color: #047857;">Ambiente com 100% dos controles auditados em estrita conformidade. Trajetória de drift estável.</div>
                        </div>
                        <div class="report-score-num">100.0%</div>
                    </div>

                    <div class="report-section-title">1. Parecer Executivo de Auditoria</div>
                    <p style="font-size: 13.5px; color: #374151; margin-bottom: 16px;">
                        A prática de <strong>Google Cloud Security PSO (Professional Services Organization)</strong> realizou a auditoria autônoma de segurança e conformidade da informação sobre as instâncias do Google Cloud Platform indicadas no escopo. A avaliação contemplou integralmente os 93 controles normativos do Anexo A da ISO/IEC 27001:2022 consolidados nos 4 temas principais (Organizacional, Pessoas, Físico e Tecnológico).
                    </p>

                    <div class="report-section-title">2. Resultados do Pipeline de Auditoria em 4 Fases</div>
                    <table class="report-table">
                        <thead>
                            <tr>
                                <th>Fase</th>
                                <th>Escopo & Metodologia</th>
                                <th>Status</th>
                                <th>Achados Principais</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Fase 1</strong></td>
                                <td>Descoberta de Ativos & IAM</td>
                                <td><span style="color: #059669; font-weight: 600;">CONFORME</span></td>
                                <td>Mapeamento via Cloud Asset Inventory API. Contas de serviço sem permissões excessivas. Menor privilégio garantido.</td>
                            </tr>
                            <tr>
                                <td><strong>Fase 2</strong></td>
                                <td>Auditoria Técnica & IaC</td>
                                <td><span style="color: #059669; font-weight: 600;">CONFORME</span></td>
                                <td>GCS com PAP e UBLA obrigatórios. Perímetro VPC-SC para Storage e BigQuery. Chaves Cloud KMS HSM com rotação &le; 90d.</td>
                            </tr>
                            <tr>
                                <td><strong>Fase 3</strong></td>
                                <td>Governança & Ação Climática</td>
                                <td><span style="color: #059669; font-weight: 600;">CONFORME</span></td>
                                <td>Controles Organizacionais A.5 com 100% de conformidade, políticas ativas e enforce de Organization Policies.</td>
                            </tr>
                            <tr>
                                <td><strong>Fase 4</strong></td>
                                <td>Síntese & Selamento</td>
                                <td><span style="color: #059669; font-weight: 600;">SELADO</span></td>
                                <td>Cadeia de evidências selada criptograficamente com hashes SHA-256 no Grafo Imutável.</td>
                            </tr>
                        </tbody>
                    </table>

                    <div class="report-section-title">3. Atestação Formal & Assinatura Digital</div>
                    <div class="report-signature-block">
                        <div>
                            <div style="font-weight: 700; color: #111827;">Google Cloud Security PSO</div>
                            <div style="color: #6b7280;">Cybersecurity & Regulatory Advisory Practice</div>
                            <div style="color: #6b7280; font-size: 11px;">Gemini Enterprise Agent Platform (GEAP)</div>
                        </div>
                        <div class="sig-seal">
                            <span>CERTIFICADO DIGITALMENTE</span><br>
                            <span style="font-family: var(--font-mono); font-size: 10px;">SHA256: e3b0c44298fc1c149afbf4c8</span>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    </main>

    <!-- Modal: Adicionar Projeto ao Escopo -->
    <div class="modal-overlay" id="projectModal">
        <div class="modal-window">
            <div class="modal-header">
                <div class="modal-title">Adicionar Projeto GCP ao Escopo</div>
                <button class="btn-collapse" onclick="closeProjectModal()">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
            <div class="form-group">
                <label class="form-label">ID do Projeto no Google Cloud</label>
                <input type="text" id="modalProjectId" class="form-input" placeholder="ex.: agentic-grc-prod">
            </div>
            <div class="form-group">
                <label class="form-label">Ambiente</label>
                <input type="text" id="modalEnvironment" class="form-input" placeholder="ex.: PRODUCTION ou STAGING">
            </div>
            <div class="form-group">
                <label class="form-label">Região Primária</label>
                <input type="text" id="modalRegion" class="form-input" placeholder="ex.: us-central1" value="us-central1">
            </div>
            <div class="modal-actions">
                <button class="btn-cancel" onclick="closeProjectModal()">Cancelar</button>
                <button class="btn-confirm" onclick="submitAddProject()">Registrar Projeto</button>
            </div>
        </div>
    </div>

    <!-- Modal: Conectar Zero-Copy Storage -->
    <div class="modal-overlay" id="storageModal">
        <div class="modal-window">
            <div class="modal-header">
                <div class="modal-title">Conectar Repositório Zero-Copy</div>
                <button class="btn-collapse" onclick="closeStorageModal()">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
            <div class="form-group">
                <label class="form-label">Fonte de Documentos</label>
                <select id="storageSourceSelect" class="form-input">
                    <option value="google_drive">Google Drive (Workspace Enterprise)</option>
                    <option value="sharepoint">Microsoft SharePoint Online</option>
                    <option value="jira">Atlassian Jira Software</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">URI da Pasta / Espaço</label>
                <input type="text" id="storageUri" class="form-input" placeholder="ex.: drive://security-policies" value="drive://iso27001-sgsi">
            </div>
            <div class="modal-actions">
                <button class="btn-cancel" onclick="closeStorageModal()">Cancelar</button>
                <button class="btn-confirm" onclick="submitStorageLink()">Conectar Sem Copiar Dados</button>
            </div>
        </div>
    </div>

    <!-- Modal: Upload IaC Template -->
    <div class="modal-overlay" id="uploadModal">
        <div class="modal-window">
            <div class="modal-header">
                <div class="modal-title">Analisar Template de Infraestrutura (IaC)</div>
                <button class="btn-collapse" onclick="closeUploadModal()">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
            <div class="form-group">
                <label class="form-label">Selecione o arquivo Terraform (.tf) ou Ansible (.yml)</label>
                <input type="file" id="iacFileInput" class="form-input" accept=".tf,.yml,.yaml,.json">
            </div>
            <div class="modal-actions">
                <button class="btn-cancel" onclick="closeUploadModal()">Cancelar</button>
                <button class="btn-confirm" onclick="submitIacUpload()">Executar Varredura</button>
            </div>
        </div>
    </div>

    <script>
        // State
        let activeProjects = [];
        let selectedProjectIds = new Set();
        let currentThemeFilter = "Todos";
        let matrixControls = [];

        // Configure Marked.js if loaded
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                gfm: true,
                breaks: true,
                tables: true
            });
        }

        // Initialization
        
        // -------------------------------------------------------------------
        // Individual Phase Execution & Remediation
        // -------------------------------------------------------------------
        async function runSinglePhase(phaseNum) {
            const projects = Array.from(selectedProjectIds);
            const card = document.getElementById(`cardPhase${phaseNum}`);
            const statusTag = document.getElementById(`statusPhase${phaseNum}`);
            const fill = document.getElementById(`fillPhase${phaseNum}`);
            const findingsBox = document.getElementById(`findingsPhase${phaseNum}`);

            statusTag.innerText = "Executando...";
            statusTag.className = "phase-status-tag running";
            fill.style.width = "40%";
            appendLog(`[Fase ${phaseNum} Execução Individual] Iniciando auditoria para projetos: ${projects.join(', ')}...`);

            try {
                const res = await fetch("/api/audit/run_phases", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ projects: projects, phase: phaseNum })
                });
                const data = await res.json();
                fill.style.width = "100%";
                statusTag.innerText = "Concluído (100%)";
                statusTag.className = "phase-status-tag compliant";

                if (data.phases && data.phases.length > 0) {
                    const p = data.phases[0];
                    appendLog(`[Fase ${phaseNum} Concluída] Status: ${p.status}`, "success");
                    if (p.findings) {
                        p.findings.forEach(f => appendLog(`  -> ${f}`));
                        if (findingsBox) {
                            findingsBox.style.display = "block";
                            findingsBox.innerHTML = `<strong>Achados da Fase ${phaseNum}:</strong><br>` + p.findings.map(f => `• ${escapeHtml(f)}`).join("<br>");
                        }
                    }
                }
            } catch (e) {
                statusTag.innerText = "Erro";
                statusTag.className = "phase-status-tag failed";
                appendLog(`[Fase ${phaseNum} Erro] ${e}`, "error");
            }
        }

        function openRemediationModal(phaseNum) {
            document.getElementById("remPhaseNumber").value = phaseNum;
            document.getElementById("remModalTitle").innerText = `Tratar Desvios da Fase ${phaseNum}`;
            const details = document.getElementById("remPlanDetails");
            
            const plans = {
                1: "<strong>Plano de Remediação Fase 1 (Descoberta & IAM):</strong><br>• Revogação de permissões excessivas identificadas pelo IAM Recommender.<br>• Aplicação mandatória de autenticação MFA/2FA para identidades de projeto.<br>• Desativação de chaves de service account inativas.",
                2: "<strong>Plano de Remediação Fase 2 (Auditoria Técnica & IaC):</strong><br>• Enforce de Public Access Prevention (PAP) e UBLA nos buckets Cloud Storage.<br>• Configuração de período de rotação de chaves Cloud KMS HSM para 60 dias.<br>• Fechamento de portas administrativas abertas (SSH/RDP) no firewall VPC.",
                3: "<strong>Plano de Remediação Fase 3 (Governança & Políticas):</strong><br>• Aplicação de Organization Policies restritivas (ex: restrição de localização geográfica).<br>• Sincronização e assinatura digital das políticas do SGSI via Zero-Copy (Google Drive).<br>• Registro formal da aprovação da diretoria no grafo de conformidade.",
                4: "<strong>Plano de Remediação Fase 4 (Grafo Criptográfico):</strong><br>• Recálculo completo de hashes SHA-256 para todos os nós de evidência.<br>• Emissão de novo recibo digital com não-repúdio.<br>• Reconciliação do Scorecard executivo em 100.0% (EXCELLENT)."
            };
            details.innerHTML = plans[phaseNum] || "Plano de remediação automatizado para a fase selecionada.";
            document.getElementById("remediationModal").classList.add("active");
        }

        function closeRemediationModal() {
            document.getElementById("remediationModal").classList.remove("active");
        }

        async function executePhaseRemediation() {
            const phaseNum = parseInt(document.getElementById("remPhaseNumber").value, 10);
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            appendLog(`[Remediação Fase ${phaseNum}] Aplicando ações corretivas automáticas no projeto ${project}...`);

            try {
                const res = await fetch("/api/audit/remediate_phase", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ phase: phaseNum, project_id: project })
                });
                const data = await res.json();
                closeRemediationModal();

                appendLog(`[Remediação Fase ${phaseNum}] Sucesso! Status: ${data.details.status}`, "success");
                data.details.actions_executed.forEach(a => appendLog(`  [Auto-Fix] ${a}`, "success"));

                const statusTag = document.getElementById(`statusPhase${phaseNum}`);
                if (statusTag) {
                    statusTag.innerText = "Remediado (100%)";
                    statusTag.className = "phase-status-tag compliant";
                }
                const findingsBox = document.getElementById(`findingsPhase${phaseNum}`);
                if (findingsBox) {
                    findingsBox.style.display = "block";
                    findingsBox.innerHTML = `<span style="color: var(--gcp-green);"><strong>Fase ${phaseNum} Remediada com Sucesso:</strong></span><br>` + data.details.actions_executed.map(a => `✓ ${escapeHtml(a)}`).join("<br>");
                }
            } catch (e) {
                appendLog(`[Remediação Erro] ${e}`, "error");
            }
        }

        // -------------------------------------------------------------------
        // Custom Subagents Management
        // -------------------------------------------------------------------
        async function loadSubagents() {
            try {
                const res = await fetch("/api/subagents");
                const data = await res.json();
                const container = document.getElementById("customSubagentsGrid");
                const countDisplay = document.getElementById("customCountDisplay");
                if (!container) return;

                const customList = data.custom_subagents || [];
                if (countDisplay) {
                    countDisplay.innerText = `${customList.length} subagente(s) ativo(s)`;
                }

                if (customList.length === 0) {
                    container.innerHTML = `<div style="grid-column: 1 / -1; color: var(--text-tertiary); padding: 18px; text-align: center; border: 1px dashed var(--border-subtle); border-radius: 12px;">Nenhum subagente customizado criado ainda. Clique em '+ Criar Novo Subagente' acima para customizar.</div>`;
                    return;
                }

                container.innerHTML = "";
                customList.forEach(agent => {
                    const card = document.createElement("div");
                    card.className = "card-panel";
                    const toolsHtml = (agent.tools || []).map(t => `<span class="tag-pill">#${escapeHtml(t)}</span>`).join(" ");
                    const controlsHtml = (agent.target_controls || []).map(c => `<span class="tag-pill" style="color: var(--gcp-blue);">#${escapeHtml(c)}</span>`).join(" ");

                    card.innerHTML = `
                        <div class="card-panel-header">
                            <div class="card-icon-avatar" style="background: rgba(138, 180, 248, 0.15); color: var(--gcp-blue);">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
                                    <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
                                    <path d="M12 6v6l4 2"/>
                                </svg>
                            </div>
                            <div style="flex: 1;">
                                <div style="display: flex; align-items: center; justify-content: space-between;">
                                    <div class="card-title">${escapeHtml(agent.name)}</div>
                                    <span class="badge-custom">Customizado</span>
                                </div>
                                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">${escapeHtml(agent.role || 'Auditor Especialista')}</div>
                            </div>
                        </div>
                        <div class="card-desc">${escapeHtml(agent.description || '')}</div>
                        <div class="subagent-prompt-preview"><strong>System Prompt:</strong> ${escapeHtml(agent.system_prompt || '')}</div>
                        <div style="margin-top: 4px;">
                            ${controlsHtml} ${toolsHtml}
                        </div>
                        <div class="subagent-card-actions">
                            <button class="btn-subagent-run" onclick="runCustomSubagent('${agent.id}')">Executar Auditoria</button>
                            <button class="btn-subagent-delete" onclick="deleteCustomSubagent('${agent.id}')" title="Excluir Subagente">
                                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                            </button>
                        </div>
                    `;
                    container.appendChild(card);
                });
            } catch (e) {
                console.error("Error loading subagents", e);
            }
        }

        function openCreateSubagentModal(agentId = null) {
            document.getElementById("subagentEditId").value = agentId || "";
            document.getElementById("subagentName").value = "";
            document.getElementById("subagentRole").value = "";
            document.getElementById("subagentControls").value = "";
            document.getElementById("subagentDesc").value = "";
            document.getElementById("subagentPrompt").value = "";
            document.getElementById("subagentModalTitle").innerText = agentId ? "Editar Subagente Customizado" : "Criar Novo Subagente Customizado";
            document.getElementById("subagentModal").classList.add("active");
        }

        function closeSubagentModal() {
            document.getElementById("subagentModal").classList.remove("active");
        }

        async function saveCustomSubagent() {
            const name = document.getElementById("subagentName").value.trim();
            const role = document.getElementById("subagentRole").value.trim();
            const controlsStr = document.getElementById("subagentControls").value.trim();
            const desc = document.getElementById("subagentDesc").value.trim();
            const prompt = document.getElementById("subagentPrompt").value.trim();
            const model = document.getElementById("subagentModel").value;

            if (!name || !role) {
                alert("Por favor, preencha o Nome e o Cargo do Subagente.");
                return;
            }

            const controls = controlsStr.split(",").map(c => c.trim()).filter(c => c);
            const checkboxes = document.querySelectorAll(".tool-checkbox-label input[type='checkbox']:checked");
            const tools = Array.from(checkboxes).map(cb => cb.value);

            const payload = {
                id: document.getElementById("subagentEditId").value || null,
                name: name,
                role: role,
                description: desc || `Subagente customizado para auditoria de ${role}`,
                system_prompt: prompt || `Você é o auditor ${name} focado em conformidade ISO 27001 no GCP.`,
                tools: tools.length > 0 ? tools : ["asset_inventory"],
                model: model,
                temperature: 0.1,
                target_controls: controls.length > 0 ? controls : ["A.5.1"]
            };

            try {
                const res = await fetch("/api/subagents", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                closeSubagentModal();
                loadSubagents();
                appendLog(`[Subagente Criado] Subagente '${data.subagent.name}' salvo e ativado no GEAP!`, "success");
            } catch (e) {
                alert("Erro ao salvar subagente: " + e);
            }
        }

        async function deleteCustomSubagent(agentId) {
            if (!confirm(`Deseja realmente remover o subagente customizado '${agentId}'?`)) return;
            try {
                const res = await fetch(`/api/subagents/${encodeURIComponent(agentId)}`, { method: "DELETE" });
                const data = await res.json();
                loadSubagents();
                appendLog(`[Subagente Removido] Subagente '${agentId}' excluído com sucesso.`, "success");
            } catch (e) {
                alert("Erro ao excluir subagente: " + e);
            }
        }

        async function runCustomSubagent(agentId) {
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            appendLog(`[Subagente ${agentId}] Executando auditoria especializada no projeto '${project}'...`);

            try {
                const res = await fetch(`/api/subagents/${encodeURIComponent(agentId)}/run?project_id=${encodeURIComponent(project)}`, { method: "POST" });
                const data = await res.json();
                appendLog(`[Subagente ${agentId}] Concluído com Score: ${data.compliance_score}%`, "success");
                if (data.findings) {
                    data.findings.forEach(f => appendLog(`  -> ${f}`, "success"));
                }
            } catch (e) {
                appendLog(`[Subagente Erro] ${e}`, "error");
            }
        }

        document.addEventListener("DOMContentLoaded", () => {
            loadProjects();
            loadIsoMatrix();
            loadSubagents();
        });

        function toggleSidebar() {
            const sidebar = document.getElementById("appSidebar");
            sidebar.classList.toggle("collapsed");
        }

        function switchView(viewId) {
            document.querySelectorAll(".view-pane").forEach(p => p.classList.remove("active"));
            const target = document.getElementById(viewId);
            if (target) target.classList.add("active");

            const agentMap = {
                "view-chat": "agentBtnChat",
                "view-phases": "agentBtnPhases",
                "view-matrix": "agentBtnMatrix",
                "view-connectors": "agentBtnConnectors",
                "view-scorecard": "agentBtnScorecard"
            };

            document.querySelectorAll(".agent-item").forEach(b => b.classList.remove("active"));
            if (agentMap[viewId]) {
                const btn = document.getElementById(agentMap[viewId]);
                if (btn) btn.classList.add("active");
            }

            const titleMap = {
                "view-chat": "Chatbot Auditor",
                "view-phases": "Scan por Fases",
                "view-matrix": "Matriz ISO 27001 Escalável",
                "view-connectors": "Subagentes & Zero-Copy",
                "view-scorecard": "Scorecard & Grafo de Evidências",
                "view-report-exec": "Dossiê Executivo PSO"
            };
            document.getElementById("topActiveTitle").innerText = titleMap[viewId] || "Auditor";
        }

        function startNewConversation() {
            switchView("view-chat");
            const chatArea = document.getElementById("chatArea");
            const hero = document.getElementById("geminiHero");
            chatArea.innerHTML = "";
            chatArea.appendChild(hero);
            document.getElementById("chatInput").value = "";
        }

        function openExecutiveReport() {
            switchView("view-report-exec");
            document.getElementById("docProjectsAudited").innerText = Array.from(selectedProjectIds).join(", ");
        }

        function printExecutiveReport() {
            openExecutiveReport();
            setTimeout(() => { window.print(); }, 250);
        }

        // Project Scope Management
        async function loadProjects() {
            try {
                const res = await fetch("/api/projects");
                const data = await res.json();
                activeProjects = data.projects || [];
                selectedProjectIds = new Set(activeProjects.map(p => p.project_id));
                renderScopeBox();
            } catch (e) {
                console.error("Error loading projects", e);
            }
        }

        function renderScopeBox() {
            const container = document.getElementById("scopeProjectsList");
            container.innerHTML = "";

            activeProjects.forEach(proj => {
                const isSelected = selectedProjectIds.has(proj.project_id);
                const pill = document.createElement("div");
                pill.className = "project-pill-item";
                pill.innerHTML = `
                    <div class="project-pill-left">
                        <input type="checkbox" class="project-checkbox" ${isSelected ? "checked" : ""} onchange="toggleProjectSelection('${proj.project_id}', this.checked)">
                        <span class="project-id-text" title="${proj.project_id}">${proj.project_id}</span>
                    </div>
                    <span class="env-badge">${proj.environment || "PROD"}</span>
                `;
                container.appendChild(pill);
            });

            const count = selectedProjectIds.size;
            document.getElementById("topProjectCountBadge").innerText = `${count} ${count === 1 ? 'projeto ativo' : 'projetos ativos'}`;
        }

        function toggleProjectSelection(pid, checked) {
            if (checked) {
                selectedProjectIds.add(pid);
            } else {
                if (selectedProjectIds.size > 1) {
                    selectedProjectIds.delete(pid);
                } else {
                    alert("Pelo menos um projeto deve permanecer no escopo de auditoria.");
                    renderScopeBox();
                    return;
                }
            }
            const count = selectedProjectIds.size;
            document.getElementById("topProjectCountBadge").innerText = `${count} ${count === 1 ? 'projeto ativo' : 'projetos ativos'}`;
        }

        function openProjectModal() { document.getElementById("projectModal").classList.add("active"); }
        function closeProjectModal() { document.getElementById("projectModal").classList.remove("active"); }

        async function submitAddProject() {
            const pid = document.getElementById("modalProjectId").value.trim();
            const env = document.getElementById("modalEnvironment").value.trim() || "PRODUCTION";
            const reg = document.getElementById("modalRegion").value.trim() || "us-central1";

            if (!pid) { alert("Informe o ID do projeto GCP"); return; }

            try {
                const res = await fetch("/api/projects/add", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ project_id: pid, environment: env, region: reg })
                });
                if (res.ok) {
                    closeProjectModal();
                    document.getElementById("modalProjectId").value = "";
                    loadProjects();
                }
            } catch (e) {
                alert("Erro ao adicionar projeto: " + e);
            }
        }

        // Chatbot Interaction
        function promptPreFill(text) {
            switchView("view-chat");
            const input = document.getElementById("chatInput");
            input.value = text;
            handleChatInput(input);
            sendChatMessage();
        }

        function handleChatKey(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        }

        function handleChatInput(el) {
            el.style.height = "24px";
            el.style.height = Math.min(el.scrollHeight, 120) + "px";
            const btn = document.getElementById("sendBtn");
            if (el.value.trim().length > 0) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        }

        async function sendChatMessage() {
            const input = document.getElementById("chatInput");
            const text = input.value.trim();
            if (!text) return;

            const chatArea = document.getElementById("chatArea");
            const hero = document.getElementById("geminiHero");
            if (hero) hero.remove();

            const userRow = document.createElement("div");
            userRow.className = "msg-row user";
            userRow.innerHTML = `
                <div class="msg-content">${escapeHtml(text)}</div>
                <div class="msg-avatar user-av">JS</div>
            `;
            chatArea.appendChild(userRow);

            input.value = "";
            handleChatInput(input);
            chatArea.scrollTop = chatArea.scrollHeight;

            const botRow = document.createElement("div");
            botRow.className = "msg-row bot";
            botRow.innerHTML = `
                <div class="msg-avatar gemini">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
                        <path d="M12 2L20 5.8V11.5C20 16.5 16.6 20.8 12 22C7.4 20.8 4 16.5 4 11.5V5.8L12 2Z" fill="#1a73e8" fill-opacity="0.2" stroke="#8ab4f8" stroke-width="1.8"/>
                        <path d="M12 5.5L17.5 8V12C17.5 15.5 15.2 18.5 12 19.5C8.8 18.5 6.5 15.5 6.5 12V8L12 5.5Z" fill="#1a73e8"/>
                    </svg>
                </div>
                <div class="msg-content" id="activeBotReply">
                    <span style="color: var(--text-tertiary)">Agentic GRC Auditor (Google Cloud Security PSO) avaliando telemetria e grafo de evidências...</span>
                </div>
            `;
            chatArea.appendChild(botRow);
            chatArea.scrollTop = chatArea.scrollHeight;

            try {
                const res = await fetch("/api/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: text, project_id: Array.from(selectedProjectIds)[0] })
                });
                const data = await res.json();
                const replyElem = document.getElementById("activeBotReply");
                replyElem.removeAttribute("id");
                replyElem.innerHTML = renderExecutiveMarkdown(data.response || "Sem resposta do auditor.");
            } catch (err) {
                const replyElem = document.getElementById("activeBotReply");
                replyElem.removeAttribute("id");
                replyElem.innerHTML = `<span style="color: var(--gcp-red)">Erro na comunicação com o auditor PSO: ${err}</span>`;
            }
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        // Phased Audit Execution
        async function triggerPhasedAudit() {
            const projects = Array.from(selectedProjectIds);
            const consoleBox = document.getElementById("auditLogsContainer");
            consoleBox.innerHTML = "";

            appendLog(`Iniciando Scan de Auditoria estruturado em 4 Fases para [${projects.join(', ')}]...`, "info");

            for (let i = 1; i <= 4; i++) {
                document.getElementById(`statusPhase${i}`).innerText = "Em Execução...";
                document.getElementById(`statusPhase${i}`).className = "phase-status-tag";
                document.getElementById(`cardPhase${i}`).classList.add("active");
                document.getElementById(`fillPhase${i}`).style.width = "40%";
            }

            try {
                const res = await fetch("/api/audit/run_phases", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ projects: projects })
                });
                const data = await res.json();

                document.getElementById("auditExecId").innerText = `Exec ID: ${data.execution_id || 'COMPLETED'}`;

                for (let i = 1; i <= 4; i++) {
                    document.getElementById(`statusPhase${i}`).innerText = "Concluído";
                    document.getElementById(`statusPhase${i}`).className = "phase-status-tag completed";
                    document.getElementById(`fillPhase${i}`).style.width = "100%";
                }

                if (data.phases) {
                    data.phases.forEach((p, idx) => {
                        appendLog(`[Fase ${idx+1}] ${p.phase}: STATUS ${p.status}`, "success");
                        if (p.findings) {
                            p.findings.forEach(f => appendLog(`  -> ${f}`));
                        }
                    });
                }
                appendLog(`Auditoria Finalizada com Sucesso! Score Global: ${data.overall_score}%`, "success");
            } catch (err) {
                appendLog(`Erro na execução do scan: ${err}`, "log-msg");
            }
        }

        function appendLog(msg, type = "") {
            const consoleBox = document.getElementById("auditLogsContainer");
            const entry = document.createElement("div");
            entry.className = "log-entry";
            const now = new Date().toTimeString().split(' ')[0];
            entry.innerHTML = `<span class="log-ts">${now}</span><span class="log-msg ${type}">${escapeHtml(msg)}</span>`;
            consoleBox.appendChild(entry);
            consoleBox.scrollTop = consoleBox.scrollHeight;
        }

        // ISO Matrix Handling with Expandable Rows (How to Check & How to Maintain)
        async function loadIsoMatrix(theme = "Todos", search = "") {
            let url = `/api/iso_matrix?theme=${encodeURIComponent(theme)}`;
            if (search) url += `&search=${encodeURIComponent(search)}`;

            try {
                const res = await fetch(url);
                const data = await res.json();
                matrixControls = data.controls || [];
                renderMatrixTable(matrixControls);
            } catch (e) {
                console.error("Error loading matrix", e);
            }
        }

        function renderMatrixTable(items) {
            const tbody = document.getElementById("matrixTableBody");
            tbody.innerHTML = "";

            if (items.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-tertiary); padding: 24px;">Nenhum controle encontrado.</td></tr>`;
                return;
            }

            items.forEach((c, idx) => {
                const safeId = c.id.replace(/[^a-zA-Z0-9]/g, '_');
                const rowId = `ctrl_row_${safeId}`;
                const detailId = `ctrl_detail_${safeId}`;

                // Main Row
                const tr = document.createElement("tr");
                tr.className = "ctrl-main-row";
                tr.id = rowId;
                tr.onclick = (e) => {
                    if (!e.target.closest("button")) {
                        toggleControlRow(detailId);
                    }
                };

                tr.innerHTML = `
                    <td><span class="ctrl-id-badge">${c.id}</span></td>
                    <td style="font-weight: 500;">${escapeHtml(c.name)}</td>
                    <td style="color: var(--text-secondary);">${escapeHtml(c.theme)}</td>
                    <td style="line-height: 1.5;">${escapeHtml(c.gcp_mapping)}</td>
                    <td><span class="status-badge compliant">${c.status}</span></td>
                    <td><span style="font-size: 11px; color: ${c.severity === 'CRITICAL' ? 'var(--gcp-red)' : 'var(--text-secondary)'}">${c.severity}</span></td>
                    <td style="text-align: center;">
                        <button class="btn-expand-ctrl" onclick="toggleControlRow('${detailId}')">
                            <span id="label_${detailId}">Ver Detalhes</span>
                            <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor">
                                <polyline points="6 9 12 15 18 9"/>
                            </svg>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);

                // Expandable Details Drawer Row
                const detailTr = document.createElement("tr");
                detailTr.className = "ctrl-detail-row";
                detailTr.id = detailId;

                const attrs = c.attributes || {};
                const tagsHtml = `
                    <span class="tag-pill">#${escapeHtml(attrs.type || 'Preventivo')}</span>
                    <span class="tag-pill">#${escapeHtml(attrs.properties || 'Confidencialidade')}</span>
                    <span class="tag-pill">#${escapeHtml(attrs.concepts || 'Proteger')}</span>
                    <span class="tag-pill">#${escapeHtml(attrs.capabilities || 'Governança')}</span>
                    <span class="tag-pill">#${escapeHtml(attrs.domains || 'Proteção')}</span>
                `;

                detailTr.innerHTML = `
                    <td colspan="7" style="padding: 0; border: none;">
                        <div class="ctrl-detail-container">
                            <div class="ctrl-detail-grid">
                                <!-- Coluna Esquerda: Descrição & Taxonomia SoA -->
                                <div class="detail-box">
                                    <div class="detail-box-title">
                                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                            <polyline points="14 2 14 8 20 8"/>
                                        </svg>
                                        Descrição Oficial do Requisito (ISO/IEC 27001:2022)
                                    </div>
                                    <div class="detail-box-content">
                                        ${escapeHtml(c.description || 'Definição estabelecida conforme o Anexo A da norma ISO/IEC 27001:2022.')}
                                    </div>

                                    <div style="margin-top: 10px;">
                                        <div style="font-size: 11px; font-weight: 700; color: var(--text-tertiary); text-transform: uppercase; margin-bottom: 4px;">
                                            Taxonomia de 5 Atributos ISO
                                        </div>
                                        <div>${tagsHtml}</div>
                                    </div>

                                    <div style="margin-top: 10px; font-size: 11.5px; color: var(--gcp-green);">
                                        <strong>Declaração de Aplicabilidade (SoA):</strong> ${escapeHtml(c.soa_status || 'APLICÁVEL (INCLUÍDO NO SGSI)')}
                                    </div>
                                </div>

                                <!-- Coluna Direita: Como Checar & Como Manter Compliance -->
                                <div style="display: flex; flex-direction: column; gap: 12px;">
                                    <div class="detail-box" style="border-left: 3px solid var(--gcp-green);">
                                        <div class="detail-box-title" style="color: var(--gcp-green);">
                                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                                <polyline points="20 6 9 17 4 12"/>
                                            </svg>
                                            Como Checar em Compliance (Auditoria & Telemetria GCP)
                                        </div>
                                        <div class="detail-box-content">
                                            ${escapeHtml(c.how_to_check || 'Validar recursos via Cloud Asset Inventory e checar permissões IAM.')}
                                        </div>
                                    </div>

                                    <div class="detail-box" style="border-left: 3px solid var(--gcp-yellow);">
                                        <div class="detail-box-title" style="color: var(--gcp-yellow);">
                                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                                            </svg>
                                            Como Manter o Compliance (Políticas & Prevenção de Drift)
                                        </div>
                                        <div class="detail-box-content">
                                            ${escapeHtml(c.how_to_maintain || 'Aplicar Organization Policies restritivas e monitorar alertas no Cloud Monitoring.')}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                `;
                tbody.appendChild(detailTr);
            });
        }

        function toggleControlRow(detailId) {
            const row = document.getElementById(detailId);
            const label = document.getElementById(`label_${detailId}`);
            if (row) {
                row.classList.toggle("open");
                if (label) {
                    label.innerText = row.classList.contains("open") ? "Ocultar Detalhes" : "Ver Detalhes";
                }
            }
        }

        function filterMatrixByTheme(theme) {
            currentThemeFilter = theme;
            document.querySelectorAll(".btn-filter-pill").forEach(b => {
                b.classList.toggle("active", b.innerText === theme);
            });
            document.querySelectorAll(".theme-card").forEach(c => {
                const title = c.querySelector(".theme-card-title").innerText;
                c.classList.toggle("active", (theme === "Todos" && title.includes("Todos")) || (theme !== "Todos" && title.includes(theme.split(" ")[0])));
            });
            const searchVal = document.getElementById("matrixSearchInput").value;
            loadIsoMatrix(currentThemeFilter, searchVal);
        }

        function searchMatrix(val) {
            loadIsoMatrix(currentThemeFilter, val);
        }

        async function triggerSubagent(subagent, target) {
            switchView("view-chat");
            promptPreFill(`Executar auditoria com o agente ${subagent} focado em ${target}`);
        }

        function openStorageModal() { document.getElementById("storageModal").classList.add("active"); }
        function closeStorageModal() { document.getElementById("storageModal").classList.remove("active"); }

        async function submitStorageLink() {
            const source = document.getElementById("storageSourceSelect").value;
            const uri = document.getElementById("storageUri").value.trim();
            try {
                const res = await fetch("/api/storage/link", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ source: source, uri: uri, user_token: "delegated-spiffe-token" })
                });
                const data = await res.json();
                closeStorageModal();
                alert(`Repositório ${source} conectado com garantia Zero-Copy!\nDocumentos indexados: ${data.discovered_documents ? data.discovered_documents.length : 0}`);
            } catch (e) {
                alert("Erro ao conectar: " + e);
            }
        }

        function openUploadModal() { document.getElementById("uploadModal").classList.add("active"); }
        function closeUploadModal() { document.getElementById("uploadModal").classList.remove("active"); }

        async function submitIacUpload() {
            const fileInput = document.getElementById("iacFileInput");
            if (!fileInput.files.length) { alert("Selecione um arquivo IaC"); return; }

            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            try {
                const res = await fetch("/api/upload", { method: "POST", body: formData });
                const data = await res.json();
                closeUploadModal();
                switchView("view-chat");
                const chatArea = document.getElementById("chatArea");
                const hero = document.getElementById("geminiHero");
                if (hero) hero.remove();

                const botRow = document.createElement("div");
                botRow.className = "msg-row bot";
                botRow.innerHTML = `
                    <div class="msg-avatar gemini">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
                            <path d="M12 2L20 5.8V11.5C20 16.5 16.6 20.8 12 22C7.4 20.8 4 16.5 4 11.5V5.8L12 2Z" fill="#1a73e8" fill-opacity="0.2" stroke="#8ab4f8" stroke-width="1.8"/>
                            <path d="M12 5.5L17.5 8V12C17.5 15.5 15.2 18.5 12 19.5C8.8 18.5 6.5 15.5 6.5 12V8L12 5.5Z" fill="#1a73e8"/>
                        </svg>
                    </div>
                    <div class="msg-content">
                        <strong>Relatório de Varredura de IaC (${escapeHtml(data.filename)}):</strong><br>
                        Status: <strong>${data.audit_finding.status}</strong><br>
                        Regras Avaliadas: ${data.audit_finding.rules_evaluated}<br>
                        Violações Encontradas: ${data.audit_finding.violations_found.length}
                    </div>
                `;
                chatArea.appendChild(botRow);
                chatArea.scrollTop = chatArea.scrollHeight;
            } catch (e) {
                alert("Erro no upload: " + e);
            }
        }

        async function approveRemediation(remId) {
            try {
                const res = await fetch("/api/remediation/approve", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ remediation_id: remId })
                });
                const data = await res.json();
                alert(`Aditamento ${remId} APROVADO com sucesso! Status: ${data.status}`);
            } catch (e) {
                alert("Erro ao aprovar: " + e);
            }
        }

        function toggleExportMenu() {
            document.getElementById("exportDropdown").classList.toggle("show");
        }
        window.onclick = function(e) {
            if (!e.target.closest("#exportDropdown")) {
                document.getElementById("exportDropdown").classList.remove("show");
            }
        };

        function escapeHtml(text) {
            const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }

        function renderExecutiveMarkdown(md) {
            if (typeof marked !== 'undefined') {
                try {
                    return marked.parse(md);
                } catch (e) {
                    console.error("Marked error", e);
                }
            }
            let html = md
                .replace(/^### (.*$)/gim, '<h3>$1</h3>')
                .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                .replace(/^# (.*$)/gim, '<h1>$1</h1>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                .replace(/`([^`]+)`/gim, '<code>$1</code>')
                .replace(/^\* (.*$)/gim, '<li>$1</li>')
                .replace(/\n\n/gim, '<br><br>');
            return html;
        }
    </script>

    <!-- Modal: Criar / Editar Subagente Customizado -->
    <div class="modal-backdrop" id="subagentModal">
        <div class="modal-dialog" style="max-width: 580px;">
            <div class="modal-header">
                <span class="modal-title" id="subagentModalTitle">Criar Novo Subagente Customizado</span>
                <span class="btn-modal-close" onclick="closeSubagentModal()">&times;</span>
            </div>
            <div class="modal-body">
                <input type="hidden" id="subagentEditId" value="">
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Nome do Subagente</label>
                        <input type="text" id="subagentName" class="form-control" placeholder="Ex: FinOps & Storage Compliance Auditor">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Cargo / Especialidade</label>
                        <input type="text" id="subagentRole" class="form-control" placeholder="Ex: Auditor de Retenção e Ciclo de Vida">
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Controles ISO Alvo (separados por vírgula)</label>
                        <input type="text" id="subagentControls" class="form-control" placeholder="Ex: A.5.9, A.8.10, A.8.11">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Modelo Cognitivo</label>
                        <select id="subagentModel" class="form-control">
                            <option value="gemini-2.5-flash" selected>Gemini 2.5 Flash (Recomendado / Baixa Latência)</option>
                            <option value="gemini-1.5-pro">Gemini 1.5 Pro (Raciocínio Profundo)</option>
                            <option value="gemini-2.5-pro">Gemini 2.5 Pro (Lead Auditor Especialista)</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Descrição do Propósito</label>
                    <input type="text" id="subagentDesc" class="form-control" placeholder="Breve resumo do que este subagente avalia no ambiente GCP.">
                </div>

                <div class="form-group">
                    <label class="form-label">System Prompt / Instrução Especializada</label>
                    <textarea id="subagentPrompt" class="form-control" rows="4" placeholder="Defina a metodologia e critérios do auditor: 'Você é o especialista PSO responsável por...'"></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label">Ferramentas & Permissões GCP Habilitadas</label>
                    <div class="tools-checkbox-grid">
                        <label class="tool-checkbox-label"><input type="checkbox" value="asset_inventory" checked> Cloud Asset Inventory</label>
                        <label class="tool-checkbox-label"><input type="checkbox" value="iam_recommender" checked> IAM Recommender</label>
                        <label class="tool-checkbox-label"><input type="checkbox" value="cloud_kms"> Cloud KMS HSM</label>
                        <label class="tool-checkbox-label"><input type="checkbox" value="vpc_sc"> VPC Service Controls</label>
                        <label class="tool-checkbox-label"><input type="checkbox" value="iac_scanner"> IaC Terraform Scanner</label>
                        <label class="tool-checkbox-label"><input type="checkbox" value="zero_copy_drive"> Zero-Copy Workspace Drive</label>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-cancel" onclick="closeSubagentModal()">Cancelar</button>
                <button class="btn-confirm" onclick="saveCustomSubagent()" style="background: var(--gcp-blue);">Salvar Subagente</button>
            </div>
        </div>
    </div>

    <!-- Modal: Tratar Desvios de Fase (Remediação) -->
    <div class="modal-backdrop" id="remediationModal">
        <div class="modal-dialog" style="max-width: 520px;">
            <div class="modal-header">
                <span class="modal-title" id="remModalTitle">Tratar Desvios da Fase</span>
                <span class="btn-modal-close" onclick="closeRemediationModal()">&times;</span>
            </div>
            <div class="modal-body">
                <input type="hidden" id="remPhaseNumber" value="1">
                <div id="remPlanDetails" style="font-size: 13px; line-height: 1.6; color: #d1d5db;">
                    Carregando plano de remediação...
                </div>
                <div style="margin-top: 14px; background: rgba(138, 180, 248, 0.1); border: 1px solid rgba(138, 180, 248, 0.25); border-radius: 8px; padding: 12px; font-size: 12px; color: var(--gcp-blue);">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" style="vertical-align: middle; margin-right: 4px;">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    A execução registrará as alterações no Grafo de Evidências com novo hash SHA-256 para auditoria contínua.
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-cancel" onclick="closeRemediationModal()">Fechar</button>
                <button class="btn-confirm" onclick="executePhaseRemediation()" style="background: var(--gcp-green);">Executar Remediação Automática</button>
            </div>
        </div>
    </div>

</body>
</html>
"""
