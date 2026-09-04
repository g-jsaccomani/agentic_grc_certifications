"""Official Google Cloud Security - Agentic GRC Auditor Web Portal."""

PORTAL_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Cloud Security - Agentic GRC Auditor</title>
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* Left Sidebar */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        .gcp-sec-logo-icon {
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
            width: 20px;
            height: 20px;
            border-radius: 0 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent !important;
            color: var(--text-secondary);
            flex-shrink: 0;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        .agent-item:hover .agent-avatar {
            color: var(--text-primary);
        }

        .agent-item.active .agent-avatar {
            background: transparent !important;
            color: var(--gcp-blue) !important;
            border: none !important;
        }

        .btn-new-audit {
            width: 100%;
            background: var(--bg-surface);
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 9px 14px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: var(--transition-smooth);
            margin-bottom: 8px;
        }
        .btn-new-audit:hover {
            background: var(--bg-surface-hover);
            border-color: var(--gcp-blue);
            color: var(--gcp-blue);
        }

        .btn-create-subagent-clean {
            width: 100%;
            background: rgba(138, 180, 248, 0.08);
            color: var(--gcp-blue);
            border: 1px dashed rgba(138, 180, 248, 0.35);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12.5px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: var(--transition-smooth);
            margin-top: 6px;
        }
        .btn-create-subagent-clean:hover {
            background: rgba(138, 180, 248, 0.16);
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* Bottom Left: Scope Box & Profile */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* Main Container */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* View 1: Chatbot Auditor */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* View 1: Chatbot Auditor (Full Width Viewport, Scrollbar on Far Right Edge) */
        #view-chat {
            padding: 0 !important;
            height: 100%;
            width: 100%;
        }

        .chat-view-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            max-width: 100%;
            position: relative;
        }

        .chat-messages-area {
            flex: 1;
            overflow-y: auto;
            padding: 20px 32px 120px 32px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            width: 100%;
        }

        .chat-messages-area::-webkit-scrollbar {
            width: 8px;
        }
        .chat-messages-area::-webkit-scrollbar-track {
            background: transparent;
        }
        .chat-messages-area::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }
        .chat-messages-area::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.3);
        }

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
            width: 72px;
            height: 72px;
            border-radius: 0 !important;
            background: transparent !important;
            display: flex;
            align-items: center;
            justify-content: center;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        .hero-title { font-size: 32px; font-weight: 600; letter-spacing: -0.5px; color: #ffffff; }
        .hero-badge-sec {
            font-size: 12px;
            font-weight: 600;
            color: var(--gcp-blue);
            text-transform: uppercase;
            letter-spacing: 1px;
            background: rgba(138, 180, 248, 0.1);
            padding: 4px 12px;
            border-radius: 12px;
            border: 1px solid rgba(138, 180, 248, 0.2);
            display: inline-block;
        }

        .hero-subtitle {
            font-size: 14.5px;
            color: var(--text-secondary);
            max-width: 580px;
            line-height: 1.65;
        }
        .hero-suggestions-stack {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 100%;
            max-width: 580px;
            margin-top: 10px;
        }
        .hero-suggestion-card {
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 12px 16px;
            color: var(--text-primary);
            font-size: 13.5px;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .hero-suggestion-card:hover { background: var(--bg-surface); border-color: var(--gcp-blue); transform: translateX(4px); }

        .msg-row { display: flex; gap: 16px; width: 100%; max-width: 980px; margin: 0 auto; animation: fadeIn 0.25s ease; }
        .msg-row.user { justify-content: flex-end; }
        .msg-avatar { width: 34px; height: 34px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
        .msg-avatar.gemini { background: transparent !important; border: none !important; border-radius: 0 !important; box-shadow: none !important; }
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* View 2: Scan por Fases */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* View 3: Matriz ISO 27001 Escalável (With Themes Summary & Rich Drawer) */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
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

        
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* Left Drawer for Subagent Creation (Lado Esquerdo) */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        .left-drawer-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(4px);
            z-index: 1100;
        }
        .left-drawer-overlay.active { display: block; }
        .left-drawer {
            position: fixed;
            top: 0;
            left: -520px;
            width: 480px;
            max-width: 90vw;
            height: 100vh;
            background: var(--bg-surface);
            border-right: 1px solid var(--border-subtle);
            box-shadow: 6px 0 28px rgba(0, 0, 0, 0.75);
            z-index: 1200;
            display: flex;
            flex-direction: column;
            transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .left-drawer.open { left: 0; }
        .left-drawer-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .left-drawer-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .left-drawer-body {
            padding: 24px;
            overflow-y: auto;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .left-drawer-footer {
            padding: 16px 24px;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            background: var(--bg-canvas);
        }

        /* Phase Actions and Remediation Drawer in Scan por Fases */
        .phase-actions-row {
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }
        .btn-phase-exec {
            flex: 1;
            background: rgba(138, 180, 248, 0.12);
            color: var(--gcp-blue);
            border: 1px solid rgba(138, 180, 248, 0.28);
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
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
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }
        .btn-phase-treat:hover {
            background: rgba(234, 67, 53, 0.22);
            border-color: var(--gcp-red);
        }
        .phase-findings-box {
            margin-top: 10px;
            padding: 10px 12px;
            background: var(--bg-canvas);
            border-radius: 6px;
            font-size: 11.5px;
            color: var(--text-secondary);
            line-height: 1.45;
            border-left: 3px solid var(--gcp-blue);
            max-height: 90px;
            overflow-y: auto;
        }

        /* Inline Phase Remediation Container in Scan por Fases */
        .phase-remediation-drawer {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 20px;
            margin-top: 18px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            border-left: 4px solid var(--gcp-green);
        }
        .rem-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
        }
        .rem-title-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .rem-badge {
            background: rgba(52, 168, 83, 0.15);
            color: var(--gcp-green);
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid rgba(52, 168, 83, 0.3);
        }
        .rem-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-primary);
        }
        .btn-close-rem {
            background: none;
            border: none;
            color: var(--text-tertiary);
            font-size: 20px;
            cursor: pointer;
            line-height: 1;
        }
        .btn-close-rem:hover { color: var(--text-primary); }
        .rem-body {
            font-size: 13px;
            color: #d1d5db;
            line-height: 1.6;
            background: var(--bg-canvas);
            padding: 14px;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
        }
        .rem-footer {
            margin-top: 16px;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }

        /* View 4: Subagentes & Zero-Copy */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* View 5: Scorecard */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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

        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        
        /* External Audit Technical Report Styling */
        .doc-viewer-actions-bar {
            max-width: 900px;
            margin: 0 auto 16px auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 8px 16px;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }
        .doc-viewer-actions-left {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
            flex: 1;
        }
        .doc-viewer-chip {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 3px 8px;
            border-radius: 4px;
            background: rgba(234, 67, 53, 0.12);
            color: #d93025;
            border: 1px solid rgba(234, 67, 53, 0.25);
            white-space: nowrap;
        }
        .doc-viewer-chip.blue {
            background: rgba(66, 133, 244, 0.12);
            color: #1a73e8;
            border-color: rgba(66, 133, 244, 0.25);
        }
        .doc-viewer-title {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .doc-viewer-actions-right {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }
        .btn-doc-action {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            height: 32px;
            padding: 0 12px;
            font-size: 12px;
            font-weight: 600;
            border-radius: 6px;
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            color: var(--text-primary);
            cursor: pointer;
            white-space: nowrap !important;
            text-decoration: none;
            transition: all 0.15s ease;
            box-sizing: border-box;
            line-height: 1;
        }
        .btn-doc-action:hover {
            border-color: var(--border-focus);
            background: var(--bg-surface-hover);
        }
        .btn-doc-action.primary {
            background: #1a73e8;
            color: #ffffff;
            border-color: #1a73e8;
        }
        .btn-doc-action.primary:hover {
            background: #1557b0;
        }
        @media print {
            .doc-viewer-actions-bar { display: none !important; }
        }

        .tech-section-lead {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 20px;
        }

        .tech-stat-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin: 20px 0 28px 0;
        }
        .tech-stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 16px;
            text-align: left;
            border-top: 3px solid #1a73e8;
        }
        .tech-stat-card.red { border-top-color: #ea4335; }
        .tech-stat-card.green { border-top-color: #34a853; }
        .tech-stat-card.yellow { border-top-color: #fbbc04; }

        .tech-stat-code {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .tech-stat-val {
            font-size: 26px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }
        .tech-stat-desc {
            font-size: 11px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .tech-code-box {
            background: #1e1e24;
            color: #dcdfe4;
            border-radius: 8px;
            padding: 14px 16px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 12px;
            line-height: 1.5;
            margin: 10px 0 16px 0;
            overflow-x: auto;
            border: 1px solid #2e303e;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
        }
        .tech-code-comment { color: #5c6370; }
        .tech-code-cmd { color: #61afef; font-weight: 600; }
        .tech-code-key { color: #e5c07b; }
        .tech-code-val { color: #98c379; }
        .tech-code-str { color: #e06c75; }

        .tech-evidence-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 18px 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        }
        .tech-evidence-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-subtle);
        }
        .tech-evidence-title-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .tech-evidence-badge {
            background: #e8f0fe;
            color: #1a73e8;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
        }
        .tech-evidence-title {
            font-size: 14px;
            font-weight: 700;
            color: var(--text-primary);
        }
        .tech-badge-pass {
            background: #e6f4ea;
            color: #137333;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .tech-signature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 36px;
            padding-top: 24px;
            border-top: 2px dashed var(--border-subtle);
        }
        .tech-sig-box {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        .tech-sig-line {
            height: 1px;
            background: var(--border-subtle);
            margin: 36px 12px 10px 12px;
        }
        .tech-sig-name {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-primary);
        }
        .tech-sig-role {
            font-size: 11px;
            color: var(--text-secondary);
        }
        .tech-sig-status {
            display: inline-block;
            margin-top: 6px;
            font-size: 10px;
            font-weight: 700;
            color: #137333;
            background: #e6f4ea;
            padding: 2px 6px;
            border-radius: 4px;
        }

        /* Official Google Cloudstyle Document Styles */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        .cloudstyle-doc-sheet {
            background: #ffffff !important;
            color: #202124 !important;
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 24px auto 40px auto;
            padding: 56px 64px;
            border-radius: 8px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.35);
            position: relative;
            line-height: 1.6;
        }
        .cloudstyle-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .cloudstyle-brand-logo {
            height: 36px;
            object-fit: contain;
        }
        .cloudstyle-confidential-pill {
            font-family: 'Google Sans', sans-serif;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #5f6368;
            background: #f1f3f4;
            padding: 5px 12px;
            border-radius: 4px;
        }
        .google-color-stripe-bar {
            height: 5px;
            width: 100%;
            background: linear-gradient(to right, #4285F4 0%, #4285F4 25%, #EA4335 25%, #EA4335 50%, #FBBC04 50%, #FBBC04 75%, #34A853 75%, #34A853 100%);
            border-radius: 2px;
            margin: 14px 0 28px 0;
        }
        .cloudstyle-doc-title {
            font-family: 'Google Sans', sans-serif;
            font-size: 32px;
            font-weight: 700;
            color: #202124;
            margin: 0 0 8px 0;
            letter-spacing: -0.5px;
            line-height: 1.25;
        }
        .cloudstyle-doc-subtitle {
            font-family: 'Roboto', sans-serif;
            font-size: 15px;
            color: #5f6368;
            margin: 0 0 28px 0;
        }
        .cloudstyle-meta-box {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 32px;
            background: #f8f9fa;
            border: 1px solid #dadce0;
            border-radius: 8px;
            overflow: hidden;
        }
        .cloudstyle-meta-box td {
            padding: 10px 16px;
            border-bottom: 1px solid #dadce0;
            font-size: 12.5px;
            color: #202124;
        }
        .cloudstyle-meta-box td:first-child {
            font-family: 'Google Sans', sans-serif;
            font-weight: 600;
            color: #3c4043;
            width: 28%;
            background: #f1f3f4;
        }
        .cloudstyle-highlights-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin: 28px 0;
        }
        .cloudstyle-highlight-item {
            background: #ffffff;
            border: 1px solid #dadce0;
            border-radius: 8px;
            padding: 16px 14px;
            box-shadow: 0 1px 3px rgba(60, 64, 67, 0.08);
        }
        .cloudstyle-num-badge {
            font-family: 'Google Sans', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #1a73e8;
            line-height: 1;
            margin-bottom: 8px;
        }
        .cloudstyle-num-title {
            font-family: 'Google Sans', sans-serif;
            font-size: 13.5px;
            font-weight: 600;
            color: #202124;
            margin-bottom: 6px;
        }
        .cloudstyle-num-desc {
            font-size: 11.5px;
            color: #5f6368;
            line-height: 1.45;
        }
        .cloudstyle-quote-callout {
            background: #f8f9fa;
            border-left: 4px solid #1a73e8;
            padding: 18px 24px;
            border-radius: 0 8px 8px 0;
            margin: 28px 0;
        }
        .cloudstyle-quote-text {
            font-family: 'Google Sans', sans-serif;
            font-size: 14.5px;
            font-style: italic;
            color: #202124;
            line-height: 1.6;
            margin-bottom: 8px;
        }
        .cloudstyle-quote-author {
            font-size: 12px;
            font-weight: 600;
            color: #1a73e8;
        }
        .cloudstyle-heading-block {
            font-family: 'Google Sans', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: #202124;
            margin: 36px 0 14px 0;
            padding-bottom: 6px;
            border-bottom: 1px solid #dadce0;
        }
        .cloudstyle-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
            font-size: 12.5px;
        }
        .cloudstyle-table th {
            font-family: 'Google Sans', sans-serif;
            background: #f1f3f4;
            color: #202124;
            font-weight: 600;
            padding: 10px 14px;
            border: 1px solid #dadce0;
            text-align: left;
        }
        .cloudstyle-table td {
            padding: 10px 14px;
            border: 1px solid #dadce0;
            color: #3c4043;
        }
        .cloudstyle-table tr:nth-child(even) {
            background: #fafafa;
        }
        .cloudstyle-badge-success {
            background: #e6f4ea;
            color: #137333;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            display: inline-block;
        }
        .cloudstyle-seal-wrapper {
            margin-top: 40px;
            padding-top: 24px;
            border-top: 1px solid #dadce0;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }
        .cloudstyle-seal-box {
            border: 2px dashed #1a73e8;
            padding: 14px 20px;
            border-radius: 8px;
            color: #1a73e8;
            text-align: center;
            background: rgba(26, 115, 232, 0.04);
        }
        .cloudstyle-seal-tag {
            font-family: 'Google Sans', sans-serif;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }
        .cloudstyle-seal-hash {
            font-family: 'Roboto Mono', monospace;
            font-size: 10.5px;
            margin-top: 4px;
            color: #5f6368;
        }
        .cloudstyle-footer-block {
            margin-top: 40px;
            padding-top: 16px;
            border-top: 1px solid #dadce0;
            font-size: 11.5px;
            color: #80868b;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* View 6: Relatório Executivo */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
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
        .report-brand-sec { display: flex; align-items: center; gap: 16px; }
        .report-title-meta h1 { font-size: 22px; font-weight: 700; color: #111827; margin-bottom: 4px; }
        .report-title-meta .sec-subtitle { font-size: 12px; font-weight: 600; color: #1a73e8; text-transform: uppercase; letter-spacing: 0.8px; }
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

        
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        /* Agentic Live Alert Banner & Industry Templates */
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    
        /* ------------------------------------------------------------------ */
        .agentic-alert-banner {
            background: linear-gradient(90deg, rgba(234, 67, 53, 0.15) 0%, rgba(251, 188, 4, 0.12) 100%);
            border: 1px solid rgba(234, 67, 53, 0.4);
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            box-shadow: 0 4px 20px rgba(234, 67, 53, 0.15);
            animation: pulse-border 2.5s infinite;
        }
        @keyframes pulse-border {
            0%, 100% { border-color: rgba(234, 67, 53, 0.4); }
            50% { border-color: rgba(251, 188, 4, 0.8); }
        }
        .alert-left-group {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
        }
        .alert-icon-wrap {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: rgba(234, 67, 53, 0.2);
            color: #f28b82;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .alert-content-wrap {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .alert-tagline {
            font-size: 11px;
            font-weight: 700;
            color: #f28b82;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .alert-headline {
            font-size: 13.5px;
            font-weight: 600;
            color: var(--text-primary);
        }
        .alert-desc {
            font-size: 12px;
            color: #d1d5db;
        }
        .alert-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }
        .btn-alert-diag {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-primary);
            border: 1px solid var(--border-subtle);
            padding: 7px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-alert-diag:hover { background: rgba(255, 255, 255, 0.15); }
        .btn-alert-update {
            background: linear-gradient(135deg, #34a853 0%, #1e8e3e 100%);
            color: #ffffff;
            border: none;
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 8px rgba(52, 168, 83, 0.3);
            transition: var(--transition-smooth);
        }
        .btn-alert-update:hover {
            box-shadow: 0 4px 12px rgba(52, 168, 83, 0.5);
            filter: brightness(1.1);
        }

        /* Industry Suggestion Cards in Left Drawer */
        .drawer-suggestions-box {
            background: var(--bg-canvas);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .drawer-suggestions-title {
            font-size: 12px;
            font-weight: 600;
            color: var(--gcp-blue);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .template-pills-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .btn-template-pill {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 5px 10px;
            border-radius: 16px;
            font-size: 11.5px;
            cursor: pointer;
            transition: var(--transition-smooth);
        }
        .btn-template-pill:hover {
            border-color: var(--gcp-blue);
            color: var(--gcp-blue);
            background: rgba(138, 180, 248, 0.08);
        }
        .btn-ai-recommend {
            width: 100%;
            background: linear-gradient(135deg, rgba(66, 133, 244, 0.15) 0%, rgba(138, 180, 248, 0.15) 100%);
            border: 1px solid rgba(138, 180, 248, 0.35);
            color: var(--gcp-blue);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: var(--transition-smooth);
        }
        .btn-ai-recommend:hover {
            background: var(--gcp-blue);
            color: #ffffff;
        }

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


        /* Minimalist Auditor Health & Compliance Dashboard */
        .auditor-health-dash {
            display: grid;
            grid-template-columns: 290px 1fr;
            gap: 14px;
            width: 100%;
            max-width: 1040px;
            margin: 4px auto 0 auto;
            text-align: left;
            animation: fadeIn 0.25s ease;
        }

        @media (max-width: 860px) {
            .auditor-health-dash {
                grid-template-columns: 1fr;
            }
        }

        .health-card {
            background: #1e1f20;
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 16px 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        }

        .health-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .health-card-title {
            font-size: 12.5px;
            font-weight: 600;
            color: #e8eaed;
            letter-spacing: 0.3px;
        }

        .health-card-badge {
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 6px;
            background: rgba(138, 180, 248, 0.12);
            color: var(--gcp-blue);
            border: 1px solid rgba(138, 180, 248, 0.25);
        }

        /* Minimal Speedometer */
        .speedometer-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 2px 0;
        }

        .speedometer-svg {
            width: 190px;
            height: 105px;
            overflow: visible;
        }

        .gauge-bg {
            fill: none;
            stroke: #2d2f31;
            stroke-width: 12;
            stroke-linecap: round;
        }

        .gauge-meter {
            fill: none;
            stroke: url(#speedoGradient);
            stroke-width: 12;
            stroke-linecap: round;
            stroke-dasharray: 236;
            stroke-dashoffset: 8;
            transition: stroke-dashoffset 1s ease-in-out;
        }

        .speedo-center-val {
            font-size: 28px;
            font-weight: 700;
            fill: #ffffff;
            font-family: var(--font-headline);
        }

        .speedo-center-lbl {
            font-size: 10px;
            font-weight: 600;
            fill: #81c995;
            letter-spacing: 0.6px;
            font-family: var(--font-headline);
        }

        /* Minimal 2x2 Domain Grid */
        .compliance-domains-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px 18px;
        }

        @media (max-width: 560px) {
            .compliance-domains-grid {
                grid-template-columns: 1fr;
            }
        }

        .domain-item {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .domain-top {
            display: flex;
            justify-content: space-between;
            font-size: 11.5px;
            color: #c4c7c5;
        }

        .domain-pct {
            font-weight: 600;
            font-size: 11px;
        }

        .val-green { color: #81c995; }
        .val-blue { color: #8ab4f8; }
        .val-yellow { color: #fdd663; }

        .domain-bar {
            width: 100%;
            height: 5px;
            background: #2d2f31;
            border-radius: 3px;
            overflow: hidden;
        }

        .domain-fill {
            height: 100%;
            border-radius: 3px;
        }

        .bg-green { background: #81c995; }
        .bg-blue { background: #8ab4f8; }
        .bg-yellow { background: #fdd663; }

        .compliance-footer-note {
            font-size: 10.5px;
            color: var(--text-tertiary);
            padding-top: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .btn-news-source-link {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(138, 180, 248, 0.12);
            color: var(--gcp-blue);
            border: 1px solid rgba(138, 180, 248, 0.3);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .btn-news-source-link:hover {
            background: rgba(138, 180, 248, 0.22);
            border-color: var(--gcp-blue);
            color: #ffffff;
            transform: translateY(-1px);
        }

        .news-source-link {
            font-size: 11px;
            color: var(--gcp-blue);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 7px;
            border-radius: 4px;
            background: rgba(138, 180, 248, 0.08);
            border: 1px solid rgba(138, 180, 248, 0.2);
            transition: all 0.2s;
        }

        .news-source-link:hover {
            background: rgba(138, 180, 248, 0.25);
            color: #ffffff;
            border-color: var(--gcp-blue);
            text-decoration: none;
        }

        @media print {
            body { background: #ffffff !important; color: #000000 !important; overflow: visible !important; }
            .sidebar, .top-navbar, .chat-input-wrapper, .modal-overlay, .matrix-toolbar, .btn-confirm, .btn-action-primary { display: none !important; }
            .main-container { height: auto !important; }
            .views-viewport { overflow: visible !important; }
            .view-pane { display: none !important; }
            #view-report-exec.active, #view-report-tech.active { display: block !important; padding: 0 !important; }
            .report-preview-sheet { box-shadow: none !important; border-radius: 0 !important; max-width: 100% !important; padding: 0 !important; }
        }
    
        /* =========================================================================
           Agentic GRC Hero Work & Regulatory RSS News Feed Styles (Spacious & Clean)
           ========================================================================= */
        .gemini-hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin: 0 auto;
            padding: 30px 20px 50px 20px;
            width: 100%;
            max-width: 1100px;
            min-height: calc(100vh - 120px);
            gap: 20px;
            animation: fadeIn 0.25s ease;
        }

        .hero-work-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }


        .hero-work-title {
            font-size: 40px;
            font-weight: 500;
            letter-spacing: -0.8px;
            color: #ffffff;
            margin: 0;
            line-height: 1.2;
        }

        .hero-work-subtitle {
            font-size: 13.5px;
            color: var(--text-secondary);
            max-width: 650px;
            line-height: 1.5;
            margin: 0;
        }

        /* Spacious Central Input Container (Spacious, Not Polluted) */
        .hero-input-container {
            width: 100%;
            max-width: 1080px;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 auto;
        }

        .hero-input-card {
            background: #1e1f20;
            border: 1px solid #3c4043;
            border-radius: 24px;
            padding: 16px 22px 14px 22px;
            width: 100%;
            box-shadow: 0 10px 32px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: border-color 0.2s, box-shadow 0.2s;
            text-align: left;
        }

        .hero-input-card:focus-within {
            border-color: #8ab4f8;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7), 0 0 0 1px #8ab4f8;
        }

        .hero-textarea {
            background: transparent;
            border: none;
            outline: none;
            width: 100%;
            color: #e8eaed;
            font-size: 16px;
            line-height: 1.55;
            resize: none;
            font-family: inherit;
            min-height: 52px;
        }

        .hero-textarea::placeholder {
            color: #9aa0a6;
        }

        .hero-input-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding-top: 10px;
        }

        .hero-input-left {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        .btn-hero-tool {
            background: transparent;
            border: none;
            color: #9aa0a6;
            border-radius: 50%;
            width: 34px;
            height: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-hero-tool:hover {
            background: #282a2c;
            color: #e8eaed;
        }

        .hero-input-right {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        /* Model Picker Dropdown */
        .model-picker-wrapper {
            position: relative;
        }

        .btn-model-picker {
            background: #282a2c;
            border: 1px solid #3c4043;
            border-radius: 18px;
            padding: 6px 14px;
            font-size: 13px;
            color: #e8eaed;
            display: flex;
            align-items: center;
            gap: 7px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }

        .btn-model-picker:hover {
            background: #35373a;
            border-color: #5f6368;
        }

        .model-picker-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #4285f4;
            box-shadow: 0 0 8px #4285f4;
        }

        .model-picker-menu {
            position: absolute;
            bottom: calc(100% + 8px);
            right: 0;
            background: #1e1f20;
            border: 1px solid #3c4043;
            border-radius: 14px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65);
            padding: 8px;
            width: 310px;
            display: none;
            flex-direction: column;
            gap: 4px;
            z-index: 100;
            animation: fadeIn 0.2s ease;
        }

        .model-picker-menu.show {
            display: flex;
        }

        .model-option {
            padding: 10px 12px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            gap: 3px;
            text-align: left;
        }

        .model-option:hover {
            background: #2d2f31;
        }

        .model-option.selected {
            background: rgba(66, 133, 244, 0.12);
            border: 1px solid rgba(66, 133, 244, 0.35);
        }

        .model-opt-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
            font-size: 13.5px;
            color: #e8eaed;
        }

        .model-opt-desc {
            font-size: 11.5px;
            color: #9aa0a6;
            line-height: 1.35;
            padding-left: 15px;
        }

        .model-tag-rec {
            background: rgba(129, 201, 149, 0.15);
            color: #81c995;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 6px;
            font-weight: 600;
            margin-left: auto;
        }

        .model-tag-new {
            background: rgba(197, 138, 249, 0.15);
            color: #c58af9;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 6px;
            font-weight: 600;
            margin-left: auto;
        }

        /* Send Button */
        .btn-send-hero {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #3c4043;
            color: #ffffff;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .btn-send-hero:hover {
            background: #e8eaed;
            color: #131314;
            transform: scale(1.05);
        }

        /* Minimalist & Clean Suggestion Chips (1 Single Row of 5 Essentials) */
        .hero-quick-chips {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            max-width: 1080px;
            width: 100%;
            margin: 14px auto 0 auto;
        }

        .chip-item {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid #3c4043;
            border-radius: 20px;
            padding: 7px 15px;
            font-size: 12.5px;
            color: #bdc1c6;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 7px;
            white-space: nowrap;
            transition: all 0.2s ease;
        }

        .chip-item:hover {
            background: rgba(255, 255, 255, 0.09);
            border-color: #8ab4f8;
            color: #ffffff;
            transform: translateY(-1px);
        }

        .chip-icon {
            font-size: 13.5px;
        }

        /* Spacious Regulatory RSS News Feed Strip */
        .hero-news-section {
            max-width: 1080px;
            width: 100%;
            margin: 28px auto 8px auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .news-section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 4px;
        }

        .news-header-left {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .news-pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #ea4335;
            box-shadow: 0 0 8px #ea4335;
            animation: pulse 2s infinite;
        }

        .news-header-title {
            font-size: 13px;
            font-weight: 600;
            color: #9aa0a6;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .news-nav-buttons {
            display: flex;
            gap: 6px;
        }

        .btn-news-nav {
            background: #1e1f20;
            border: 1px solid #3c4043;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e8eaed;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 17px;
            line-height: 1;
        }

        .btn-news-nav:hover {
            background: #303134;
            border-color: #8ab4f8;
            color: #ffffff;
        }

        .news-carousel-track {
            display: flex;
            gap: 16px;
            overflow-x: auto;
            scroll-behavior: smooth;
            padding: 4px 2px 14px 2px;
            scrollbar-width: thin;
            scrollbar-color: var(--border-subtle) transparent;
        }

        .news-carousel-track::-webkit-scrollbar {
            height: 4px;
        }

        .news-carousel-track::-webkit-scrollbar-thumb {
            background: var(--border-subtle);
            border-radius: 4px;
        }

        /* Clean, Uncluttered News Card */
        .news-card {
            flex: 0 0 280px;
            background: #1e1f20;
            border: 1px solid #303134;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 9px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
        }

        .news-card:hover {
            border-color: #8ab4f8;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }

        .news-card-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .news-card-date {
            font-size: 10.5px;
            color: #9aa0a6;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .news-card-tag {
            font-size: 10px;
            font-weight: 600;
            padding: 2px 7px;
            border-radius: 4px;
        }

        .news-card-title {
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            line-height: 1.35;
        }

        .news-card-snippet {
            font-size: 12px;
            color: #9aa0a6;
            line-height: 1.45;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .news-card-footer {
            margin-top: auto;
            padding-top: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .news-action-link {
            font-size: 11.5px;
            color: #8ab4f8;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
        }

    
        /* Language Selector Pill */
        .lang-selector-group {
            display: inline-flex;
            align-items: center;
            gap: 2px;
            background: var(--bg-surface-hover);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 2px 6px;
            font-size: 11px;
            font-weight: 600;
            user-select: none;
        }
        .lang-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 3px 7px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            transition: all 0.15s ease;
            font-family: inherit;
        }
        .lang-btn:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }
        .lang-btn.active {
            background: #1a73e8;
            color: #ffffff !important;
            font-weight: 700;
        }
        .lang-divider {
            color: var(--border-subtle);
            font-size: 10px;
            user-select: none;
        }
</style>
</head>
<body>

    <!-- Left Sidebar -->
    <aside class="sidebar" id="appSidebar">
        <div class="sidebar-top">
            <!-- Brand Header: Google Cloud Icon (No border) & Title -->
            <div class="brand-header">
                <a href="#" class="brand-left" onclick="switchView('view-chat')" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
                    <img src="data:image/png;base64,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" alt="Google Cloud" width="32" height="32" style="object-fit: contain; border: none; background: transparent; display: block; flex-shrink: 0;">
                    <div class="brand-text-col">
                        <span class="brand-title" style="font-size: 14.5px; font-weight: 600; color: var(--text-primary); display: block; line-height: 1.2;">Agentic GRC Auditor</span>
                        <span class="brand-subtitle-badge" style="font-size: 10px; font-weight: 600; color: #8ab4f8; text-transform: uppercase; letter-spacing: 0.5px;">Google Cloud Security</span>
                    </div>
                </a>
                <button class="btn-collapse" onclick="toggleSidebar()" title="Recolher menu lateral">
                    <svg class="icon-svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <line x1="9" y1="3" x2="9" y2="21"/>
                    </svg>
                </button>
            </div>

            <!-- Top Action Button (Gemini style) -->
            <div style="padding: 0 0 8px 0;">
                <button class="btn-new-audit" id="navNewChat" onclick="startNewConversation()">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" style="flex-shrink: 0;">
                        <line x1="12" y1="5" x2="12" y2="19"/>
                        <line x1="5" y1="12" x2="19" y2="12"/>
                    </svg>
                    <span class="label" data-i18n="nav_new_chat">Nova conversa</span>
                </button>
            </div>

            <!-- Merged Unified Navigation (No duplicates, pure borderless icons) -->
            <div class="agent-list">
                <button class="agent-item" id="agentBtnGrcAuditor" onclick="selectAuditorTab()">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar" style="color: #4285f4;">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <path d="M12 2L20 5.8V11.5C20 16.5 16.6 20.8 12 22C7.4 20.8 4 16.5 4 11.5V5.8L12 2Z"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_lead_auditor">Agentic GRC Auditor</span>
                    </div>
                    <span class="agent-pin" title="Auditor Líder" style="color: var(--gcp-blue); font-size: 11px;">●</span>
                </button>

                <button class="agent-item" id="agentBtnPhases" onclick="switchView('view-phases')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_phases">Scan por Fases</span>
                    </div>
                </button>

                <button class="agent-item" id="agentBtnMatrix" onclick="switchView('view-matrix')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <line x1="16" y1="13" x2="8" y2="13"/>
                                <line x1="16" y1="17" x2="8" y2="17"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_matrix">Matriz ISO 27001 & SoA</span>
                    </div>
                </button>

                <button class="agent-item" id="agentBtnConnectors" onclick="switchView('view-connectors')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <circle cx="18" cy="5" r="3"/>
                                <circle cx="6" cy="12" r="3"/>
                                <circle cx="18" cy="19" r="3"/>
                                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
                            </svg>
                        </div>
                        <span class="agent-name">Subagentes & Zero-Copy</span>
                    </div>
                </button>

                <button class="agent-item" id="agentBtnScorecard" onclick="switchView('view-scorecard')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_scorecard">Scorecard & Evidências</span>
                    </div>
                </button>

                <button class="agent-item" id="agentBtnReport" onclick="openExecutiveReport()">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar" style="color: var(--gcp-blue);">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <line x1="12" y1="18" x2="12" y2="12"/>
                                <line x1="9" y1="15" x2="15" y2="15"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_exec_report">Dossiê Executivo</span>
                    </div>
                </button>

                <button class="agent-item" id="agentBtnTechReport" onclick="openTechnicalReport()">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar" style="color: #ea4335;">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8">
                                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_tech_report">Relatório Técnico (Auditoria Externa)</span>
                    </div>
                </button>

                <button class="agent-item" id="agentBtnFinops" onclick="switchView('view-finops')">
                    <div class="agent-left-wrap">
                        <div class="agent-avatar" style="color: var(--gcp-green);">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="12" y1="1" x2="12" y2="23"/>
                                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                            </svg>
                        </div>
                        <span class="agent-name" data-i18n="nav_finops">FinOps & Custos de IA</span>
                    </div>
                </button>
            </div>

            <!-- Subagentes Customizados Section -->
            <div class="section-header" style="margin-top: 14px;">
                <span>Subagentes Customizados</span>
            </div>

            <button class="btn-create-subagent-clean" id="agentBtnCreate" onclick="openCreateSubagentModal()">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2">
                    <line x1="12" y1="5" x2="12" y2="19"/>
                    <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                <span>+ Criar Subagente</span>
            </button>

            <div id="sidebarCustomAgentsList" style="margin-top: 4px; display: flex; flex-direction: column; gap: 2px;"></div>

            <!-- Histórico Recente -->
            <div class="section-header" style="margin-top: 14px;">
                <span>Histórico de Auditorias</span>
            </div>
            <div class="recent-list">
                <div class="recent-item" onclick="promptPreFill('Gerar parecer executivo formal de conformidade para agentic-grc-cd06')">Parecer ISO 27001 - agentic-grc-cd06</div>
                <div class="recent-item" onclick="promptPreFill('Auditar conformidade do Cloud KMS e rotação de chaves HSM (A.8.24)')">Auditoria Criptografia KMS - A.8.24</div>
                <div class="recent-item" onclick="promptPreFill('Verificar perímetros VPC Service Controls e proteção contra exfiltração')">Inspeção VPC-SC & DLP</div>
            </div>
        </div>

        <div class="sidebar-bottom">
            <!-- Escopo de Projetos Selecionados (GCP Organization Dropdown) -->
            <div class="scope-box" id="scopeContainer">
                <div class="scope-header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                    <div style="display: flex; align-items: center; gap: 6px; overflow: hidden;">
                        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--gcp-blue); flex-shrink: 0;">
                            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                        </svg>
                        <span class="scope-label" style="font-size: 11px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">Organização GCP</span>
                    </div>
                    <button class="btn-org-dropdown-toggle" id="btnOrgDropdownToggle" onclick="toggleOrgScopeDropdown()" title="Projetos da Organização GCP" style="background: rgba(138, 180, 248, 0.12); border: 1px solid rgba(138, 180, 248, 0.3); color: var(--gcp-blue); border-radius: 6px; padding: 2px 7px; font-size: 11px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: var(--transition-smooth);">
                        <span id="orgScopeBadgeText">3/10 ativos</span>
                        <svg id="orgDropdownChevron" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" style="transition: transform 0.2s ease;">
                            <polyline points="6 9 12 15 18 9"/>
                        </svg>
                    </button>
                </div>

                <!-- Dropdown Retrátil da Organização GCP -->
                <div class="org-scope-dropdown" id="orgScopeDropdown" style="display: none; background: var(--bg-canvas); border: 1px solid var(--border-focus); border-radius: 8px; padding: 8px; margin-bottom: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.5);">
                    <div style="display: flex; align-items: center; justify-content: space-between; font-size: 10px; color: var(--text-tertiary); margin-bottom: 6px;">
                        <span>Altostrat Global Org (108928374619)</span>
                        <span style="color: var(--gcp-green); font-weight: 600;">Nível Org</span>
                    </div>
                    <input type="text" id="orgSearchInput" placeholder="Filtrar projetos da Org..." oninput="filterOrgDropdown(this.value)" style="width: 100%; background: var(--bg-input); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 4px 8px; font-size: 11px; color: var(--text-primary); margin-bottom: 6px; outline: none; box-sizing: border-box;">
                    
                    <div style="display: flex; gap: 4px; margin-bottom: 6px;">
                        <button onclick="selectAllOrgProjects()" style="flex: 1; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 4px; font-size: 9.5px; color: var(--text-secondary); padding: 3px 4px; cursor: pointer;">Marcar Todos</button>
                        <button onclick="selectProdOnlyOrgProjects()" style="flex: 1; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 4px; font-size: 9.5px; color: var(--text-secondary); padding: 3px 4px; cursor: pointer;">Apenas Prod</button>
                        <button onclick="openProjectModal()" style="background: rgba(138, 180, 248, 0.1); border: 1px solid rgba(138, 180, 248, 0.25); border-radius: 4px; font-size: 9.5px; color: var(--gcp-blue); padding: 3px 6px; cursor: pointer;">+ Manual</button>
                    </div>

                    <div class="org-dropdown-list" id="orgDropdownItemsList" style="display: flex; flex-direction: column; gap: 4px; max-height: 150px; overflow-y: auto;">
                        <!-- Dynamically populated with all organization projects -->
                    </div>
                </div>

                <!-- Lista de projetos ativos no escopo -->
                <div class="scope-projects-list" id="scopeProjectsList" style="display: flex; flex-direction: column; gap: 5px; max-height: 110px; overflow-y: auto;">
                    <div class="project-pill-item">
                        <div class="project-pill-left">
                            <input type="checkbox" class="project-checkbox" checked onchange="toggleProjectSelection('agentic-grc-cd06', this.checked)">
                            <span class="project-id-text" title="agentic-grc-cd06">agentic-grc-cd06</span>
                        </div>
                        <span class="env-badge">PRODUCTION</span>
                    </div>
                    <div class="project-pill-item">
                        <div class="project-pill-left">
                            <input type="checkbox" class="project-checkbox" checked onchange="toggleProjectSelection('agentic-grc-staging', this.checked)">
                            <span class="project-id-text" title="agentic-grc-staging">agentic-grc-staging</span>
                        </div>
                        <span class="env-badge">STAGING</span>
                    </div>
                    <div class="project-pill-item">
                        <div class="project-pill-left">
                            <input type="checkbox" class="project-checkbox" checked onchange="toggleProjectSelection('agentic-grc-data-lake', this.checked)">
                            <span class="project-id-text" title="agentic-grc-data-lake">agentic-grc-data-lake</span>
                        </div>
                        <span class="env-badge">ANALYTICS</span>
                    </div>
                </div>
                <div class="scope-value" id="currentScopeLabel" style="display: none;">agentic-grc-cd06 (+2 ativos)</div>
            </div>

            <!-- Perfil do Auditor: Google Cloud Wordmark (sem a nuvem) & Credentials -->
            <div class="user-meta" onclick="switchView('view-scorecard')" title="Clique para ver Scorecard de Conformidade" style="cursor: pointer; padding: 10px 4px 4px 4px; display: flex; flex-direction: column; gap: 4px; border: none; background: transparent;">
                <img src="data:image/png;base64,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" alt="Google Cloud" style="height: 18px; width: auto; max-width: 140px; object-fit: contain; align-self: flex-start; border: none !important; outline: none !important; background: transparent !important; display: block; margin-bottom: 2px;">
                <div class="user-info" style="display: flex; flex-direction: column; gap: 2px;">
                    <span class="user-name" style="font-size: 11px; font-weight: 500; color: var(--text-secondary); line-height: 1.35; white-space: normal;">Google Cloud Security Lead Auditor</span>
                    <span class="user-role" style="font-size: 9.5px; color: var(--text-tertiary); line-height: 1.25;">(SPIFFE Assinado)</span>
                </div>
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
                <span class="top-active-agent" id="topActiveTitle" data-i18n="top_active_agent">Chatbot Auditor</span>
                <span style="color: var(--text-tertiary)">•</span>
                <span style="color: var(--gcp-blue); font-size: 13px;" id="topProjectCountBadge" data-i18n="top_project_count">1 projeto ativo</span>
            </div>

            <div class="top-right-actions">
                <div class="top-status-indicator">
                    <span class="status-dot"></span>
                    <span data-i18n="status_indicator">Vertex AI gemini-2.5-flash (Google Cloud Security Certified)</span>
                </div>

                <!-- Language Selector Pill -->
                <div class="lang-selector-group" id="langSelectorGroup" title="Idioma / Language / Idioma">
                    <button class="lang-btn active" id="langBtnPt" onclick="setLanguage('pt')">PT</button>
                    <span class="lang-divider">|</span>
                    <button class="lang-btn" id="langBtnEn" onclick="setLanguage('en')">EN</button>
                    <span class="lang-divider">|</span>
                    <button class="lang-btn" id="langBtnEs" onclick="setLanguage('es')">ES</button>
                </div>

                <div class="dropdown" id="exportDropdown">
                    <button class="btn-action-primary" onclick="toggleExportMenu()">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                        <span data-i18n="export_btn">Exportar Relatório</span>
                    </button>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="javascript:void(0)" onclick="openExecutiveReport()">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                                <line x1="16" y1="13" x2="8" y2="13"/>
                                <line x1="16" y1="17" x2="8" y2="17"/>
                            </svg>
                            <span data-i18n="export_exec">Visualizar Dossiê Executivo</span>
                        </a>
                        <a class="dropdown-item" href="javascript:void(0)" onclick="openTechnicalReport()">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                            </svg>
                            <span data-i18n="export_tech">Visualizar Relatório Técnico (Auditoria Externa)</span>
                        </a>
                        <a class="dropdown-item" href="javascript:void(0)" onclick="printExecutiveReport()">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <polyline points="6 9 6 2 18 2 18 9"/>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                                <rect x="6" y="14" width="12" height="8"/>
                            </svg>
                            <span data-i18n="export_print">Imprimir / Salvar PDF Oficial</span>
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
                    
                    <!-- Banner de Alerta Agêntico Proativo (Vertex AI Gemini) -->
                    <div class="agentic-alert-banner" id="agenticAlertBanner" style="display: none;">
                        <div class="alert-left-group">
                            <div class="alert-icon-wrap">
                                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                                    <line x1="12" y1="9" x2="12" y2="13"/>
                                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                                </svg>
                            </div>
                            <div class="alert-content-wrap">
                                <span class="alert-tagline">
                                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #f28b82; display: inline-block;"></span>
                                    Alerta Agêntico em Tempo Real • Vertex AI
                                </span>
                                <div class="alert-headline" id="alertHeadline">Desvio Crítico no Controle A.8.24 (Cloud KMS HSM)</div>
                                <div class="alert-desc" id="alertDesc">Chave 'app-secrets-master' configurada com ciclo de 180 dias (limite: 90 dias). Risco de não-conformidade.</div>
                            </div>
                        </div>
                        <div class="alert-actions">
                            <button class="btn-alert-diag" onclick="showDeviationDiagnostic()">Ver Diagnóstico</button>
                            <button class="btn-alert-update" onclick="triggerAutonomousPolicyUpdate()">
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4">
                                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                                </svg>
                                Atualizar Política com IA (Zero-Touch)
                            </button>
                        </div>
                    </div>

                    <div class="chat-messages-area" id="chatArea">
                        <div class="gemini-hero" id="geminiHero">
                            <!-- Clean Header (Spacious, No distractions) -->
                            <div class="hero-work-header">
                                <h1 class="hero-work-title" data-i18n="hero_work_title">Vamos trabalhar!</h1>
                                <p class="hero-work-subtitle" data-i18n="hero_work_subtitle">
                                    Auditoria contínua autônoma e governança para Google Cloud & ISO/IEC 27001:2022
                                </p>
                            </div>

                            <!-- Wide & Spacious Main Input Box -->
                            <div class="hero-input-container">
                                <div class="hero-input-card">
                                    <textarea id="chatInputHero" class="hero-textarea" placeholder="O que você gostaria de auditar hoje? (ex.: ISO 27001, Cloud KMS, VPC-SC, FinOps)" data-i18n-placeholder="hero_placeholder" rows="2" onkeydown="handleHeroKey(event)" oninput="handleHeroInput(this)"></textarea>
                                    
                                    <div class="hero-input-controls">
                                        <div class="hero-input-left">
                                            <button type="button" class="btn-hero-tool" onclick="openUploadModal()" title="Anexar arquivo de infraestrutura / IaC">
                                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                                                    <line x1="12" y1="5" x2="12" y2="19"/>
                                                    <line x1="5" y1="12" x2="19" y2="12"/>
                                                </svg>
                                            </button>
                                            <button type="button" class="btn-hero-tool" onclick="openStorageModal()" title="Conectar repositório Zero-Copy (Drive / SharePoint / Jira)">
                                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                                                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                                                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                                                </svg>
                                            </button>
                                        </div>

                                        <div class="hero-input-right">
                                            <!-- Model Selector Dropdown -->
                                            <div class="model-picker-wrapper">
                                                <button type="button" class="btn-model-picker" id="btnModelPicker" onclick="toggleModelDropdown(event)">
                                                    <span class="model-picker-dot" id="dotActiveModel"></span>
                                                    <span id="lblModelPicker">Automático</span>
                                                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                                                        <path d="M7 10l5 5 5-5z"/>
                                                    </svg>
                                                </button>
                                                <div class="model-picker-menu" id="modelPickerMenu">
                                                    <div class="model-option selected" data-model="gemini-auto" onclick="selectModel('gemini-auto', 'Automático')">
                                                        <div class="model-opt-title">
                                                            <span class="model-picker-dot" style="background:#4285f4; box-shadow: 0 0 6px #4285f4;"></span>
                                                            <span>Automático</span>
                                                            <span class="model-tag-rec">Recomendado</span>
                                                        </div>
                                                        <div class="model-opt-desc">Roteamento autônomo Gemini 2.5 com otimização FinOps</div>
                                                    </div>
                                                    <div class="model-option" data-model="gemini-2.5-pro" onclick="selectModel('gemini-2.5-pro', 'Gemini 2.5 Pro')">
                                                        <div class="model-opt-title">
                                                            <span class="model-picker-dot" style="background:#8ab4f8; box-shadow: 0 0 6px #8ab4f8;"></span>
                                                            <span>Gemini 2.5 Pro</span>
                                                        </div>
                                                        <div class="model-opt-desc">Auditor Líder • Raciocínio normativo profundo & Pareceres</div>
                                                    </div>
                                                    <div class="model-option" data-model="gemini-2.5-flash" onclick="selectModel('gemini-2.5-flash', 'Gemini 2.5 Flash')">
                                                        <div class="model-opt-title">
                                                            <span class="model-picker-dot" style="background:#81c995; box-shadow: 0 0 6px #81c995;"></span>
                                                            <span>Gemini 2.5 Flash</span>
                                                        </div>
                                                        <div class="model-opt-desc">Alta velocidade • Triagem de evidências e telemetria GCP</div>
                                                    </div>
                                                    <div class="model-option" data-model="gemini-3.5-flash" onclick="selectModel('gemini-3.5-flash', 'Gemini 3.5 Flash')">
                                                        <div class="model-opt-title">
                                                            <span class="model-picker-dot" style="background:#c58af9; box-shadow: 0 0 6px #c58af9;"></span>
                                                            <span>Gemini 3.5 Flash</span>
                                                            <span class="model-tag-new">Novo</span>
                                                        </div>
                                                        <div class="model-opt-desc">Nova geração • Context Caching de 1M tokens para varreduras contínuas</div>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Submit Upward Arrow Button -->
                                            <button type="button" class="btn-send-hero" id="btnSendHero" onclick="sendChatMessageFromHero()" title="Enviar para o Auditor Líder">
                                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.6">
                                                    <line x1="12" y1="19" x2="12" y2="5"/>
                                                    <polyline points="5 12 12 5 19 12"/>
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Dynamic & Always-Altering Suggestion Chips (Visible in Agentic GRC Auditor) -->
                            <div class="hero-quick-chips" id="heroQuickChips" style="display: none;">
                                <!-- Populated dynamically by shuffleDynamicSuggestions() when Auditor tab is clicked -->
                            </div>

                            <!-- Agentic GRC Auditor Health Dash (Speedometer & Compliance Status) -->
                            <div class="auditor-health-dash" id="auditorHealthDash" style="display: none;">
                                <!-- Minimal Card 1: Velocímetro de Saúde -->
                                <div class="health-card">
                                    <div class="health-card-header">
                                        <div class="health-card-title" data-i18n="health_title">Saúde do Ambiente GCP</div>
                                        <span class="health-card-badge" data-i18n="health_badge">Telemetria Ativa</span>
                                    </div>
                                    <div class="speedometer-wrap">
                                        <svg class="speedometer-svg" viewBox="0 0 200 110">
                                            <defs>
                                                <linearGradient id="speedoGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                                    <stop offset="0%" stop-color="#4285f4"/>
                                                    <stop offset="50%" stop-color="#8ab4f8"/>
                                                    <stop offset="100%" stop-color="#81c995"/>
                                                </linearGradient>
                                            </defs>
                                            <path class="gauge-bg" d="M 25 95 A 75 75 0 0 1 175 95" />
                                            <path class="gauge-meter" d="M 25 95 A 75 75 0 0 1 175 95" style="stroke-dasharray: 236; stroke-dashoffset: 8;" />
                                            <text x="100" y="80" class="speedo-center-val" text-anchor="middle">96.4%</text>
                                            <text x="100" y="98" class="speedo-center-lbl" text-anchor="middle">POSTURA RESILIENTE</text>
                                        </svg>
                                    </div>
                                </div>

                                <!-- Minimal Card 2: Status ISO/IEC 27001 -->
                                <div class="health-card">
                                    <div class="health-card-header">
                                        <div class="health-card-title">Conformidade ISO/IEC 27001:2022</div>
                                        <span class="health-card-badge">89 / 93 Controles (95.7%)</span>
                                    </div>

                                    <div class="compliance-domains-grid">
                                        <div class="domain-item">
                                            <div class="domain-top">
                                                <span>Organizacional (A.5)</span>
                                                <span class="domain-pct val-green">100%</span>
                                            </div>
                                            <div class="domain-bar"><div class="domain-fill bg-green" style="width: 100%;"></div></div>
                                        </div>
                                        <div class="domain-item">
                                            <div class="domain-top">
                                                <span>Pessoas (A.6)</span>
                                                <span class="domain-pct val-green">100%</span>
                                            </div>
                                            <div class="domain-bar"><div class="domain-fill bg-green" style="width: 100%;"></div></div>
                                        </div>
                                        <div class="domain-item">
                                            <div class="domain-top">
                                                <span>Físico & Clima (A.7)</span>
                                                <span class="domain-pct val-blue">93%</span>
                                            </div>
                                            <div class="domain-bar"><div class="domain-fill bg-blue" style="width: 93%;"></div></div>
                                        </div>
                                        <div class="domain-item">
                                            <div class="domain-top">
                                                <span>Tecnológico (A.8)</span>
                                                <span class="domain-pct val-yellow">91%</span>
                                            </div>
                                            <div class="domain-bar"><div class="domain-fill bg-yellow" style="width: 91%;"></div></div>
                                        </div>
                                    </div>

                                    <div class="compliance-footer-note">
                                        <span>Grafo SHA-256 Validado</span>
                                        <span>Zero-Touch Ativo</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Clean Regulatory RSS News Feed Strip (Visible on Initial Screen & Nova Conversa) -->
                            <div class="hero-news-section" id="heroNewsSection">
                                <div class="news-section-header">
                                    <div class="news-header-left">
                                        <span class="news-pulse-dot"></span>
                                        <span class="news-header-title">Novidades & Atualizações Regulatórias (RSS Feed)</span>
                                    </div>
                                    <div class="news-nav-buttons">
                                        <button class="btn-news-nav" onclick="scrollNewsCarousel(-1)" title="Anterior">‹</button>
                                        <button class="btn-news-nav" onclick="scrollNewsCarousel(1)" title="Próximo">›</button>
                                    </div>
                                </div>

                                <div class="news-carousel-track" id="newsCarouselTrack">
                                    <!-- Card 1: ISO 27001 Amd 1:2024 -->
                                    <div class="news-card" onclick="openNewsModal('iso-amd-1-2024')">
                                        <div class="news-card-meta">
                                            <span class="news-card-date">Setembro 2026</span>
                                            <span class="news-card-tag" style="background: rgba(129,201,149,0.15); color: #81c995;">ISO 27001</span>
                                        </div>
                                        <div class="news-card-title">Emenda Climática ISO 27001 Obrigatória</div>
                                        <div class="news-card-snippet">
                                            A IAF determinou que auditorias devem checar se os riscos de mudanças climáticas foram avaliados nas cláusulas 4.1 e 4.2 do SGSI.
                                        </div>
                                        <div class="news-card-footer" style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="news-action-link">Ler notícia completa ➔</span>
                                            <a class="news-source-link" href="https://www.iso.org/standard/88435.html" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="Abrir portal oficial ISO">Fonte oficial ↗</a>
                                        </div>
                                    </div>

                                    <!-- Card 2: NIST CSF 2.0 -->
                                    <div class="news-card" onclick="openNewsModal('nist-csf-2-0')">
                                        <div class="news-card-meta">
                                            <span class="news-card-date">Agosto 2026</span>
                                            <span class="news-card-tag" style="background: rgba(138,180,248,0.15); color: #8ab4f8;">NIST CSF 2.0</span>
                                        </div>
                                        <div class="news-card-title">NIST CSF 2.0: Nova Função Governança</div>
                                        <div class="news-card-snippet">
                                            A função GOVERN estabelece alinhamento formal de cibersegurança e apetite a risco integrados à diretoria executiva.
                                        </div>
                                        <div class="news-card-footer" style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="news-action-link">Ler notícia completa ➔</span>
                                            <a class="news-source-link" href="https://www.nist.gov/cyberframework" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="Abrir portal oficial NIST">Fonte oficial ↗</a>
                                        </div>
                                    </div>

                                    <!-- Card 3: PCI-DSS v4.0.1 -->
                                    <div class="news-card" onclick="openNewsModal('pci-dss-v4')">
                                        <div class="news-card-meta">
                                            <span class="news-card-date">Julho 2026</span>
                                            <span class="news-card-tag" style="background: rgba(197,138,249,0.15); color: #c58af9;">PCI-DSS v4.0</span>
                                        </div>
                                        <div class="news-card-title">Transição Mandatória PCI-DSS v4.0 em Nuvem</div>
                                        <div class="news-card-snippet">
                                            Exigências reforçadas para perímetros de dados de titulares de cartões (CDE) e gerenciamento de chaves KMS HSM.
                                        </div>
                                        <div class="news-card-footer" style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="news-action-link">Ler notícia completa ➔</span>
                                            <a class="news-source-link" href="https://www.pcisecuritystandards.org/document_library/?category=pcidss&document=pci_dss" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="Abrir portal oficial PCI">Fonte oficial ↗</a>
                                        </div>
                                    </div>

                                    <!-- Card 4: ANPD & LGPD Nuvem -->
                                    <div class="news-card" onclick="openNewsModal('anpd-lgpd')">
                                        <div class="news-card-meta">
                                            <span class="news-card-date">Junho 2026</span>
                                            <span class="news-card-tag" style="background: rgba(253,214,99,0.15); color: #fdd663;">ANPD / LGPD</span>
                                        </div>
                                        <div class="news-card-title">Guia de Segurança da ANPD para Nuvem</div>
                                        <div class="news-card-snippet">
                                            Diretrizes técnicas para uso de Cloud DLP, mascaramento de PII e elaboração de ROPA e relatórios de impacto.
                                        </div>
                                        <div class="news-card-footer" style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="news-action-link">Ler notícia completa ➔</span>
                                            <a class="news-source-link" href="https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-publica-guia-orientativo-de-seguranca-da-informacao" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="Abrir portal oficial ANPD">Fonte oficial ↗</a>
                                        </div>
                                    </div>

                                    <!-- Card 5: CSA Guidance v5 -->
                                    <div class="news-card" onclick="openNewsModal('csa-guidance-v5')">
                                        <div class="news-card-meta">
                                            <span class="news-card-date">Maio 2026</span>
                                            <span class="news-card-tag" style="background: rgba(120,217,236,0.15); color: #78d9ec;">CSA Star</span>
                                        </div>
                                        <div class="news-card-title">CSA Guia v5 de Governança para Agentes IA</div>
                                        <div class="news-card-snippet">
                                            Padrões internacionais de governança de contexto, isolamento de execução, prevenção de vazamento e Zero-Copy.
                                        </div>
                                        <div class="news-card-footer" style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="news-action-link">Ler notícia completa ➔</span>
                                            <a class="news-source-link" href="https://cloudsecurityalliance.org/research/guidance/" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="Abrir portal oficial CSA">Fonte oficial ↗</a>
                                        </div>
                                    </div>

                                    <!-- Card 6: CIS Google Cloud Benchmark v3.0 -->
                                    <div class="news-card" onclick="openNewsModal('cis-gcp-v3')">
                                        <div class="news-card-meta">
                                            <span class="news-card-date">Abril 2026</span>
                                            <span class="news-card-tag" style="background: rgba(252,173,112,0.15); color: #fcad70;">CIS Benchmark</span>
                                        </div>
                                        <div class="news-card-title">CIS GCP Benchmark v3.0 Atualizado</div>
                                        <div class="news-card-snippet">
                                            Requisitos atualizados de hardening para Cloud Storage, Workload Identity Federation e VPC Service Controls.
                                        </div>
                                        <div class="news-card-footer" style="display: flex; justify-content: space-between; align-items: center;">
                                            <span class="news-action-link">Ler notícia completa ➔</span>
                                            <a class="news-source-link" href="https://www.cisecurity.org/benchmark/google_cloud_computing_platform" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" title="Abrir portal oficial CIS">Fonte oficial ↗</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="chat-input-wrapper" style="display: none;">
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
                            <textarea id="chatInput" class="chat-textarea" placeholder="Consulte o Agentic GRC Auditor (Google Cloud Security)..." data-i18n-placeholder="chat_input_placeholder" rows="1" onkeydown="handleChatKey(event)" oninput="handleChatInput(this)"></textarea>
                            <button id="sendBtn" class="btn-send" onclick="sendChatMessage()" title="Enviar mensagem">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5">
                                    <line x1="12" y1="19" x2="12" y2="5"/>
                                    <polyline points="5 12 12 5 19 12"/>
                                </svg>
                            </button>
                        </div>
                        <div class="chat-disclaimer" data-i18n="chat_disclaimer">
                            Google Cloud Security • As evidências e pareceres de conformidade são validados no Grafo Criptográfico SHA-256 e protegidos por Model Armor.
                        </div>
                    </div>
                </div>
            </section>

            <!-- View 2: Scan por Fases -->
            <section class="view-pane" id="view-phases">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Scan de Auditoria por Fases (Google Cloud Security)</h2>
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
                            <span class="log-msg">Motor de auditoria Google Cloud Security pronto para inicialização das 4 fases nos projetos selecionados.</span>
                        </div>
                    </div>
                </div>
            
                <!-- Painel de Tratamento de Desvios (Estritamente dentro de Scan por Fases) -->
                <div class="phase-remediation-drawer" id="phaseRemediationContainer" style="display: none;">
                    <div class="rem-header">
                        <div class="rem-title-wrap">
                            <span class="rem-badge" id="remBadge">Tratamento de Desvios</span>
                            <div class="rem-title" id="remTitle">Plano de Remediação Automatizada (Zero-Drift)</div>
                        </div>
                        <button class="btn-close-rem" onclick="closePhaseRemediation()">&times;</button>
                    </div>
                    <input type="hidden" id="remPhaseNumber" value="1">
                    <div class="rem-body" id="remBody">
                        Carregando plano de remediação técnica...
                    </div>
                    <div class="rem-footer">
                        <button class="btn-cancel" onclick="closePhaseRemediation()">Fechar</button>
                        <button class="btn-confirm" onclick="executePhaseRemediation()" style="background: var(--gcp-green);">
                            Executar Remediação Automática
                        </button>
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
                        Subagentes Nativos (Google Cloud Security)
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
                        <button class="btn-action-primary" onclick="executeSubagent('annex_a', 'Annex A Auditor Agent')" style="margin-top: auto;">Auditar Anexo A</button>
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
                        <button class="btn-action-primary" onclick="executeSubagent('horizon_scanner', 'Horizon Scanner Agent')" style="margin-top: auto;">Executar Horizon Scan</button>
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

                        <!-- View 7: FinOps & Gestão de Custos de IA -->
            <section class="view-pane" id="view-finops">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>FinOps & Gestão de Custos de IA</h2>
                        <p>Telemetria em tempo real de consumo de tokens (Prompt, Context Caching, Completion) e custos ($ USD / R$ BRL) por agente, subagente e fases de auditoria.</p>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <button class="btn-action-primary" onclick="loadFinOpsMetrics()" title="Recarregar métricas em tempo real">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="23 4 23 10 17 10"/>
                                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                            </svg>
                            Atualizar Métricas
                        </button>
                        <button class="btn-action-primary" onclick="simulateFinOpsRun()" style="background: rgba(129, 201, 149, 0.12); border-color: rgba(129, 201, 149, 0.35); color: var(--gcp-green);">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                                <polygon points="5 3 19 12 5 21 5 3"/>
                            </svg>
                            Simular Auditoria Contínua
                        </button>
                        <button class="btn-action-primary" onclick="exportFinOpsJson()">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                                <polyline points="7 10 12 15 17 10"/>
                                <line x1="12" y1="15" x2="12" y2="3"/>
                            </svg>
                            Exportar FinOps
                        </button>
                    </div>
                </div>

                <!-- KPI Cards Row -->
                <div class="scorecard-stats-row">
                    <div class="stat-card">
                        <div class="stat-label">Custo Total de IA Acumulado</div>
                        <div class="stat-val" style="color: var(--gcp-green);" id="finopsTotalCostUsd">$ 1.86 USD</div>
                        <div style="font-size: 12.5px; color: var(--text-secondary); margin-top: 2px;" id="finopsTotalCostBrl">R$ 10,62 BRL (Cotação R$ 5,70)</div>
                        <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Orçamento: $50.00 / mês • <span id="finopsQuotaUsed" style="color: var(--gcp-green); font-weight: 600;">3.7% consumido</span></div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Tokens Totais Processados</div>
                        <div class="stat-val" style="color: var(--gcp-blue);" id="finopsTotalTokens">2.253.000</div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;" id="finopsTokensBreakdown">Prompt: 1.503k | Saída: 470k</div>
                        <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Execuções de Agentes: <strong id="finopsInvocations" style="color: var(--text-primary);">379 chamadas</strong></div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Economia Gemini Context Caching</div>
                        <div class="stat-val" style="color: #81c995;" id="finopsSavingsUsd">$ 7.42 USD</div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;" id="finopsSavingsBrl">R$ 42,29 BRL economizados</div>
                        <div style="font-size: 11px; color: var(--gcp-green); margin-top: 4px;">Taxa de Cache Hit: <strong id="finopsCacheHitRatio">72.8%</strong> (Zero-Copy Evidence)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Custo Médio por Controle ISO 27001</div>
                        <div class="stat-val" style="color: #fdd663;" id="finopsCostPerControl">$ 0.020 USD</div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;">R$ 0,11 BRL por controle auditado</div>
                        <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Auditoria humana tradicional: ~R$ 350 / controle</div>
                    </div>
                </div>

                <!-- Detalhamento de Custos por Fase (Fases 1 a 4) -->
                <div class="card-panel" style="margin-top: 16px;">
                    <div class="card-title">Consumo de IA por Fase da Auditoria (Pipeline de Certificação)</div>
                    <div class="card-desc">Divisão de tokens e custos em cada estágio do ciclo de conformidade autônoma.</div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; margin-top: 14px;">
                        <div class="stat-card" style="background: var(--bg-canvas);">
                            <div style="font-size: 11px; font-weight: 600; color: var(--gcp-blue); text-transform: uppercase;">Fase 1: Triagem Zero-Copy</div>
                            <div style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 4px 0;" id="finopsPhase1Cost">$ 0.42 USD</div>
                            <div style="font-size: 12px; color: var(--text-secondary);" id="finopsPhase1Tokens">420.000 tokens • R$ 2,39</div>
                            <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Ingestão documental semântica</div>
                        </div>
                        <div class="stat-card" style="background: var(--bg-canvas);">
                            <div style="font-size: 11px; font-weight: 600; color: var(--gcp-yellow); text-transform: uppercase;">Fase 2: Telemetria Técnica GCP</div>
                            <div style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 4px 0;" id="finopsPhase2Cost">$ 0.88 USD</div>
                            <div style="font-size: 12px; color: var(--text-secondary);" id="finopsPhase2Tokens">680.000 tokens • R$ 5,02</div>
                            <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">IAM, KMS, SCC e Workload Identity</div>
                        </div>
                        <div class="stat-card" style="background: var(--bg-canvas);">
                            <div style="font-size: 11px; font-weight: 600; color: var(--gcp-red); text-transform: uppercase;">Fase 3: Teste de Eficácia & Drift</div>
                            <div style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 4px 0;" id="finopsPhase3Cost">$ 0.54 USD</div>
                            <div style="font-size: 12px; color: var(--text-secondary);" id="finopsPhase3Tokens">390.000 tokens • R$ 3,08</div>
                            <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Simulação de drift e verificação</div>
                        </div>
                        <div class="stat-card" style="background: var(--bg-canvas);">
                            <div style="font-size: 11px; font-weight: 600; color: var(--gcp-green); text-transform: uppercase;">Fase 4: Parecer & Selagem</div>
                            <div style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 4px 0;" id="finopsPhase4Cost">$ 1.64 USD</div>
                            <div style="font-size: 12px; color: var(--text-secondary);" id="finopsPhase4Tokens">352.650 tokens • R$ 9,35</div>
                            <div style="font-size: 11px; color: var(--text-tertiary); margin-top: 4px;">Gemini 2.5 Pro Lead Auditor</div>
                        </div>
                    </div>
                </div>

                <!-- Tabela Detalhada por Agente e Subagente -->
                <div class="card-panel" style="margin-top: 16px;">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <div class="card-title">Detalhamento por Agente e Subagente (Métricas e Custos)</div>
                            <div class="card-desc">Contabilização exata de prompt tokens, context cache hits, completion tokens e custo final em USD/BRL.</div>
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <input type="text" id="finopsAgentSearch" placeholder="Filtrar agentes..." oninput="filterFinopsTable(this.value)" style="background: var(--bg-canvas); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 6px 12px; font-size: 12px; color: var(--text-primary); outline: none;">
                        </div>
                    </div>

                    <div style="overflow-x: auto; margin-top: 14px;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
                            <thead>
                                <tr style="border-bottom: 1px solid var(--border-subtle); color: var(--text-secondary); font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;">
                                    <th style="padding: 10px 12px;">Agente / Subagente</th>
                                    <th style="padding: 10px 12px;">Modelo LLM</th>
                                    <th style="padding: 10px 12px;">Chamadas</th>
                                    <th style="padding: 10px 12px;">Prompt Tokens</th>
                                    <th style="padding: 10px 12px;">Cached Tokens</th>
                                    <th style="padding: 10px 12px;">Output Tokens</th>
                                    <th style="padding: 10px 12px;">Total Tokens</th>
                                    <th style="padding: 10px 12px;">Custo (USD)</th>
                                    <th style="padding: 10px 12px;">Custo (BRL)</th>
                                    <th style="padding: 10px 12px;">Economia Cache</th>
                                </tr>
                            </thead>
                            <tbody id="finopsAgentsTableBody">
                                <!-- Populated dynamically by renderFinOpsDashboard -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Tabela de Referência de Tarifas Vertex AI / Gemini Enterprise -->
                <div class="card-panel" style="margin-top: 16px;">
                    <div class="card-title">Tabela de Tarifação Oficial de Referência (Google Cloud Vertex AI)</div>
                    <div class="card-desc">Preços por milhão de tokens utilizados na apuração de custos em conformidade com as tabelas oficiais do Google Cloud.</div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 12px;">
                        <div style="background: var(--bg-canvas); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 600; color: var(--gcp-blue);">Gemini 2.5 Pro</div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Prompt: $1.25 / 1M • Output: $5.00 / 1M</div>
                            <div style="font-size: 11px; color: var(--gcp-green); margin-top: 2px;">Context Caching: $0.3125 / 1M (75% desconto)</div>
                        </div>
                        <div style="background: var(--bg-canvas); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 600; color: var(--gcp-yellow);">Gemini 2.5 Flash</div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Prompt: $0.075 / 1M • Output: $0.30 / 1M</div>
                            <div style="font-size: 11px; color: var(--gcp-green); margin-top: 2px;">Context Caching: $0.01875 / 1M (75% desconto)</div>
                        </div>
                        <div style="background: var(--bg-canvas); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 600; color: #a8c7fa;">Text Embedding 005</div>
                            <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">Prompt: $0.025 / 1M • Output: $0.00</div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">Vetorização semântica e busca RAG</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- View 6: Relatório Executivo (Google Cloudstyle) -->
            <section class="view-pane" id="view-report-exec" style="background: var(--bg-canvas); overflow-y: auto; padding: 20px 16px;">
                
                <!-- Floating Action Bar above Document Paper -->
                <div class="doc-viewer-actions-bar">
                    <div class="doc-viewer-actions-left">
                        <span class="doc-viewer-chip blue" data-i18n="doc_exec_chip">Visão Estratégica • C-Level</span>
                        <span class="doc-viewer-title" data-i18n="doc_exec_title">Continuous Compliance & Audit Dossier</span>
                    </div>
                    <div class="doc-viewer-actions-right">
                        <button class="btn-doc-action primary" onclick="printExecutiveReport()" title="Imprimir ou Salvar em PDF">
                            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            <span>Imprimir / PDF</span>
                        </button>
                        <a href="/api/reports/export?format=json" download class="btn-doc-action" title="Exportar JSON">
                            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="7 10 12 15 17 10"></polyline>
                                <line x1="12" y1="15" x2="12" y2="3"></line>
                            </svg>
                            <span>JSON</span>
                        </a>
                        <a href="/api/reports/export?format=markdown" download class="btn-doc-action" title="Exportar Markdown">
                            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                            </svg>
                            <span>Markdown</span>
                        </a>
                        <button class="btn-doc-action" onclick="openTechnicalReport()" title="Ver Relatório Técnico">
                            <span>Relatório Técnico ›</span>
                        </button>
                    </div>
                </div>

                <div class="cloudstyle-doc-sheet">
                    
                    <!-- Header with Google Cloud Wordmark and Confidentiality Badge -->
                    <div class="cloudstyle-header-row">
                        <img src="data:image/png;base64,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" alt="Google Cloud" class="cloudstyle-brand-logo">
                        <span class="cloudstyle-confidential-pill">Confidencial • Relatório de Auditoria Formal</span>
                    </div>

                    <!-- Iconic Google 4-Color Accent Stripe -->
                    <div class="google-color-stripe-bar"></div>

                    <!-- Title & Subtitle in Google Sans -->
                    <h1 class="cloudstyle-doc-title">Continuous Compliance & Audit Dossier</h1>
                    <div class="cloudstyle-doc-subtitle">
                        Avaliação autônoma de segurança da informação, conformidade contínua com a <strong>ISO/IEC 27001:2022</strong> (93 Controles do Anexo A) e validação de telemetria nos ambientes Google Cloud Platform.
                    </div>

                    <!-- Document Metadata Box -->
                    <table class="cloudstyle-meta-box">
                        <tr>
                            <td>Organização / Cliente</td>
                            <td>Google Cloud Security & Workload Projects</td>
                        </tr>
                        <tr>
                            <td>Código do Documento</td>
                            <td><strong id="docReportId">GCS-GRC-ISO27001-2026-FINAL</strong></td>
                        </tr>
                        <tr>
                            <td>Norma & Emendas Auditadas</td>
                            <td>ABNT NBR ISO/IEC 27001:2022 (Anexo A - 93 Controles) + Amd 1:2024 (Ação Climática)</td>
                        </tr>
                        <tr>
                            <td>Auditor Líder Responsável</td>
                            <td>Agentic GRC Auditor (Vertex AI Gemini 2.5 Flash Autonomous Lead Auditor)</td>
                        </tr>
                        <tr>
                            <td>Projetos no Escopo</td>
                            <td><span id="docProjectsAudited">agentic-grc-cd06</span></td>
                        </tr>
                        <tr>
                            <td>Garantia Criptográfica</td>
                            <td><span style="font-family: var(--font-mono); color: #137333; font-weight: 600;">Grafo de Evidências SHA-256 Imutável • Model Armor Ativo</span></td>
                        </tr>
                    </table>

                    <!-- Numbered Highlights Grid: 01, 02, 03, 04 (Pure Cloudstyle) -->
                    <div class="cloudstyle-highlights-grid">
                        <div class="cloudstyle-highlight-item">
                            <div class="cloudstyle-card-num">01</div>
                            <div class="cloudstyle-card-title">Conformidade Global</div>
                            <div class="cloudstyle-card-text"><strong>100.0% (EXCELLENT)</strong> de aderência aos 93 controles do Anexo A avaliados continuamente.</div>
                        </div>
                        <div class="cloudstyle-highlight-item">
                            <div class="cloudstyle-card-num">02</div>
                            <div class="cloudstyle-card-title">Criptografia & HSM</div>
                            <div class="cloudstyle-card-text">Chaves Cloud KMS em HSM FIPS 140-2 com rotação compulsória de 60 dias e UBLA ativo.</div>
                        </div>
                        <div class="cloudstyle-highlight-item">
                            <div class="cloudstyle-card-num">03</div>
                            <div class="cloudstyle-card-title">Perímetros & DLP</div>
                            <div class="cloudstyle-card-text">VPC Service Controls, PAP ativado e inspeção contínua contra exfiltração de dados sensíveis.</div>
                        </div>
                        <div class="cloudstyle-highlight-item">
                            <div class="cloudstyle-card-num">04</div>
                            <div class="cloudstyle-card-title">Grafo SHA-256</div>
                            <div class="cloudstyle-card-text">Nós de evidência selados com garantia matemática de integridade, trilha de auditoria e não-repúdio.</div>
                        </div>
                    </div>

                    <!-- Executive Quote / Opinion Callout -->
                    <div class="cloudstyle-quote-callout">
                        <div class="cloudstyle-quote-text">
                            “Com base na coleta automatizada de telemetria, inspeção contínua de configurações e análise de infraestrutura como código (IaC), a prática de Google Cloud Security emite uma <strong>OPINIÃO LIMPA E SEM RESSALVAS (UNQUALIFIED OPINION)</strong>, atestando conformidade plena com os 93 requisitos do Anexo A da ISO/IEC 27001:2022.”
                        </div>
                        <div class="cloudstyle-quote-author">
                            — Agentic GRC Virtual Lead Auditor, Google Cloud Security Practice
                        </div>
                    </div>

                    <!-- Section 1: Breakdown dos 4 Temas da ISO 27001:2022 -->
                    <div class="cloudstyle-heading-block">1. Estrutura de Controles por Tema (ISO/IEC 27001:2022)</div>
                    <table class="cloudstyle-table">
                        <thead>
                            <tr>
                                <th style="width: 28%;">Tema Normativo</th>
                                <th style="width: 18%;">Total de Controles</th>
                                <th style="width: 20%;">Status Auditado</th>
                                <th>Postura Técnica & Serviços Google Cloud</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>A.5 Organizacional</strong></td>
                                <td>37 controles</td>
                                <td><span class="cloudstyle-badge-success">100% CONFORME</span></td>
                                <td>Políticas do SGSI aprovadas, Organization Policies, Gestão de Acessos IAM</td>
                            </tr>
                            <tr>
                                <td><strong>A.6 Pessoas</strong></td>
                                <td>8 controles</td>
                                <td><span class="cloudstyle-badge-success">100% CONFORME</span></td>
                                <td>Conscientização em segurança, termos de confidencialidade e offboarding</td>
                            </tr>
                            <tr>
                                <td><strong>A.7 Físico</strong></td>
                                <td>14 controles</td>
                                <td><span class="cloudstyle-badge-success">100% CONFORME</span></td>
                                <td>Perímetros físicos e segurança de Data Centers GCP (SOC 2 Tipo II, ISO 27001)</td>
                            </tr>
                            <tr>
                                <td><strong>A.8 Tecnológico</strong></td>
                                <td>34 controles</td>
                                <td><span class="cloudstyle-badge-success">100% CONFORME</span></td>
                                <td>Cloud KMS HSM, VPC-SC, IaC Terraform Scanner, BigQuery Data Masking, SLSA-3</td>
                            </tr>
                            <tr>
                                <td><strong>Amd 1:2024 Ação Climática</strong></td>
                                <td>Cláusulas 4.1 e 4.2</td>
                                <td><span class="cloudstyle-badge-success">100% CONFORME</span></td>
                                <td>Regiões de Baixo Carbono (Low-Carbon Mode), FinOps e descarte sustentável</td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- Section 2: Amostra de Controles Técnicos Auditados (SoA) -->
                    <div class="cloudstyle-heading-block">2. Amostra de Controles & Declaração de Aplicabilidade (SoA)</div>
                    <table class="cloudstyle-table">
                        <thead>
                            <tr>
                                <th style="width: 12%;">Controle</th>
                                <th style="width: 26%;">Requisito Normativo</th>
                                <th style="width: 32%;">Implementação Google Cloud</th>
                                <th style="width: 15%;">Status</th>
                                <th style="width: 15%;">Evidência</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>A.5.1</strong></td>
                                <td>Políticas de Segurança da Informação</td>
                                <td>Organization Policies GCP + SGSI via Zero-Copy</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                            <tr>
                                <td><strong>A.5.15</strong></td>
                                <td>Controle de Acesso (Privilégio Mínimo)</td>
                                <td>IAM Recommender + MFA compulsório</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                            <tr>
                                <td><strong>A.5.23</strong></td>
                                <td>Segurança em Serviços em Nuvem</td>
                                <td>Public Access Prevention (PAP) + UBLA</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                            <tr>
                                <td><strong>A.8.10</strong></td>
                                <td>Exclusão de Dados</td>
                                <td>Object Lifecycle Management + Bucket Lock WORM</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                            <tr>
                                <td><strong>A.8.12</strong></td>
                                <td>Prevenção de Fuga de Dados (DLP)</td>
                                <td>VPC Service Controls + Sensitive Data Protection</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                            <tr>
                                <td><strong>A.8.24</strong></td>
                                <td>Uso de Criptografia</td>
                                <td>Cloud KMS HSM (FIPS 140-2 Nível 3) + Rotação 60d</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                            <tr>
                                <td><strong>A.8.28</strong></td>
                                <td>Codificação Segura (DevSecOps)</td>
                                <td>IaC Scanner Terraform + Binary Authorization SLSA-3</td>
                                <td><span class="cloudstyle-badge-success">Conforme</span></td>
                                <td><code>SHA-256 Validado</code></td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- Digital Seal and Formal Sign-off -->
                    <div class="cloudstyle-seal-wrapper">
                        <div>
                            <div style="font-weight: 700; color: #202124; font-size: 13.5px;">Google Cloud Security Practice</div>
                            <div style="font-size: 12px; color: #5f6368; margin-top: 2px;">Agentic GRC & Autonomous Compliance Advisory</div>
                            <div style="font-size: 11.5px; color: #80868b; margin-top: 4px;">Gemini Enterprise Agent Platform (GEAP)</div>
                        </div>
                        <div class="cloudstyle-seal-box">
                            <div class="cloudstyle-seal-tag">VERIFIED BY VERTEX AI GEMINI</div>
                            <div style="font-size: 11px; color: #1a73e8; font-weight: 600; margin-top: 2px;">SELO DE INTEGRIDADE SHA-256</div>
                            <div class="cloudstyle-seal-hash">Hash: 7a8421429cf6bd6354...</div>
                        </div>
                    </div>

                    <!-- Cloudstyle Footer -->
                    <div class="cloudstyle-footer-block">
                        <span>Google Cloud Security • Para mais informações, acesse <a href="https://cloud.google.com/security" target="_blank" style="color: #1a73e8; text-decoration: none;">cloud.google.com/security</a></span>
                        <span>Documento Confidencial • Emitido via GEAP</span>
                    </div>

                </div>
            </section>

            <!-- =========================================================================
                 RELATÓRIO TÉCNICO DE AUDITORIA EXTERNA (ISO/IEC 27001:2022 STAGE 2 / CERTIFICAÇÃO)
                 Projetado especificamente para entrega a organismos certificadores externos
                 ========================================================================= -->
            <section class="view-pane" id="view-report-tech" style="background: var(--bg-canvas); overflow-y: auto; padding: 20px 16px;">
                
                <!-- Floating Action Bar above Document Paper -->
                <div class="doc-viewer-actions-bar">
                    <div class="doc-viewer-actions-left">
                        <span class="doc-viewer-chip" data-i18n="doc_tech_chip">Auditoria Externa • Stage 2</span>
                        <span class="doc-viewer-title" data-i18n="doc_tech_title">ISO/IEC 27001:2022 Technical Dossier</span>
                    </div>
                    <div class="doc-viewer-actions-right">
                        <button class="btn-doc-action primary" onclick="printTechnicalReport()" title="Imprimir ou Salvar em PDF">
                            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                                <rect x="6" y="14" width="12" height="8"></rect>
                            </svg>
                            <span>Imprimir / PDF</span>
                        </button>
                        <a href="/api/reports/export?format=json" download class="btn-doc-action" title="Exportar JSON">
                            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="7 10 12 15 17 10"></polyline>
                                <line x1="12" y1="15" x2="12" y2="3"></line>
                            </svg>
                            <span>JSON</span>
                        </a>
                        <a href="/api/reports/export?format=markdown" download class="btn-doc-action" title="Exportar Markdown">
                            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                            </svg>
                            <span>Markdown</span>
                        </a>
                        <button class="btn-doc-action" onclick="openExecutiveReport()" title="Ver Dossiê Executivo">
                            <span>Dossiê Executivo ›</span>
                        </button>
                    </div>
                </div>

                <div class="cloudstyle-doc-sheet">
                    
                    <!-- Header with Google Cloud Wordmark and Certification Badge -->
                    <div class="cloudstyle-header-row">
                        <img src="data:image/png;base64,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" alt="Google Cloud" class="cloudstyle-brand-logo">
                        <span class="cloudstyle-confidential-pill" style="background: rgba(234, 67, 53, 0.08); color: #d93025; border-color: rgba(234, 67, 53, 0.2);">
                            CONFIDENCIAL • RELATÓRIO TÉCNICO DE AUDITORIA EXTERNA (STAGE 2)
                        </span>
                    </div>

                    <h1 class="cloudstyle-doc-title">Relatório Técnico de Auditoria Externa & Statement of Applicability (SoA)</h1>
                    <div class="cloudstyle-doc-subtitle">
                        Auditoria Independente de Eficácia Operacional dos 93 Controles ISO/IEC 27001:2022, ISO/IEC 27017 & ISO/IEC 27018 em Google Cloud
                    </div>

                    <!-- Ficha Técnica da Auditoria Externa -->
                    <table class="cloudstyle-meta-box">
                        <tr>
                            <td>Código do Dossiê Técnico</td>
                            <td><code style="font-family: monospace; font-weight: 700; color: #1a73e8;" id="techDossierCode">GCS-EXT-AUDIT-ISO27001-2022-TECH-001</code></td>
                        </tr>
                        <tr>
                            <td>Normas & Critérios de Auditoria</td>
                            <td>
                                <strong>ABNT NBR ISO/IEC 27001:2022</strong> (Anexo A - 93 Controles)<br>
                                <span style="font-size: 11px; color: var(--text-secondary);">Completado com: ISO/IEC 27017:2015 (Segurança em Nuvem) e ISO/IEC 27018:2019 (Privacidade de Dados PII em Nuvem Pública)</span>
                            </td>
                        </tr>
                        <tr>
                            <td>Organismos Alvo & Entidades Receptoras</td>
                            <td><strong>Organismo de Certificação Acreditado</strong> (BSI, DNV, TÜV, Bureau Veritas, A-LIGN, Schellman ou Big 4 Audit)</td>
                        </tr>
                        <tr>
                            <td>Escopo de Auditoria (GCP Projects)</td>
                            <td><strong id="techProjectsAudited">agentic-grc-cd06</strong> (Google Cloud Multi-Region Tenant)</td>
                        </tr>
                        <tr>
                            <td>Metodologia de Teste</td>
                            <td><strong>Teste Contínuo de População Total (100% Automated Population Testing)</strong> via Telemetria Contínua, Cloud Asset Inventory e SPIFFE Zero-Copy Connectors (Zero-Sampling Error)</td>
                        </tr>
                        <tr>
                            <td>Data e Hora da Emissão</td>
                            <td><span id="techGeneratedAt">2026-09-04 14:15:00 UTC</span></td>
                        </tr>
                        <tr>
                            <td>Parecer Técnico Conclusivo</td>
                            <td>
                                <span class="cloudstyle-badge-success" style="background: #e6f4ea; color: #137333; font-weight: 700;">
                                    RECOMENDAÇÃO DE CERTIFICAÇÃO SEM RESSALVAS (UNQUALIFIED CLEAN OPINION)
                                </span>
                            </td>
                        </tr>
                    </table>

                    <!-- Parecer Formal do Auditor Líder -->
                    <div class="cloudstyle-quote-callout">
                        <div class="cloudstyle-quote-text">
                            "Com base nos testes de desenho e de eficácia operacional contínua executados sobre 100% da infraestrutura em nuvem, certificamos que os controles do SGSI descritos na Declaração de Aplicabilidade (SoA) estão plenamente implementados, operando de forma autônoma e mitigando os riscos cibernéticos em estrita conformidade com os requisitos da norma ISO/IEC 27001:2022. Não foram identificadas Não-Conformidades Maiores ou Menores remanescentes."
                        </div>
                        <div class="cloudstyle-quote-author">
                            — <strong>Agentic GRC Auditor</strong>, Lead Auditor Virtual Certificado Google Cloud Security PSO & GEAP
                        </div>
                    </div>

                    <!-- Cobertura da Auditoria Externa por Domínio ISO/IEC 27001:2022 -->
                    <div class="cloudstyle-heading-block">
                        1. Resumo Quantitativo de Eficácia Operacional (4 Domínios ISO/IEC 27001:2022)
                    </div>
                    <p class="tech-section-lead">
                        Em conformidade com a estrutura da ISO/IEC 27001:2022, todos os 93 controles distribuídos nos 4 domínios foram submetidos a testes contínuos de verificação técnica via APIs e agentes autônomos.
                    </p>

                    <div class="tech-stat-grid">
                        <div class="tech-stat-card green">
                            <div class="tech-stat-code">Domínio A.5</div>
                            <div class="tech-stat-val">37 / 37</div>
                            <div class="tech-stat-desc">Controles Organizacionais<br><strong>100% Conforme</strong> (Políticas, Inventário, Gestão de Acessos)</div>
                        </div>
                        <div class="tech-stat-card green">
                            <div class="tech-stat-code">Domínio A.6</div>
                            <div class="tech-stat-val">8 / 8</div>
                            <div class="tech-stat-desc">Controles de Pessoas<br><strong>100% Conforme</strong> (Termos, Conscientização, Desligamento)</div>
                        </div>
                        <div class="tech-stat-card green">
                            <div class="tech-stat-code">Domínio A.7</div>
                            <div class="tech-stat-val">14 / 14</div>
                            <div class="tech-stat-desc">Controles Físicos & Ambientais<br><strong>100% Conforme</strong> (Datacenters GCP com ISO 27001/SOC 2)</div>
                        </div>
                        <div class="tech-stat-card green">
                            <div class="tech-stat-code">Domínio A.8</div>
                            <div class="tech-stat-val">34 / 34</div>
                            <div class="tech-stat-desc">Controles Tecnológicos<br><strong>100% Conforme</strong> (KMS HSM, VPC-SC, DLP, IAM, WAF)</div>
                        </div>
                    </div>

                    <!-- Matriz SoA (Statement of Applicability) -->
                    <div class="cloudstyle-heading-block">
                        2. Declaração de Aplicabilidade Técnica (Statement of Applicability - SoA v2022.4)
                    </div>
                    <p class="tech-section-lead">
                        A tabela a seguir documenta a rastreabilidade direta entre os requisitos normativos da ISO/IEC 27001:2022 e os mecanismos técnicos de implementação e comprovação operacional no Google Cloud:
                    </p>

                    <table class="cloudstyle-table">
                        <thead>
                            <tr>
                                <th style="width: 80px;">Controle</th>
                                <th style="width: 220px;">Título ISO/IEC 27001:2022</th>
                                <th style="width: 80px;">SoA</th>
                                <th>Mecanismo Técnico no Google Cloud</th>
                                <th style="width: 170px;">Fonte da Telemetria</th>
                                <th style="width: 110px;">Resultado</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>A.5.1</code></td>
                                <td>Políticas para Segurança da Informação</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Repositório de Políticas Corporativas ancorado via Zero-Copy Connector com hash SHA-256 imutável.</td>
                                <td>Cloud Storage & CI Engine</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.5.15</code></td>
                                <td>Controle de Acesso</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Google Cloud IAM com Princípio do Menor Privilégio, Just-In-Time Access e IAM Recommender.</td>
                                <td>Cloud Asset Inventory API</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.5.24</code></td>
                                <td>Planejamento e Preparação da Gestão de Incidentes</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Playbooks automatizados integrados ao Security Command Center (SCC) e Cloud Monitoring.</td>
                                <td>SCC Findings API</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.5.37</code></td>
                                <td>Procedimentos Operacionais Documentados</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Infraestrutura como Código (Terraform) versionada em Git com escaneamento preventivo de desvios.</td>
                                <td>IaC Scanner & Cloud Build</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.6.8</code></td>
                                <td>Notificação de Eventos de Segurança</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Canais de alerta em tempo real (Pub/Sub + Webhook) com detecção autônoma de anomalias por IA.</td>
                                <td>Cloud Logging / PubSub</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.7.1</code></td>
                                <td>Perímetros de Segurança Física</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Herança direta da infraestrutura de datacenters globais Google Cloud (certificados ISO/IEC 27001 e SOC 2).</td>
                                <td>GCP Compliance Reports</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.2</code></td>
                                <td>Privilégios de Acesso Privilegiado</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Proibição compulsória de chaves de Service Account (<code>iam.disableServiceAccountKeyCreation</code>) e MFA obrigatório.</td>
                                <td>Resource Manager Org Policy</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.5</code></td>
                                <td>Autenticação Segura</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Workforce Identity Federation com suporte a chaves físicas FIDO2/WebAuthn e OAuth 2.0 PKCE.</td>
                                <td>Cloud Identity API</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.9</code></td>
                                <td>Gestão de Configurações Seguras</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Organization Policies restritivas na raiz do Tenant e compliance contínuo via IaC Scanner.</td>
                                <td>Org Policies API</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.12</code></td>
                                <td>Prevenção contra Fuga de Dados (DLP)</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Perímetros VPC Service Controls (VPC-SC) com Cloud DLP inspecionando e desidentificando dados sensíveis.</td>
                                <td>Access Context Manager</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.20</code></td>
                                <td>Segurança de Redes</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Cloud Armor Edge WAF com regras OWASP Top 10, anti-DDoS e Private Google Access (zero IPs públicos).</td>
                                <td>Compute Security Policies</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.24</code></td>
                                <td>Uso de Criptografia</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Chaves Customer-Managed (CMEK) em Cloud KMS com Hardware Security Module (HSM) FIPS 140-2 Nível 3.</td>
                                <td>Cloud KMS API</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                            <tr>
                                <td><code>A.8.28</code></td>
                                <td>Engenharia de Segurança de Software</td>
                                <td><span class="tech-badge-pass">Sim</span></td>
                                <td>Binary Authorization bloqueando contêineres sem assinatura criptográfica no Cloud Build / Artifact Registry.</td>
                                <td>Binary Authorization API</td>
                                <td><span class="tech-badge-pass">✓ Conforme</span></td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- Caderno de Evidências Técnicas Verificáveis -->
                    <div class="cloudstyle-heading-block">
                        3. Caderno de Evidências Técnicas Verificáveis (Technical Evidence Repository)
                    </div>
                    <p class="tech-section-lead">
                        As evidências técnicas a seguir contêm saídas de comandos oficiais do Google Cloud CLI (<code>gcloud</code>), telemetrias de APIs e hashes imutáveis que comprovam a operação contínua e sem falhas dos controles críticos de segurança:
                    </p>

                    <!-- Evidência 1 -->
                    <div class="tech-evidence-card">
                        <div class="tech-evidence-header">
                            <div class="tech-evidence-title-wrap">
                                <span class="tech-evidence-badge">EVIDÊNCIA 01</span>
                                <span class="tech-evidence-title">A.8.2 & A.8.5 — Restrição Total de Chaves Estáticas e Menor Privilégio (IAM)</span>
                            </div>
                            <span class="tech-badge-pass">✓ Verificação Aprovada</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                            <strong>Procedimento de Teste:</strong> Auditoria exaustiva em todas as Service Accounts para garantir ausência de chaves de usuário (<code>USER_MANAGED</code>) e imposição de política organizacional de bloqueio de criação de chaves.
                        </div>
                        <div class="tech-code-box">
<span class="tech-code-comment"># Verificação da Organização: Bloqueio de Chaves Estáticas de Service Account</span>
<span class="tech-code-cmd">$ gcloud resource-manager org-policies describe constraints/iam.disableServiceAccountKeyCreation --organization=ORGANIZATION_ID</span>
<span class="tech-code-key">booleanPolicy:</span>
  <span class="tech-code-key">enforced:</span> <span class="tech-code-val">true</span>
<span class="tech-code-key">constraint:</span> <span class="tech-code-str">constraints/iam.disableServiceAccountKeyCreation</span>

<span class="tech-code-comment"># Varredura de Chaves Estáticas Ativas no Projeto em Escopo</span>
<span class="tech-code-cmd">$ gcloud iam service-accounts keys list --iam-account=sa-grc-core@agentic-grc-cd06.iam.gserviceaccount.com</span>
<span class="tech-code-key">KEY_ID</span>                            <span class="tech-code-key">CREATED_AT</span>            <span class="tech-code-key">EXPIRES_AT</span>            <span class="tech-code-key">KEY_TYPE</span>
7a9b1c3d5e7f8024a1b2c3d4e5f6a7b8  2026-08-01T00:00:00Z  2026-09-01T00:00:00Z  <span class="tech-code-val">SYSTEM_MANAGED (Google Rotated)</span>
<span class="tech-code-comment"># Total de chaves USER_MANAGED encontradas: 0 (Zero Trust Validado)</span>
                        </div>
                    </div>

                    <!-- Evidência 2 -->
                    <div class="tech-evidence-card">
                        <div class="tech-evidence-header">
                            <div class="tech-evidence-title-wrap">
                                <span class="tech-evidence-badge">EVIDÊNCIA 02</span>
                                <span class="tech-evidence-title">A.8.9 & A.5.37 — Governança de Configurações Seguras via Organization Policies</span>
                            </div>
                            <span class="tech-badge-pass">✓ Verificação Aprovada</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                            <strong>Procedimento de Teste:</strong> Validação de restrições organizacionais mandatórias contra exposição inadvertida de buckets e redes no Cloud Storage e Compute Engine.
                        </div>
                        <div class="tech-code-box">
<span class="tech-code-comment"># 1. Bloqueio Mandatório de Compartilhamento Público de Buckets (Public Access Prevention)</span>
<span class="tech-code-cmd">$ gcloud resource-manager org-policies describe constraints/storage.publicAccessPrevention --organization=ORGANIZATION_ID</span>
<span class="tech-code-key">booleanPolicy:</span>
  <span class="tech-code-key">enforced:</span> <span class="tech-code-val">true</span>

<span class="tech-code-comment"># 2. Imposição de Acesso Uniforme em Nível de Bucket (Uniform Bucket-Level Access - UBLA)</span>
<span class="tech-code-cmd">$ gcloud resource-manager org-policies describe constraints/storage.uniformBucketLevelAccess --organization=ORGANIZATION_ID</span>
<span class="tech-code-key">booleanPolicy:</span>
  <span class="tech-code-key">enforced:</span> <span class="tech-code-val">true</span>

<span class="tech-code-comment"># 3. Proibição de IPs Externos para Instâncias Virtuais Privadas</span>
<span class="tech-code-cmd">$ gcloud resource-manager org-policies describe constraints/compute.vmExternalIpAccess --organization=ORGANIZATION_ID</span>
<span class="tech-code-key">listPolicy:</span>
  <span class="tech-code-key">allValues:</span> <span class="tech-code-val">DENY</span>
                        </div>
                    </div>

                    <!-- Evidência 3 -->
                    <div class="tech-evidence-card">
                        <div class="tech-evidence-header">
                            <div class="tech-evidence-title-wrap">
                                <span class="tech-evidence-badge">EVIDÊNCIA 03</span>
                                <span class="tech-evidence-title">A.8.12 — Perímetro de Serviço VPC (VPC-SC) e Prevenção de Fuga de Dados (DLP)</span>
                            </div>
                            <span class="tech-badge-pass">✓ Verificação Aprovada</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                            <strong>Procedimento de Teste:</strong> Verificação do perímetro de segurança lógica de rede para isolar APIs do Google Cloud contra exfiltração de dados sensíveis e credenciais.
                        </div>
                        <div class="tech-code-box">
<span class="tech-code-comment"># Status do Perímetro de Serviço no Access Context Manager</span>
<span class="tech-code-cmd">$ gcloud access-context-manager perimeters describe iso_27001_perimeter --policy=DEFAULT_POLICY</span>
<span class="tech-code-key">name:</span> <span class="tech-code-str">accessPolicies/198273645/servicePerimeters/iso_27001_perimeter</span>
<span class="tech-code-key">status:</span>
  <span class="tech-code-key">restrictedServices:</span>
  - <span class="tech-code-val">storage.googleapis.com</span>
  - <span class="tech-code-val">bigquery.googleapis.com</span>
  - <span class="tech-code-val">dlp.googleapis.com</span>
  - <span class="tech-code-val">cloudkms.googleapis.com</span>
  <span class="tech-code-key">vpcAccessibleServices:</span>
    <span class="tech-code-key">enableRestriction:</span> <span class="tech-code-val">true</span>
<span class="tech-code-comment"># Resultado: Perímetro em modo ENFORCED bloqueando chamadas fora do perímetro autorizado.</span>
                        </div>
                    </div>

                    <!-- Evidência 4 -->
                    <div class="tech-evidence-card">
                        <div class="tech-evidence-header">
                            <div class="tech-evidence-title-wrap">
                                <span class="tech-evidence-badge">EVIDÊNCIA 04</span>
                                <span class="tech-evidence-title">A.8.20 & A.8.22 — Proteção de Borda com Cloud Armor WAF & Segmentação de Rede</span>
                            </div>
                            <span class="tech-badge-pass">✓ Verificação Aprovada</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                            <strong>Procedimento de Teste:</strong> Auditoria das políticas de segurança Cloud Armor e ausência de regras de firewall de entrada permitindo portas SSH/RDP para a Internet aberta.
                        </div>
                        <div class="tech-code-box">
<span class="tech-code-comment"># 1. Auditoria de Firewall: Verificação de Portas 22 (SSH) e 3389 (RDP) expostas para 0.0.0.0/0</span>
<span class="tech-code-cmd">$ gcloud compute firewall-rules list --filter="direction=INGRESS AND allowed.ports:(22 OR 3389) AND sourceRanges:0.0.0.0/0"</span>
<span class="tech-code-val">Listed 0 items. (Em estrita conformidade - Todas as conexões via Identity-Aware Proxy)</span>

<span class="tech-code-comment"># 2. Status da Política Cloud Armor Edge WAF</span>
<span class="tech-code-cmd">$ gcloud compute security-policies describe grc-edge-waf --project=agentic-grc-cd06</span>
<span class="tech-code-key">rules:</span>
- <span class="tech-code-key">action:</span> <span class="tech-code-val">deny(403)</span>
  <span class="tech-code-key">priority:</span> 1000
  <span class="tech-code-key">match:</span> <span class="tech-code-str">evaluatePreconfiguredExpr('cve-canary') || evaluatePreconfiguredExpr('owasp-crs-v030301-id942100-sqli')</span>
                        </div>
                    </div>

                    <!-- Evidência 5 -->
                    <div class="tech-evidence-card">
                        <div class="tech-evidence-header">
                            <div class="tech-evidence-title-wrap">
                                <span class="tech-evidence-badge">EVIDÊNCIA 05</span>
                                <span class="tech-evidence-title">A.8.24 — Criptografia com Chaves em Hardware FIPS 140-2 Nível 3 (Cloud KMS HSM)</span>
                            </div>
                            <span class="tech-badge-pass">✓ Verificação Aprovada</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                            <strong>Procedimento de Teste:</strong> Comprovação de uso de chaves Customer-Managed Encryption Keys (CMEK) em módulo HSM físico com rotação compulsória e ciclo de vida criptográfico ativo.
                        </div>
                        <div class="tech-code-box">
<span class="tech-code-comment"># Metadados da Chave Criptográfica Primária do Sistema de Gestão</span>
<span class="tech-code-cmd">$ gcloud kms keys describe grc-master-hsm-key --keyring=grc-fips-ring --location=us-central1</span>
<span class="tech-code-key">name:</span> <span class="tech-code-str">projects/agentic-grc-cd06/locations/us-central1/keyRings/grc-fips-ring/cryptoKeys/grc-master-hsm-key</span>
<span class="tech-code-key">protectionLevel:</span> <span class="tech-code-val">HSM (Hardware Security Module - FIPS 140-2 Level 3)</span>
<span class="tech-code-key">purpose:</span> <span class="tech-code-val">ENCRYPT_DECRYPT</span>
<span class="tech-code-key">rotationPeriod:</span> <span class="tech-code-val">5184000s (60 dias)</span>
<span class="tech-code-key">nextRotationTime:</span> <span class="tech-code-str">'2026-11-03T14:00:00Z'</span>
<span class="tech-code-key">primary:</span>
  <span class="tech-code-key">algorithm:</span> <span class="tech-code-val">GOOGLE_SYMMETRIC_ENCRYPTION (AES-256-GCM)</span>
  <span class="tech-code-key">state:</span> <span class="tech-code-val">ENABLED</span>
                        </div>
                    </div>

                    <!-- Evidência 6 -->
                    <div class="tech-evidence-card">
                        <div class="tech-evidence-header">
                            <div class="tech-evidence-title-wrap">
                                <span class="tech-evidence-badge">EVIDÊNCIA 06</span>
                                <span class="tech-evidence-title">A.8.28 — Assinatura Criptográfica de Imagens de Contêiner (Binary Authorization)</span>
                            </div>
                            <span class="tech-badge-pass">✓ Verificação Aprovada</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
                            <strong>Procedimento de Teste:</strong> Verificação de bloqueio contra execução de contêineres e códigos sem atestação formal de integridade e vulnerabilidades.
                        </div>
                        <div class="tech-code-box">
<span class="tech-code-comment"># Política de Admissão de Contêineres no Cloud Run e GKE</span>
<span class="tech-code-cmd">$ gcloud container binauthz policy export</span>
<span class="tech-code-key">defaultAdmissionRule:</span>
  <span class="tech-code-key">enforcementMode:</span> <span class="tech-code-val">ENFORCING</span>
  <span class="tech-code-key">evaluationMode:</span> <span class="tech-code-val">REQUIRE_ATTESTATION</span>
  <span class="tech-code-key">requireAttestationsBy:</span>
  - <span class="tech-code-str">projects/agentic-grc-cd06/attestors/secops-build-attestor</span>
<span class="tech-code-comment"># Resultado: Zero contêineres não assinados autorizados a executar em ambiente produtivo.</span>
                        </div>
                    </div>

                    <!-- Matriz de Não-Conformidades e Ações Corretivas (CAPA) -->
                    <div class="cloudstyle-heading-block">
                        4. Trilha de Eficácia Operacional e Tratamento de Desvios (CAPA Register)
                    </div>
                    <p class="tech-section-lead">
                        Registro dos desvios identificados durante as rotinas de telemetria contínua, planos de ação gerados e histórico de aprovação humana (Human-in-the-Loop):
                    </p>

                    <table class="cloudstyle-table">
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Classificação</th>
                                <th>Descrição da Observação</th>
                                <th>Ação Corretiva Aplicada</th>
                                <th>Validador HITL</th>
                                <th>Status Final</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>OFI-001</code></td>
                                <td><span style="background: #fef7e0; color: #b06000; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700;">OFI</span></td>
                                <td>Bucket legado secundário com UBLA desativado detectado na fase inicial.</td>
                                <td>Aplicação automatizada de <code>gcloud storage buckets update --uniform-bucket-level-access</code> via subagente.</td>
                                <td>Security Officer</td>
                                <td><span class="tech-badge-pass">Resolvido & Validado</span></td>
                            </tr>
                            <tr>
                                <td><code>OFI-002</code></td>
                                <td><span style="background: #fef7e0; color: #b06000; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700;">OFI</span></td>
                                <td>Regra de firewall de desenvolvimento temporária com escopo abrangente.</td>
                                <td>Substituição imediata por túnel seguro via Google Cloud Identity-Aware Proxy (IAP).</td>
                                <td>Lead Architect</td>
                                <td><span class="tech-badge-pass">Resolvido & Validado</span></td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- Selo Criptográfico de Integridade -->
                    <div class="cloudstyle-seal-wrapper">
                        <div class="cloudstyle-seal-box">
                            <div class="cloudstyle-seal-tag">SELO CRIPTOGRÁFICO DE INTEGRIDADE DA AUDITORIA EXTERNA</div>
                            <div class="cloudstyle-seal-hash">Merkle Root Hash: 9f8e7d6c5b4a39281726354859607182a3b4c5d6e7f8091a2b3c4d5e6f7a8b9c</div>
                            <div style="margin-top: 6px; font-size: 11px; color: var(--text-secondary);">
                                Dossiê SHA-256: <code>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</code> • Carimbo de Tempo RFC 3161 Atômico: <span id="techSealDate">2026-09-04 14:15:00 UTC</span>
                            </div>
                        </div>
                    </div>

                    <!-- Bloco Formal de Assinaturas e Atestação -->
                    <div class="tech-signature-grid">
                        <div class="tech-sig-box">
                            <div class="tech-sig-name">Agentic GRC Auditor</div>
                            <div class="tech-sig-role">Auditor Líder Técnico Virtual (SPIFFE Validated)</div>
                            <div class="tech-sig-line"></div>
                            <span class="tech-sig-status">✓ Atestação Criptográfica Emitida</span>
                        </div>
                        <div class="tech-sig-box">
                            <div class="tech-sig-name">Chief Information Security Officer</div>
                            <div class="tech-sig-role">Gestor do SGSI (ISMS Manager)</div>
                            <div class="tech-sig-line"></div>
                            <span class="tech-sig-status">✓ Homologado sem Ressalvas</span>
                        </div>
                        <div class="tech-sig-box">
                            <div class="tech-sig-name">Lead Certification Auditor</div>
                            <div class="tech-sig-role">Auditor Externo (Organismo Credenciado)</div>
                            <div class="tech-sig-line"></div>
                            <span class="tech-sig-status">✓ Revisão Técnica Concluída</span>
                        </div>
                    </div>

                    <div class="cloudstyle-footer-block" style="margin-top: 32px;">
                        Google Cloud Security PSO & Regulatory Compliance • Relatório emitido para organismos de certificação acreditados sob as normas ABNT NBR ISO/IEC 27001:2022, ISO/IEC 27017:2015 e ISO/IEC 27018:2019.
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

        <!-- Modal: Leitura de Notícia Regulatória & Auditoria Opcional -->
    <div class="modal-overlay" id="newsModal">
        <div class="modal-window" style="max-width: 680px; border-radius: 16px;">
            <div class="modal-header" style="border-bottom: 1px solid var(--border-subtle); padding: 16px 20px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span id="newsModalTag" class="news-card-tag" style="font-size: 11px; padding: 4px 8px;"></span>
                    <span class="modal-title" id="newsModalTitle" style="font-size: 16px; font-weight: 600; color: #ffffff;"></span>
                </div>
                <button class="btn-collapse" onclick="closeNewsModal()" title="Fechar">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
            <div class="modal-body" style="display: flex; flex-direction: column; gap: 16px; max-height: 65vh; overflow-y: auto; padding: 20px;">
                <div style="display: flex; justify-content: space-between; font-size: 12.5px; color: var(--text-tertiary); border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                    <span>Publicação: <strong id="newsModalDate" style="color: var(--text-primary);"></strong></span>
                    <span>Órgão Emissor: <strong id="newsModalIssuer" style="color: var(--gcp-blue);"></strong></span>
                </div>

                <div>
                    <h4 style="font-size: 13.5px; color: #ffffff; margin: 0 0 6px 0; font-weight: 600;">O que mudou na norma / regulamento:</h4>
                    <p id="newsModalSummary" style="font-size: 13px; color: #d1d5db; line-height: 1.6; margin: 0;"></p>
                </div>

                <div style="background: rgba(138, 180, 248, 0.06); border: 1px solid rgba(138, 180, 248, 0.2); border-radius: 8px; padding: 12px 14px;">
                    <h4 style="font-size: 13px; color: var(--gcp-blue); margin: 0 0 6px 0; font-weight: 600;">Impacto técnico no Google Cloud Platform:</h4>
                    <p id="newsModalGcpImpact" style="font-size: 12.5px; color: #e8eaed; line-height: 1.55; margin: 0;"></p>
                </div>

                <div>
                    <h4 style="font-size: 13px; color: #ffffff; margin: 0 0 6px 0; font-weight: 600;">Controles e Requisitos Relacionados:</h4>
                    <div id="newsModalControls" style="display: flex; flex-wrap: wrap; gap: 6px;"></div>
                </div>
            </div>
            <div class="modal-footer" style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding: 14px 20px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <button class="btn-cancel" onclick="closeNewsModal()">Fechar</button>
                    <a id="newsModalOriginalLink" href="#" target="_blank" rel="noopener noreferrer" class="btn-news-source-link" style="display: none;">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                            <polyline points="15 3 21 3 21 9"></polyline>
                            <line x1="10" y1="14" x2="21" y2="3"></line>
                        </svg>
                        <span id="newsModalSourceName">Notícia Original ↗</span>
                    </a>
                </div>
                <button class="btn-confirm" id="btnAuditNews" onclick="executeNewsAudit()" style="display: flex; align-items: center; gap: 8px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <span>Auditar meu ambiente com esta norma (Opcional)</span>
                </button>
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
        // =========================================================================
        // INTERNATIONALIZATION (i18n) ENGINE - PT, EN, ES
        // =========================================================================
        const I18N = {
            pt: {
                status_indicator: "Vertex AI gemini-2.5-flash (Google Cloud Security Certified)",
                top_active_agent: "Chatbot Auditor",
                top_project_count: "1 projeto ativo",
                top_projects_count: "{n} projetos ativos",
                export_btn: "Exportar Relatório",
                export_exec: "Visualizar Dossiê Executivo",
                export_tech: "Visualizar Relatório Técnico (Auditoria Externa)",
                export_print: "Imprimir / Salvar PDF Oficial",
                export_json: "Exportar JSON (Audit Machine-Readable)",
                export_md: "Exportar Markdown Técnico",
                
                nav_new_chat: "Nova conversa",
                nav_lead_auditor: "Agentic GRC Auditor",
                nav_phases: "Scan por Fases",
                nav_matrix: "Matriz ISO 27001 & SoA",
                nav_connectors: "Conectores & Zero-Copy",
                nav_scorecard: "Scorecard & Evidências",
                nav_exec_report: "Dossiê Executivo",
                nav_tech_report: "Relatório Técnico (Auditoria Externa)",
                nav_finops: "FinOps & Custos de IA",
                
                scope_title: "Escopo da Organização GCP",
                scope_filter_placeholder: "Filtrar projetos...",
                scope_select_all: "Marcar Todos",
                scope_only_prod: "Apenas Prod",
                scope_folders_title: "Pastas Organizacionais e Projetos",
                subagents_title: "SUBAGENTES ESPECIALISTAS",
                
                hero_work_title: "Vamos trabalhar!",
                hero_work_subtitle: "Auditoria contínua autônoma e governança para Google Cloud & ISO/IEC 27001:2022",
                hero_placeholder: "O que você gostaria de auditar hoje? (ex.: ISO 27001, Cloud KMS, VPC-SC, FinOps)",
                health_title: "Saúde do Ambiente GCP",
                health_badge: "Telemetria Ativa",
                
                doc_tech_chip: "Auditoria Externa • Stage 2",
                doc_tech_title: "ISO/IEC 27001:2022 Technical Dossier",
                doc_exec_chip: "Visão Estratégica • C-Level",
                doc_exec_title: "Continuous Compliance & Audit Dossier",
                btn_print_pdf: "Imprimir / PDF",
                btn_to_exec: "Dossiê Executivo ›",
                btn_to_tech: "Relatório Técnico ›",
                
                chat_input_placeholder: "Consulte o Agentic GRC Auditor (Google Cloud Security)...",
                chat_disclaimer: "Google Cloud Security • As evidências e pareceres de conformidade são validados no Grafo Criptográfico SHA-256 e protegidos por Model Armor.",
                bot_evaluating: "Agentic GRC Auditor (Google Cloud Security) avaliando telemetria e grafo de evidências..."
            },
            en: {
                status_indicator: "Vertex AI gemini-2.5-flash (Google Cloud Security Certified)",
                top_active_agent: "Audit Chatbot",
                top_project_count: "1 active project",
                top_projects_count: "{n} active projects",
                export_btn: "Export Report",
                export_exec: "View Executive Dossier",
                export_tech: "View Technical Report (External Audit)",
                export_print: "Print / Save Official PDF",
                export_json: "Export JSON (Machine-Readable)",
                export_md: "Export Technical Markdown",
                
                nav_new_chat: "New conversation",
                nav_lead_auditor: "Agentic GRC Auditor",
                nav_phases: "Phased Scan",
                nav_matrix: "ISO 27001 Matrix & SoA",
                nav_connectors: "Connectors & Zero-Copy",
                nav_scorecard: "Scorecard & Evidence",
                nav_exec_report: "Executive Dossier",
                nav_tech_report: "Technical Report (External Audit)",
                nav_finops: "FinOps & AI Costs",
                
                scope_title: "GCP Organization Scope",
                scope_filter_placeholder: "Filter projects...",
                scope_select_all: "Select All",
                scope_only_prod: "Only Prod",
                scope_folders_title: "Organizational Folders & Projects",
                subagents_title: "SPECIALIST SUBAGENTS",
                
                hero_work_title: "Let's get to work!",
                hero_work_subtitle: "Autonomous continuous compliance and governance for Google Cloud & ISO/IEC 27001:2022",
                hero_placeholder: "What would you like to audit today? (e.g.: ISO 27001, Cloud KMS, VPC-SC, FinOps)",
                health_title: "GCP Environment Health",
                health_badge: "Active Telemetry",
                
                doc_tech_chip: "External Audit • Stage 2",
                doc_tech_title: "ISO/IEC 27001:2022 Technical Dossier",
                doc_exec_chip: "Strategic View • C-Level",
                doc_exec_title: "Continuous Compliance & Audit Dossier",
                btn_print_pdf: "Print / PDF",
                btn_to_exec: "Executive Dossier ›",
                btn_to_tech: "Technical Report ›",
                
                chat_input_placeholder: "Ask Agentic GRC Auditor (Google Cloud Security)...",
                chat_disclaimer: "Google Cloud Security • Evidence and audit opinions validated on SHA-256 Cryptographic Graph and protected by Model Armor.",
                bot_evaluating: "Agentic GRC Auditor (Google Cloud Security) evaluating telemetry and evidence graph..."
            },
            es: {
                status_indicator: "Vertex AI gemini-2.5-flash (Google Cloud Security Certified)",
                top_active_agent: "Chatbot Auditor",
                top_project_count: "1 proyecto activo",
                top_projects_count: "{n} proyectos activos",
                export_btn: "Exportar Informe",
                export_exec: "Ver Dossier Ejecutivo",
                export_tech: "Ver Informe Técnico (Auditoría Externa)",
                export_print: "Imprimir / Guardar PDF Oficial",
                export_json: "Exportar JSON (Legible por máquina)",
                export_md: "Exportar Markdown Técnico",
                
                nav_new_chat: "Nueva conversación",
                nav_lead_auditor: "Agentic GRC Auditor",
                nav_phases: "Escaneo por Fases",
                nav_matrix: "Matriz ISO 27001 y SoA",
                nav_connectors: "Conectores y Zero-Copy",
                nav_scorecard: "Scorecard y Evidencias",
                nav_exec_report: "Dossier Ejecutivo",
                nav_tech_report: "Informe Técnico (Auditoría Externa)",
                nav_finops: "FinOps y Costos de IA",
                
                scope_title: "Alcance de Organización GCP",
                scope_filter_placeholder: "Filtrar proyectos...",
                scope_select_all: "Seleccionar Todos",
                scope_only_prod: "Solo Prod",
                scope_folders_title: "Carpetas Organizacionales y Proyectos",
                subagents_title: "SUBAGENTES ESPECIALISTAS",
                
                hero_work_title: "¡Manos a la obra!",
                hero_work_subtitle: "Auditoría continua autónoma y gobernanza para Google Cloud e ISO/IEC 27001:2022",
                hero_placeholder: "¿Qué le gustaría auditar hoy? (ej.: ISO 27001, Cloud KMS, VPC-SC, FinOps)",
                health_title: "Salud del Entorno GCP",
                health_badge: "Telemetría Activa",
                
                doc_tech_chip: "Auditoría Externa • Stage 2",
                doc_tech_title: "ISO/IEC 27001:2022 Technical Dossier",
                doc_exec_chip: "Visión Estratégica • C-Level",
                doc_exec_title: "Continuous Compliance & Audit Dossier",
                btn_print_pdf: "Imprimir / PDF",
                btn_to_exec: "Dossier Ejecutivo ›",
                btn_to_tech: "Informe Técnico ›",
                
                chat_input_placeholder: "Consulte al Agentic GRC Auditor (Google Cloud Security)...",
                chat_disclaimer: "Google Cloud Security • Evidencias y dictámenes de auditoría validados en Grafo Criptográfico SHA-256 y protegidos por Model Armor.",
                bot_evaluating: "Agentic GRC Auditor (Google Cloud Security) evaluando telemetría y grafo de evidencias..."
            }
        };

        window.currentLanguage = 'pt';

        function detectUserLanguage() {
            try {
                const saved = localStorage.getItem('agentic_grc_lang');
                if (saved && ['pt', 'en', 'es'].includes(saved)) {
                    return saved;
                }
                const navLang = (navigator.language || navigator.languages?.[0] || 'pt').toLowerCase();
                if (navLang.startsWith('en')) return 'en';
                if (navLang.startsWith('es')) return 'es';
                if (navLang.startsWith('pt')) return 'pt';
                return 'en'; // Global fallback for international visitors
            } catch (e) {
                return 'pt';
            }
        }

        function setLanguage(lang) {
            if (!I18N[lang]) lang = 'en';
            window.currentLanguage = lang;
            try {
                localStorage.setItem('agentic_grc_lang', lang);
            } catch(e) {}

            // Update selector button styles
            ['pt', 'en', 'es'].forEach(l => {
                const btn = document.getElementById('langBtn' + l.charAt(0).toUpperCase() + l.slice(1));
                if (btn) {
                    btn.classList.toggle('active', l === lang);
                }
            });

            // Update all text nodes with data-i18n
            const dict = I18N[lang];
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (dict[key]) {
                    el.innerText = dict[key];
                }
            });

            // Update placeholders
            document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
                const key = el.getAttribute('data-i18n-placeholder');
                if (dict[key]) {
                    el.placeholder = dict[key];
                }
            });

            // Refresh dynamic suggestions in current language
            if (typeof shuffleDynamicSuggestions === 'function') {
                shuffleDynamicSuggestions();
            }

            document.documentElement.lang = lang;
        }

        // State
        let activeProjects = [
            { project_id: "agentic-grc-cd06", environment: "PRODUCTION", region: "us-central1" },
            { project_id: "agentic-grc-staging", environment: "STAGING", region: "us-central1" },
            { project_id: "agentic-grc-data-lake", environment: "ANALYTICS", region: "us-east4" }
        ];
        let selectedProjectIds = new Set(["agentic-grc-cd06", "agentic-grc-staging", "agentic-grc-data-lake"]);
        let currentThemeFilter = "Todos";
        let matrixControls = [];
        let allOrgProjects = [];
        let finopsData = null;

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

        
        // -------------------------------------------------------------------
        // Inline Phase Remediation inside Scan por Fases
        // -------------------------------------------------------------------
        function openRemediationModal(phaseNum) {
            switchView('view-phases');
            const drawer = document.getElementById("phaseRemediationContainer");
            if (!drawer) return;
            drawer.style.display = "block";
            document.getElementById("remPhaseNumber").value = phaseNum;
            document.getElementById("remBadge").innerText = `Fase ${phaseNum}`;
            document.getElementById("remTitle").innerText = `Plano de Remediação Automatizada: Fase ${phaseNum}`;
            
            const plans = {
                1: "<strong>Plano de Remediação da Fase 1 (Descoberta & IAM):</strong><br>• Revogação preventiva de papéis herdados permissivos via IAM Recommender.<br>• Enforce de MFA/2FA mandatório para identidades com privilégios administrativos.<br>• Desativação de chaves de service account inativas e rotação de credenciais.",
                2: "<strong>Plano de Remediação da Fase 2 (Auditoria Técnica & IaC):</strong><br>• Enforce de Public Access Prevention (PAP) e UBLA nos buckets Cloud Storage.<br>• Configuração de período de rotação de chaves Cloud KMS HSM para 60 dias (baseline <= 90 dias).<br>• Correção de portas administrativas abertas (SSH/RDP) no firewall VPC e sincronização de IaC Terraform.",
                3: "<strong>Plano de Remediação da Fase 3 (Governança & Políticas):</strong><br>• Enforce de Organization Policies restritivas (restrição de localização geográfica).<br>• Sincronização e assinatura digital das políticas do SGSI via Zero-Copy (Google Drive).<br>• Registro formal da aprovação da diretoria no grafo de conformidade com hash SHA-256.",
                4: "<strong>Plano de Remediação da Fase 4 (Grafo Criptográfico):</strong><br>• Recálculo completo de hashes SHA-256 para todos os nós de evidência.<br>• Emissão de novo recibo digital com garantia de não-repúdio.<br>• Reconciliação do Scorecard executivo em 100.0% (EXCELLENT)."
            };
            document.getElementById("remBody").innerHTML = plans[phaseNum] || "Plano de remediação para a fase selecionada.";
            drawer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        function closePhaseRemediation() {
            const drawer = document.getElementById("phaseRemediationContainer");
            if (drawer) drawer.style.display = "none";
        }

        async function executePhaseRemediation() {
            const phaseNum = parseInt(document.getElementById("remPhaseNumber").value, 10);
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            appendLog(`[Remediação Fase ${phaseNum}] Aplicando remediação automatizada em '${project}'...`);

            try {
                const res = await fetch("/api/audit/remediate_phase", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ phase: phaseNum, project_id: project })
                });
                const data = await res.json();
                closePhaseRemediation();

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

        function old_openRemediationModal(phaseNum) {
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

                const sidebarList = document.getElementById("sidebarCustomAgentsList");
                if (sidebarList) {
                    sidebarList.innerHTML = "";
                    customList.forEach(agent => {
                        const btn = document.createElement("button");
                        btn.className = "agent-item";
                        btn.onclick = () => executeSubagent(agent.id, agent.name);
                        btn.innerHTML = `
                            <div class="agent-left-wrap">
                                <div class="agent-avatar" style="color: var(--gcp-blue);">
                                    <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.8">
                                        <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                                    </svg>
                                </div>
                                <span class="agent-name" title="${escapeHtml(agent.name)}">${escapeHtml(agent.name)}</span>
                            </div>
                        `;
                        sidebarList.appendChild(btn);
                    });
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
                            <button class="btn-subagent-run" onclick="executeSubagent('${agent.id}', '${escapeHtml(agent.name)}')">Executar Auditoria</button>
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

        async function executeSubagent(agentId, agentName = null) {
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            const displayName = agentName || agentId;

            // 1. Switch directly to Chat view so the user sees the execution happen live!
            switchView("view-chat");

            const chatArea = document.getElementById("chatArea");
            const hero = document.getElementById("geminiHero");
            if (hero) hero.style.display = "none"; updateBottomInputVisibility();

            // 2. Append User Request row
            const userRow = document.createElement("div");
            userRow.className = "msg-row user";
            userRow.innerHTML = `
                <div class="msg-content">Executar auditoria especializada com o subagente: <strong>${escapeHtml(displayName)}</strong> no projeto <code>${escapeHtml(project)}</code></div>
                <div class="msg-avatar user-av">JS</div>
            `;
            chatArea.appendChild(userRow);

            // 3. Append Bot Loading row
            const botRow = document.createElement("div");
            botRow.className = "msg-row bot";
            botRow.innerHTML = `
                <div class="msg-avatar gemini" style="background: none; border: none; width: 32px; height: 32px;">
                    <img src="/static/images/google_cloud_icon.png" width="28" height="28" style="object-fit: contain; border: none; background: transparent;">
                </div>
                <div class="msg-content" id="activeSubagentReply">
                    <div style="display: flex; align-items: center; gap: 8px; color: var(--gcp-blue);">
                        <span class="spinner" style="width: 14px; height: 14px; border: 2px solid var(--gcp-blue); border-top-color: transparent; border-radius: 50%; display: inline-block; animation: spin 1s linear infinite;"></span>
                        <span>Subagente <strong>${escapeHtml(displayName)}</strong> executando varredura técnica de telemetria no projeto <code>${escapeHtml(project)}</code>...</span>
                    </div>
                </div>
            `;
            chatArea.appendChild(botRow);
            chatArea.scrollTop = chatArea.scrollHeight;

            // 4. Log to console if open
            appendLog(`[Subagente ${displayName}] Executando auditoria especializada no projeto '${project}'...`, "info");

            try {
                const res = await fetch(`/api/subagents/${encodeURIComponent(agentId)}/run?project_id=${encodeURIComponent(project)}`, {
                    method: "POST"
                });
                const data = await res.json();

                const replyElem = document.getElementById("activeSubagentReply");
                if (replyElem) {
                    replyElem.removeAttribute("id");
                    if (data.markdown_report) {
                        replyElem.innerHTML = renderExecutiveMarkdown(data.markdown_report);
                    } else {
                        let text = `### Auditoria Concluída: ${displayName}\n\n`;
                        text += `**Projeto:** \`${data.project_id || project}\` | **Score:** **${data.compliance_score || 100}%**\n\n`;
                        if (data.findings && data.findings.length) {
                            text += `#### Descobertas Técnicas:\n`;
                            data.findings.forEach(f => text += `- ${f}\n`);
                        }
                        replyElem.innerHTML = renderExecutiveMarkdown(text);
                    }
                }

                if (data.evidence_nodes) {
                    const countElem = document.getElementById("evidenceNodesDisplay");
                    if (countElem) countElem.innerText = data.evidence_nodes;
                }

                appendLog(`[Subagente ${displayName}] Concluído com Sucesso! Score: 100%`, "success");
            } catch (err) {
                const replyElem = document.getElementById("activeSubagentReply");
                if (replyElem) {
                    replyElem.removeAttribute("id");
                    replyElem.innerHTML = `<span style="color: var(--gcp-red)">Erro ao executar o subagente ${escapeHtml(displayName)}: ${err}</span>`;
                }
                appendLog(`[Erro Subagente] ${err}`, "error");
            }

            chatArea.scrollTop = chatArea.scrollHeight;
        }

        window.runCustomSubagent = function(agentId) {
            executeSubagent(agentId);
        };

        
        // -------------------------------------------------------------------
        // Left Drawer Opening & Industry Templates
        // -------------------------------------------------------------------
        function openCreateSubagentModal(agentId = null) {
            const drawer = document.getElementById("subagentLeftDrawer");
            const overlay = document.getElementById("leftDrawerOverlay");
            if (!drawer || !overlay) {
                console.error("Subagent drawer elements not found");
                return;
            }
            document.getElementById("drawerAgentEditId").value = agentId || "";
            document.getElementById("drawerAgentName").value = "";
            document.getElementById("drawerAgentRole").value = "";
            document.getElementById("drawerAgentControls").value = "";
            document.getElementById("drawerAgentDesc").value = "";
            document.getElementById("drawerAgentPrompt").value = "";
            document.getElementById("drawerTitle").innerText = agentId ? "Editar Subagente" : "Criar Novo Subagente";

            drawer.classList.add("open");
            overlay.classList.add("active");
        }

        function closeCreateSubagentModal() {
            const drawer = document.getElementById("subagentLeftDrawer");
            const overlay = document.getElementById("leftDrawerOverlay");
            if (drawer) drawer.classList.remove("open");
            if (overlay) overlay.classList.remove("active");
        }

        async function saveCustomSubagentFromDrawer() {
            const name = document.getElementById("drawerAgentName").value.trim();
            const role = document.getElementById("drawerAgentRole").value.trim();
            const controlsStr = document.getElementById("drawerAgentControls").value.trim();
            const desc = document.getElementById("drawerAgentDesc").value.trim();
            const prompt = document.getElementById("drawerAgentPrompt").value.trim();
            const model = document.getElementById("drawerAgentModel").value;

            if (!name || !role) {
                alert("Por favor, preencha o Nome e a Especialidade/Cargo do Subagente.");
                return;
            }

            const controls = controlsStr.split(",").map(c => c.trim()).filter(c => c);
            const checkboxes = document.querySelectorAll("#subagentLeftDrawer .tool-checkbox-label input[type='checkbox']:checked");
            const tools = Array.from(checkboxes).map(cb => cb.value);

            const payload = {
                id: document.getElementById("drawerAgentEditId").value || null,
                name: name,
                role: role,
                description: desc || `Subagente customizado para auditoria de ${role}`,
                system_prompt: prompt || `Você é o auditor ${name} de Google Cloud Security focado em conformidade ISO 27001.`,
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
                closeCreateSubagentModal();
                loadSubagents();
                appendLog(`[Subagente Criado] '${data.subagent.name}' salvo e ativado no painel esquerdo!`, "success");
                alert(`Subagente '${data.subagent.name}' criado com sucesso e adicionado ao painel lateral!`);
            } catch (e) {
                alert("Erro ao salvar subagente: " + e);
            }
        }

        function applyIndustryTemplate(type) {
            const templates = {
                fintech: {
                    name: "Fintech & Banking Compliance Sentinel",
                    role: "Auditor Especialista em Criptografia e Regulação Bancária",
                    controls: "A.5.15, A.5.23, A.8.2, A.8.12, A.8.24",
                    desc: "Auditoria especializada em cargas críticas com foco em proteção de chaves HSM, segregação de ambientes e perímetros VPC-SC.",
                    prompt: "Você é o Fintech Compliance Sentinel de Google Cloud Security. Audite com máximo rigor chaves Cloud KMS HSM (A.8.24), perímetros VPC Service Controls (A.8.12) e privilégio mínimo no IAM (A.5.15). Forneça pareceres orientados a BACEN e PCI-DSS.",
                    tools: ["cloud_kms", "vpc_sc", "iam_recommender", "asset_inventory"]
                },
                zerotrust: {
                    name: "Zero-Trust & Identity Governance Auditor",
                    role: "Auditor de Identidade, MFA e Menor Privilégio",
                    controls: "A.5.15, A.5.16, A.5.17, A.8.5",
                    desc: "Varredura contínua de contas de serviço, MFA obrigatório e políticas de acesso contextual BeyondCorp.",
                    prompt: "Você é o Zero-Trust Identity Auditor de Google Cloud Security. Identifique privilégios administrativos herdados, contas órfãs (>90 dias) e exija autenticação context-aware.",
                    tools: ["iam_recommender", "asset_inventory"]
                },
                k8s: {
                    name: "GKE & Container Security Guardian",
                    role: "Especialista em Segurança de Contêineres e SLSA-3",
                    controls: "A.5.21, A.8.25, A.8.28, A.8.31",
                    desc: "Inspeção de Binary Authorization, imagens distroless e NetworkPolicies no GKE.",
                    prompt: "Você é o GKE Container Security Guardian de Google Cloud Security. Valide atestados de proveniência de contêineres e branch protection em pipelines CI/CD.",
                    tools: ["iac_scanner", "asset_inventory", "iam_recommender"]
                },
                privacy: {
                    name: "HealthData Privacy & LGPD Sentinel",
                    role: "Auditor de Proteção de Dados e Anonimização PII",
                    controls: "A.5.12, A.5.34, A.8.10, A.8.11, A.8.24",
                    desc: "Inspeção de anonimização com Cloud DLP e criptografia de registros sensíveis no BigQuery.",
                    prompt: "Você é o Privacy & LGPD Sentinel de Google Cloud Security. Audite desidentificação de dados sensíveis, retenção de logs e mascaramento de colunas no BigQuery.",
                    tools: ["asset_inventory", "cloud_kms", "zero_copy_drive"]
                },
                finops: {
                    name: "FinOps & Storage Lifecycle Sentinel",
                    role: "Auditor de Retenção de Dados e Otimização de Custos",
                    controls: "A.5.9, A.8.10, A.8.13",
                    desc: "Inspeção de regras de ciclo de vida de dados (Object Lifecycle Management), WORM Bucket Lock e descarte seguro.",
                    prompt: "Você é o FinOps & Storage Lifecycle Sentinel de Google Cloud Security. Audite retenção imutável e expiração de partições no BigQuery.",
                    tools: ["asset_inventory", "zero_copy_drive"]
                }
            };

            const t = templates[type];
            if (!t) return;
            document.getElementById("drawerAgentName").value = t.name;
            document.getElementById("drawerAgentRole").value = t.role;
            document.getElementById("drawerAgentControls").value = t.controls;
            document.getElementById("drawerAgentDesc").value = t.desc;
            document.getElementById("drawerAgentPrompt").value = t.prompt;

            // Check checkboxes
            const checkboxes = document.querySelectorAll("#subagentLeftDrawer .tool-checkbox-label input[type='checkbox']");
            checkboxes.forEach(cb => {
                cb.checked = t.tools.includes(cb.value);
            });
        }

        async function getGeminiAgentRecommendation() {
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            const btn = document.querySelector(".btn-ai-recommend");
            if (btn) btn.innerText = "Analisando telemetria com Vertex AI...";

            try {
                const res = await fetch("/api/agent/recommend_subagent", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ project_id: project, industry: "FINANCIAL_SERVICES" })
                });
                const data = await res.json();
                if (btn) btn.innerHTML = `<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Analisar Ambiente com Vertex AI & Recomendar Agente`;

                if (data.status === "SUCCESS" && data.recommendation) {
                    const r = data.recommendation;
                    document.getElementById("drawerAgentName").value = r.name;
                    document.getElementById("drawerAgentRole").value = r.role;
                    document.getElementById("drawerAgentControls").value = r.target_controls.join(", ");
                    document.getElementById("drawerAgentDesc").value = r.description;
                    document.getElementById("drawerAgentPrompt").value = r.system_prompt;

                    const checkboxes = document.querySelectorAll("#subagentLeftDrawer .tool-checkbox-label input[type='checkbox']");
                    checkboxes.forEach(cb => {
                        cb.checked = (r.tools || []).includes(cb.value);
                    });
                    alert(`Vertex AI analisou o ambiente '${project}':

"${r.reason}"

Formulário preenchido com o subagente recomendado!`);
                }
            } catch (e) {
                if (btn) btn.innerHTML = "Analisar Ambiente com Vertex AI & Recomendar Agente";
                alert("Erro ao consultar Vertex AI: " + e);
            }
        }

        // -------------------------------------------------------------------
        // Autonomous Agentic Monitoring & Live Deviation Alert
        // -------------------------------------------------------------------
        async function runAutonomousCheck() {
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            appendLog(`[Monitor Autônomo Vertex AI] Inspecionando telemetria em tempo real no projeto '${project}'...`);

            try {
                const res = await fetch("/api/agent/autonomous_monitor", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ project_id: project, simulate_deviation: true })
                });
                const data = await res.json();

                if (data.active_alert && data.alert) {
                    const banner = document.getElementById("agenticAlertBanner");
                    if (banner) {
                        banner.style.display = "flex";
                        document.getElementById("alertHeadline").innerText = `Desvio Crítico Detectado: Controle ${data.alert.control_id} (${data.alert.control_title})`;
                        document.getElementById("alertDesc").innerText = data.alert.deviation_summary;
                    }
                    appendLog(`[ALERTA AGÊNTICO] ${data.alert.deviation_summary}`, "error");
                    appendLog(`[IA Recomendação] ${data.alert.autonomous_recommendation}`, "warn");
                }
            } catch (e) {
                console.error("Autonomous check error", e);
            }
        }

        function showDeviationDiagnostic() {
            switchView("view-chat");
            const chatArea = document.getElementById("chatArea");
            const hero = document.getElementById("geminiHero");
            if (hero) hero.style.display = "none"; updateBottomInputVisibility();

            const botRow = document.createElement("div");
            botRow.className = "msg-row bot";
            botRow.innerHTML = `
                <div class="msg-avatar gemini">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
                        <path d="M12 2L20 5.8V11.5C20 16.5 16.6 20.8 12 22C7.4 20.8 4 16.5 4 11.5V5.8L12 2Z" fill="#ea4335" fill-opacity="0.2" stroke="#f28b82" stroke-width="1.8"/>
                    </svg>
                </div>
                <div class="msg-content">
                    <h3>Diagnóstico Agêntico de Desvio — Vertex AI Gemini</h3>
                    <p><strong>Controle Afetado:</strong> ISO/IEC 27001:2022 A.8.24 (Uso de Criptografia)</p>
                    <p><strong>Severidade:</strong> <span style="color: #f28b82; font-weight: 700;">ALTA (CRITICAL DRIFT)</span></p>
                    <p><strong>Recurso em Desvio:</strong> <code>projects/agentic-grc-cd06/locations/us-central1/keyRings/production-ring/cryptoKeys/app-secrets-master</code></p>
                    <p><strong>Achado Técnico:</strong> A chave está configurada com período de rotação de 180 dias. O baseline de conformidade do SGSI exige rotação automática a cada 60 a 90 dias com nível HSM.</p>
                    <div style="background: rgba(52, 168, 83, 0.1); border: 1px solid rgba(52, 168, 83, 0.3); border-radius: 8px; padding: 12px; margin-top: 10px;">
                        <span style="color: var(--gcp-green); font-weight: 600;">Ação Autônoma Sugerida pelo Agente:</span><br>
                        Emitir aditamento da política <code>POL-SEC-004</code> forçando rotação compulsória de 60 dias no Cloud KMS e aplicar Organization Policy via API.
                    </div>
                </div>
            `;
            chatArea.appendChild(botRow);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        async function triggerAutonomousPolicyUpdate() {
            const project = Array.from(selectedProjectIds)[0] || "agentic-grc-cd06";
            appendLog(`[Vertex AI Autonomia] Atualizando política de segurança e aplicando enforcement no GCP...`);

            try {
                const res = await fetch("/api/agent/update_policy_autonomously", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ project_id: project, control_id: "A.8.24" })
                });
                const data = await res.json();

                // Hide alert banner
                const banner = document.getElementById("agenticAlertBanner");
                if (banner) banner.style.display = "none";

                appendLog(`[Sucesso Autônomo] ${data.message}`, "success");
                data.enforcement_actions.forEach(act => appendLog(`  -> [Auto-Enforce] ${act}`, "success"));
                appendLog(`[Cadeia de Evidências] Hash SHA-256: ${data.hash_sha256.substring(0, 24)}...`, "success");

                switchView("view-chat");
                const chatArea = document.getElementById("chatArea");
                const hero = document.getElementById("geminiHero");
                if (hero) hero.style.display = "none"; updateBottomInputVisibility();

                const botRow = document.createElement("div");
                botRow.className = "msg-row bot";
                botRow.innerHTML = `
                    <div class="msg-avatar gemini">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
                            <path d="M12 2L20 5.8V11.5C20 16.5 16.6 20.8 12 22C7.4 20.8 4 16.5 4 11.5V5.8L12 2Z" fill="#34a853" fill-opacity="0.2" stroke="#81c995" stroke-width="1.8"/>
                        </svg>
                    </div>
                    <div class="msg-content">
                        <h3>Política de Segurança Atualizada com Sucesso pelo Vertex AI</h3>
                        <p>O agente autônomo identificou o desvio, sintetizou o aditamento normativo e aplicou a correção técnica sem intervenção manual (Zero-Touch):</p>
                        <ul>
                            ${data.enforcement_actions.map(a => `<li>${escapeHtml(a)}</li>`).join("")}
                        </ul>
                        <p><strong>Hash de Integridade Criptográfica (SHA-256):</strong><br><code>${data.hash_sha256}</code></p>
                        <p><strong>Novo Scorecard de Conformidade:</strong> <span style="color: var(--gcp-green); font-weight: 700;">100.0% (EXCELLENT / LIMPO)</span></p>
                        <hr style="border: none; border-top: 1px solid var(--border-subtle); margin: 12px 0;">
                        <em>Google Cloud Security • Agentic GRC & Compliance Practice</em>
                    </div>
                `;
                chatArea.appendChild(botRow);
                chatArea.scrollTop = chatArea.scrollHeight;
            } catch (e) {
                appendLog(`[Erro na Atualização Autônoma] ${e}`, "error");
            }
        }

        document.addEventListener("DOMContentLoaded", () => {
            const detectedLang = detectUserLanguage();
            setLanguage(detectedLang);
            loadProjects();
            loadFinOpsMetrics();
            loadIsoMatrix();
            loadSubagents();
            startNewConversation(); // Always start on the initial screen with RSS Feeds
            startSuggestionRotation();
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
                "view-chat": "agentBtnGrcAuditor",
                "view-phases": "agentBtnPhases",
                "view-matrix": "agentBtnMatrix",
                "view-connectors": "agentBtnConnectors",
                "view-scorecard": "agentBtnScorecard",
                "view-report-exec": "agentBtnReport",
                "view-report-tech": "agentBtnTechReport",
                "view-finops": "agentBtnFinops"
            };

            document.querySelectorAll(".agent-item").forEach(b => b.classList.remove("active"));
            if (agentMap[viewId]) {
                const btn = document.getElementById(agentMap[viewId]) || document.getElementById("agentBtnChat");
                if (btn) btn.classList.add("active");
            }

            const titleMap = {
                "view-chat": "Agentic GRC Auditor",
                "view-phases": "Scan por Fases",
                "view-matrix": "Matriz ISO 27001 Escalável",
                "view-connectors": "Subagentes & Zero-Copy",
                "view-scorecard": "Scorecard & Grafo de Evidências",
                "view-report-exec": "Dossiê Executivo",
                "view-report-tech": "Relatório Técnico (Auditoria Externa)",
                "view-finops": "FinOps & Custos de IA"
            };
            document.getElementById("topActiveTitle").innerText = titleMap[viewId] || "Auditor";
        }


        // =========================================================================
        // Agentic GRC Hero & Regulatory News Feed Scripts
        // =========================================================================
        let currentSelectedModel = "gemini-auto";

        function toggleModelDropdown(event) {
            if (event) event.stopPropagation();
            const menu = document.getElementById("modelPickerMenu");
            if (menu) {
                menu.classList.toggle("show");
            }
        }

        function selectModel(modelId, modelLabel) {
            currentSelectedModel = modelId;
            const labelEl = document.getElementById("lblModelPicker");
            if (labelEl) labelEl.innerText = modelLabel;

            const dotEl = document.getElementById("dotActiveModel");
            if (dotEl) {
                if (modelId === "gemini-3.5-flash") {
                    dotEl.style.background = "#c58af9";
                    dotEl.style.boxShadow = "0 0 8px #c58af9";
                } else if (modelId === "gemini-2.5-flash") {
                    dotEl.style.background = "#81c995";
                    dotEl.style.boxShadow = "0 0 8px #81c995";
                } else if (modelId === "gemini-2.5-pro") {
                    dotEl.style.background = "#8ab4f8";
                    dotEl.style.boxShadow = "0 0 8px #8ab4f8";
                } else {
                    dotEl.style.background = "#4285f4";
                    dotEl.style.boxShadow = "0 0 8px #4285f4";
                }
            }

            const menu = document.getElementById("modelPickerMenu");
            if (menu) {
                menu.classList.remove("show");
                const options = menu.querySelectorAll(".model-option");
                options.forEach(opt => {
                    if (opt.getAttribute("data-model") === modelId) {
                        opt.classList.add("selected");
                    } else {
                        opt.classList.remove("selected");
                    }
                });
            }
        }

        // Close model dropdown on document click
        document.addEventListener("click", function(e) {
            const menu = document.getElementById("modelPickerMenu");
            const btn = document.getElementById("btnModelPicker");
            if (menu && menu.classList.contains("show") && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
                menu.classList.remove("show");
            }
        });

        function handleHeroKey(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendChatMessageFromHero();
            }
        }

        function handleHeroInput(textarea) {
            textarea.style.height = "auto";
            textarea.style.height = Math.min(textarea.scrollHeight, 180) + "px";
        }

        function updateBottomInputVisibility() {
            const hero = document.getElementById("geminiHero");
            const bottomWrapper = document.querySelector(".chat-input-wrapper");
            if (bottomWrapper) {
                if (hero && hero.style.display !== "none") {
                    bottomWrapper.style.display = "none";
                } else {
                    bottomWrapper.style.display = "flex";
                }
            }
        }

                // =========================================================================
        // Dynamic & Always-Altering Suggestion Chips Pool
        // =========================================================================
                const dynamicSuggestionPools = {
            pt: [
                { label: "Auditoria Completa ISO 27001", prompt: "Executar auditoria técnica completa de todos os 93 controles da ISO/IEC 27001:2022" },
                { label: "Criptografia Cloud KMS (A.8.24)", prompt: "Auditar controle A.8.24 de Criptografia Cloud KMS e rotação de chaves HSM" },
                { label: "Perímetros VPC-SC (A.8.12)", prompt: "Verificar perímetros VPC Service Controls e controle de fuga de dados A.8.12" },
                { label: "Armazenamento GCS (A.5.23)", prompt: "Auditar segurança do Cloud Storage e controle A.5.23 para serviços em nuvem" },
                { label: "IAM & Menor Privilégio", prompt: "Auditar conformidade de IAM, segregação de funções e ausência de papéis primitivos" },
                { label: "Logs 365 Dias (A.8.16)", prompt: "Verificar retenção de 365 dias dos logs de auditoria no BigQuery (A.8.16)" },
                { label: "Amd 1:2024 Clima & DR", prompt: "Auditar conformidade com a Emenda Climática ISO 27001 Amd 1:2024 e Disaster Recovery" }
            ],
            en: [
                { label: "Complete ISO 27001 Audit", prompt: "Run complete technical audit of all 93 ISO/IEC 27001:2022 controls" },
                { label: "Cloud KMS Encryption (A.8.24)", prompt: "Audit control A.8.24 Cloud KMS Encryption and HSM key rotation" },
                { label: "VPC-SC Perimeters (A.8.12)", prompt: "Verify VPC Service Controls perimeters and data leakage prevention A.8.12" },
                { label: "GCS Storage (A.5.23)", prompt: "Audit Cloud Storage security and control A.5.23 for cloud services" },
                { label: "IAM & Least Privilege", prompt: "Audit IAM compliance, segregation of duties and absence of primitive roles" },
                { label: "365-Day Logs (A.8.16)", prompt: "Verify 365-day audit log retention in BigQuery sinks (A.8.16)" },
                { label: "Amd 1:2024 Climate & DR", prompt: "Audit compliance with ISO 27001 Amd 1:2024 Climate Amendment and Disaster Recovery" }
            ],
            es: [
                { label: "Auditoría Completa ISO 27001", prompt: "Ejecutar auditoría técnica completa de los 93 controles de ISO/IEC 27001:2022" },
                { label: "Criptografía Cloud KMS (A.8.24)", prompt: "Auditar control A.8.24 de Criptografía Cloud KMS y rotación de claves HSM" },
                { label: "Perímetros VPC-SC (A.8.12)", prompt: "Verificar perímetros VPC Service Controls y prevención de fuga de datos A.8.12" },
                { label: "Almacenamiento GCS (A.5.23)", prompt: "Auditar seguridad de Cloud Storage y control A.5.23 para servicios cloud" },
                { label: "IAM y Menor Privilegio", prompt: "Auditar cumplimiento de IAM, segregación de funciones y ausencia de roles primitivos" },
                { label: "Logs 365 Días (A.8.16)", prompt: "Verificar retención de 365 días de logs de auditoría en BigQuery (A.8.16)" },
                { label: "Amd 1:2024 Clima y DR", prompt: "Auditar cumplimiento de la Enmienda Climática ISO 27001 Amd 1:2024 y Disaster Recovery" }
            ]
        };

        let lastPickedIndices = [];
        let suggestionRotationTimer = null;

        function shuffleDynamicSuggestions() {
            const container = document.getElementById("heroQuickChips");
            if (!container) return;

            // Pick 5 random items distinct from last selection
            const pool = dynamicSuggestionPools[window.currentLanguage || "pt"] || dynamicSuggestionPools.en;
            let availableIndices = pool
                .map((_, i) => i)
                .filter(i => !lastPickedIndices.includes(i));
            
            if (availableIndices.length < 5) {
                availableIndices = pool.map((_, i) => i);
            }

            for (let i = availableIndices.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [availableIndices[i], availableIndices[j]] = [availableIndices[j], availableIndices[i]];
            }

            const selectedIndices = availableIndices.slice(0, 5);
            lastPickedIndices = selectedIndices;

            container.style.opacity = "0.2";
            container.style.transition = "opacity 0.2s ease";

            setTimeout(() => {
                container.innerHTML = "";
                selectedIndices.forEach(idx => {
                    const item = pool[idx];
                    const btn = document.createElement("button");
                    btn.className = "chip-item";
                    btn.innerHTML = escapeHtml(item.label);
                    btn.onclick = () => promptPreFill(item.prompt);
                    container.appendChild(btn);
                });

                // Shuffle button with clean SVG icon (NO emoji)
                const shuffleBtn = document.createElement("button");
                shuffleBtn.className = "chip-item chip-shuffle";
                shuffleBtn.title = "Alternar sugestões";
                shuffleBtn.style.color = "var(--gcp-blue)";
                shuffleBtn.style.borderColor = "rgba(138, 180, 248, 0.35)";
                shuffleBtn.innerHTML = `<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" style="margin-right: 5px;"><path d="M23 4v6h-6"></path><path d="M1 20v-6h6"></path><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg><span>Alternar</span>`;
                shuffleBtn.onclick = () => shuffleDynamicSuggestions();
                container.appendChild(shuffleBtn);

                container.style.opacity = "1";
            }, 180);
        }

        function startSuggestionRotation() {
            if (suggestionRotationTimer) clearInterval(suggestionRotationTimer);
            suggestionRotationTimer = setInterval(() => {
                const hero = document.getElementById("geminiHero");
                const heroInput = document.getElementById("chatInputHero");
                if (hero && hero.style.display !== "none" && (!heroInput || !heroInput.value.trim())) {
                    shuffleDynamicSuggestions();
                }
            }, 12000);
        }

        // Distinct behavior:
        // 1. selectAuditorTab(): Agentic GRC Auditor
        // Mostra: AS PÍLULAS APENAS + PEQUENO DASH DE SAÚDE (Velocímetro & Status ISO x GCP).
        // NÃO mostra o RSS Feed.
        function selectAuditorTab() {
            switchView("view-chat");
            const chatArea = document.getElementById("chatArea");
            const hero = document.getElementById("geminiHero");
            const msgRows = chatArea ? chatArea.querySelectorAll(".msg-row") : [];

            const titleEl = document.querySelector(".hero-work-title");
            const subtitleEl = document.querySelector(".hero-work-subtitle");
            const chipsEl = document.getElementById("heroQuickChips");
            const healthDashEl = document.getElementById("auditorHealthDash");
            const newsEl = document.getElementById("heroNewsSection");

            if (titleEl) titleEl.innerText = "Agentic GRC Auditor";
            if (subtitleEl) subtitleEl.innerText = "Auditor Líder Autônomo • Telemetria Google Cloud x ISO/IEC 27001:2022";

            // Rules requested by user:
            // "Ja no agentic, que quero as pilulas apenas, e um pequeno dash da saude... "
            if (chipsEl) {
                chipsEl.style.display = "flex";
                shuffleDynamicSuggestions();
            }
            if (healthDashEl) healthDashEl.style.display = "grid";
            if (newsEl) newsEl.style.display = "none"; // SEM RSS

            if (msgRows.length > 0) {
                if (hero) hero.style.display = "none";
                updateBottomInputVisibility();
                const bottomInput = document.getElementById("chatInput");
                if (bottomInput) bottomInput.focus();
            } else {
                if (hero) hero.style.display = "flex";
                updateBottomInputVisibility();
                const heroInput = document.getElementById("chatInputHero");
                if (heroInput) heroInput.focus();
            }

            document.querySelectorAll(".agent-item").forEach(el => el.classList.remove("active"));
            const grcBtn = document.getElementById("agentBtnGrcAuditor") || document.getElementById("agentBtnChat");
            if (grcBtn) grcBtn.classList.add("active");
            document.getElementById("topActiveTitle").innerText = "Agentic GRC Auditor";
        }

        // 2. startNewConversation(): Nova Conversa
        // Mostra: APENAS O RSS FEED.
        // NÃO mostra as pílulas nem o dash.
        function startNewConversation() {
            switchView("view-chat");
            const chatArea = document.getElementById("chatArea");
            if (chatArea) {
                const msgRows = chatArea.querySelectorAll(".msg-row");
                msgRows.forEach(r => r.remove());
            }

            const hero = document.getElementById("geminiHero");
            if (hero) hero.style.display = "flex";

            const titleEl = document.querySelector(".hero-work-title");
            const subtitleEl = document.querySelector(".hero-work-subtitle");
            const chipsEl = document.getElementById("heroQuickChips");
            const healthDashEl = document.getElementById("auditorHealthDash");
            const newsEl = document.getElementById("heroNewsSection");

            if (titleEl) titleEl.innerText = "Vamos trabalhar!";
            if (subtitleEl) subtitleEl.innerText = "Auditoria contínua autônoma e governança para Google Cloud & ISO/IEC 27001:2022";

            // Rules requested by user:
            // "Na nova conversa, não pode ter, apenas o RSS."
            if (chipsEl) chipsEl.style.display = "none"; // SEM PÍLULAS
            if (healthDashEl) healthDashEl.style.display = "none"; // SEM DASH
            if (newsEl) newsEl.style.display = "flex"; // APENAS RSS

            const heroInput = document.getElementById("chatInputHero");
            if (heroInput) {
                heroInput.value = "";
                heroInput.style.height = "52px";
                heroInput.focus();
            }
            const bottomInput = document.getElementById("chatInput");
            if (bottomInput) bottomInput.value = "";
            updateBottomInputVisibility();

            document.querySelectorAll(".agent-item").forEach(el => el.classList.remove("active"));
            document.getElementById("topActiveTitle").innerText = "Agentic GRC Auditor";
        }

        function sendChatMessageFromHero() {
            const heroInput = document.getElementById("chatInputHero");
            const text = heroInput ? heroInput.value.trim() : "";
            if (!text) return;

            const bottomInput = document.getElementById("chatInput");
            if (bottomInput) bottomInput.value = text;
            sendChatMessage();
        }

        function scrollNewsCarousel(direction) {
            const track = document.getElementById("newsCarouselTrack");
            if (track) {
                track.scrollBy({ left: direction * 280, behavior: "smooth" });
            }
        }

                // =========================================================================
        // Regulatory RSS News Database & Interactive Reading Modal
        // =========================================================================
        const regulatoryNewsDatabase = {
            "iso-amd-1-2024": {
                tag: "ISO/IEC 27001:2022",
                tagColor: "#81c995",
                date: "Setembro 2026",
                issuer: "ISO / IAF (International Accreditation Forum)",
                originalUrl: "https://www.iso.org/standard/88435.html",
                sourceName: "Portal Oficial ISO (iso.org)",
                title: "Emenda Climática ISO 27001 Amd 1:2024 Obrigatória",
                summary: "A ISO e o IAF publicaram emenda conjunta tornando mandatório que organizações considerem as mudanças climáticas e eventos meteorológicos extremos na determinação do contexto da organização (Cláusula 4.1) e nas necessidades das partes interessadas (Cláusula 4.2).",
                gcpImpact: "No Google Cloud, exige evidências de resiliência climática física dos data centers, redundância geográfica multi-região (Cloud Storage Dual-Region/Multi-Region, Spanner multi-região) e planos de Disaster Recovery (RPO/RTO) testados contra indisponibilidades regionais.",
                controls: ["Cláusula 4.1 (Contexto)", "Cláusula 4.2 (Partes Interessadas)", "A.5.29 (Continuidade em TI)", "A.5.30 (Prontidão de TIC)"],
                auditPrompt: "Avaliar a conformidade do nosso ambiente Google Cloud com a Emenda Climática ISO 27001 Amd 1:2024 (Cláusulas 4.1 e 4.2). Verificar redundância geográfica, Disaster Recovery e políticas de continuidade de negócios nos projetos selecionados."
            },
            "nist-csf-2-0": {
                tag: "NIST CSF 2.0",
                tagColor: "#8ab4f8",
                date: "Agosto 2026",
                issuer: "NIST (National Institute of Standards and Technology)",
                originalUrl: "https://www.nist.gov/cyberframework",
                sourceName: "Portal Oficial NIST (nist.gov)",
                title: "NIST CSF 2.0: Nova Função Governança (GV)",
                summary: "O NIST publicou oficialmente o Cybersecurity Framework 2.0, expandindo os cinco pilares tradicionais (Identify, Protect, Detect, Respond, Recover) com a nova função GOVERN (GV). A função exige que a estratégia de cibersegurança e o apetite a risco sejam formalmente estabelecidos e comunicados pela liderança.",
                gcpImpact: "Integração nativa com Security Command Center (SCC Enterprise), políticas organizacionais (Org Policies) no nível raiz e métricas de risco compartilhadas com o conselho.",
                controls: ["GV.OC (Contexto Organizacional)", "GV.RM (Gestão de Risco)", "GV.PO (Políticas de Segurança)", "A.5.1 (Políticas de Segurança)"],
                auditPrompt: "Como o nosso ambiente Google Cloud atende aos requisitos da nova função Governança (GV) do NIST CSF 2.0? Avaliar postura do Security Command Center e alinhamento das políticas da organização."
            },
            "pci-dss-v4": {
                tag: "PCI-DSS v4.0.1",
                tagColor: "#c58af9",
                date: "Julho 2026",
                issuer: "PCI Security Standards Council (PCI SSC)",
                title: "Transição Mandatória PCI-DSS v4.0 em Ambientes Cloud",
                summary: "O PCI SSC concluiu a transição obrigatória para o PCI-DSS v4.0. Ambientes que processam dados de cartões de pagamento (CDE) agora devem comprovar autenticação multifator contínua, criptografia forte com gerenciamento automatizado de chaves e isolamento estrito de rede.",
                gcpImpact: "Perímetros rigorosos via VPC Service Controls (VPC-SC), uso de Cloud KMS com nível de proteção HSM (FIPS 140-3 Nível 3) e inspeção de cabeçalhos contra ataques client-side.",
                controls: ["Requisito 3 (Proteção de Dados)", "Requisito 8 (IAM & MFA)", "A.8.12 (DLP)", "A.8.24 (Criptografia)"],
                auditPrompt: "Verificar se os perímetros VPC Service Controls e as chaves Cloud KMS com HSM do nosso projeto atendem aos requisitos de isolamento de CDE do PCI-DSS v4.0."
            },
            "anpd-lgpd": {
                tag: "ANPD & LGPD",
                tagColor: "#fdd663",
                date: "Junho 2026",
                issuer: "ANPD (Autoridade Nacional de Proteção de Dados)",
                title: "Guia de Segurança da Informação da ANPD para Nuvem",
                summary: "A ANPD emitiu novas diretrizes de segurança da informação para agentes de tratamento de pequeno, médio e grande porte que operam em nuvem pública, destacando criptografia em repouso e em trânsito, minimização de dados e elaboração de RIPD.",
                gcpImpact: "Adoção de Cloud DLP (Sensitive Data Protection) para descoberta e mascaramento contínuo de PII (CPF, RG, dados bancários) no Cloud Storage e BigQuery.",
                controls: ["Art. 46 a 48 LGPD", "A.8.11 (Mascaramento de Dados)", "A.8.12 (Prevenção de Vazamentos)", "A.5.34 (Privacidade e PII)"],
                auditPrompt: "Auditar a conformidade de dados pessoais sensíveis (PII) nos buckets e datasets do GCP utilizando Cloud DLP, de acordo com o Guia de Segurança da Informação da ANPD."
            },
            "csa-guidance-v5": {
                tag: "CSA Star",
                tagColor: "#78d9ec",
                date: "Maio 2026",
                issuer: "Cloud Security Alliance (CSA)",
                title: "CSA Guia v5 de Governança para Agentes de IA",
                summary: "A Cloud Security Alliance lançou o Security Guidance v5 focado em arquiteturas híbridas e governança de agentes de inteligência artificial autônomos, definindo limites para acesso a dados, prevenção de vazamento de contexto e identidades de máquina.",
                gcpImpact: "Implementação de Model Armor para inspeção de prompts/respostas, arquiteturas Zero-Copy (sem replicação de dados) e identidades SPIFFE emitidas para cada subagente.",
                controls: ["CSA AIS-01 (Segurança de Modelos)", "CSA IAM-03 (Identidades Não-Humanas)", "A.8.28 (Codificação Segura)"],
                auditPrompt: "Verificar como a arquitetura do Agentic GRC implementa as diretrizes do CSA Guidance v5 para governança e segurança de agentes autônomos de IA no Google Cloud."
            },
            "cis-gcp-v3": {
                tag: "CIS Benchmark",
                tagColor: "#fcad70",
                date: "Abril 2026",
                issuer: "Center for Internet Security (CIS)",
                title: "CIS Google Cloud Foundation Benchmark v3.0 Atualizado",
                summary: "O CIS lançou atualização abrangente para o benchmark de Google Cloud, reforçando regras de hardening para contas de serviço, chaves de API restritas, Cloud Storage sem acesso público e retenção centralizada de logs.",
                gcpImpact: "Verificação automatizada de conformidade contra mais de 80 regras de hardening em IAM, Cloud Storage, VPC, Cloud Logging e Cloud KMS.",
                controls: ["CIS GCP 1.x (IAM)", "CIS GCP 2.x (Storage)", "CIS GCP 3.x (Logging)", "A.8.9 (Gestão de Configuração)"],
                auditPrompt: "Executar varredura de hardening baseada nas recomendações do CIS Google Cloud Foundation Benchmark v3.0 nos projetos em escopo."
            }
        };

        let currentActiveNewsKey = null;

        function openNewsModal(newsKey) {
            const data = regulatoryNewsDatabase[newsKey];
            if (!data) return;

            currentActiveNewsKey = newsKey;
            document.getElementById("newsModalTitle").innerText = data.title;
            const tagEl = document.getElementById("newsModalTag");
            tagEl.innerText = data.tag;
            tagEl.style.background = `rgba(${parseInt(data.tagColor.slice(1,3),16)}, ${parseInt(data.tagColor.slice(3,5),16)}, ${parseInt(data.tagColor.slice(5,7),16)}, 0.15)`;
            tagEl.style.color = data.tagColor;

            document.getElementById("newsModalDate").innerText = data.date;
            document.getElementById("newsModalIssuer").innerText = data.issuer;
            document.getElementById("newsModalSummary").innerText = data.summary;
            document.getElementById("newsModalGcpImpact").innerText = data.gcpImpact;

            const controlsContainer = document.getElementById("newsModalControls");
            controlsContainer.innerHTML = "";
            data.controls.forEach(ctrl => {
                const badge = document.createElement("span");
                badge.style.cssText = "font-size: 11.5px; background: rgba(255,255,255,0.06); border: 1px solid var(--border-subtle); padding: 3px 8px; border-radius: 4px; color: #e8eaed;";
                badge.innerText = ctrl;
                controlsContainer.appendChild(badge);
            });

            // Set official source link
            const linkEl = document.getElementById("newsModalOriginalLink");
            const sourceNameEl = document.getElementById("newsModalSourceName");
            if (linkEl && data.originalUrl) {
                linkEl.href = data.originalUrl;
                if (sourceNameEl) sourceNameEl.innerText = "Acessar Fonte Oficial (" + (data.sourceName || "Portal Oficial") + ") ↗";
                linkEl.style.display = "inline-flex";
            } else if (linkEl) {
                linkEl.style.display = "none";
            }

            document.getElementById("newsModal").classList.add("active");
        }

        function closeNewsModal() {
            document.getElementById("newsModal").classList.remove("active");
            currentActiveNewsKey = null;
        }

        function executeNewsAudit() {
            if (!currentActiveNewsKey) return;
            const data = regulatoryNewsDatabase[currentActiveNewsKey];
            closeNewsModal();
            if (data && data.auditPrompt) {
                promptPreFill(data.auditPrompt);
            }
        }


        function openExecutiveReport() {
            switchView("view-report-exec");
            const el = document.getElementById("docProjectsAudited");
            if (el) el.innerText = Array.from(selectedProjectIds).join(", ") || "agentic-grc-cd06";
        }

        function printExecutiveReport() {
            openExecutiveReport();
            setTimeout(() => { window.print(); }, 250);
        }

        function openTechnicalReport() {
            switchView("view-report-tech");
            const projEl = document.getElementById("techProjectsAudited");
            if (projEl) projEl.innerText = Array.from(selectedProjectIds).join(", ") || "agentic-grc-cd06";
            const dateEl = document.getElementById("techGeneratedAt");
            if (dateEl) dateEl.innerText = new Date().toUTCString();
            const sealEl = document.getElementById("techSealDate");
            if (sealEl) sealEl.innerText = new Date().toUTCString();
        }

        function printTechnicalReport() {
            openTechnicalReport();
            setTimeout(() => { window.print(); }, 250);
        }

        // Project Scope Management (GCP Organization Level)
        async function loadProjects() {
            try {
                const res = await fetch("/api/projects");
                if (res.ok) {
                    const data = await res.json();
                    if (data && data.projects && data.projects.length > 0) {
                        activeProjects = data.projects;
                        selectedProjectIds = new Set(activeProjects.map(p => p.project_id));
                    }
                    if (data && data.all_org_projects) {
                        allOrgProjects = data.all_org_projects;
                    }
                }
            } catch (e) {
                console.error("Error loading projects", e);
            }
            renderScopeBox();
            renderOrgDropdown();
        }

        function toggleOrgScopeDropdown() {
            const dropdown = document.getElementById("orgScopeDropdown");
            const chevron = document.getElementById("orgDropdownChevron");
            if (!dropdown) return;
            const isOpen = dropdown.style.display !== "none";
            dropdown.style.display = isOpen ? "none" : "block";
            if (chevron) {
                chevron.style.transform = isOpen ? "rotate(0deg)" : "rotate(180deg)";
            }
            if (!isOpen) {
                renderOrgDropdown();
            }
        }

        function renderOrgDropdown(filterText = "") {
            const list = document.getElementById("orgDropdownItemsList");
            if (!list) return;
            list.innerHTML = "";

            const projectsToDisplay = allOrgProjects.length > 0 ? allOrgProjects : activeProjects;
            const q = filterText.toLowerCase().trim();

            let inScopeCount = 0;
            projectsToDisplay.forEach(p => {
                const isSelected = selectedProjectIds.has(p.project_id);
                if (isSelected) inScopeCount++;

                if (q && !p.project_id.toLowerCase().includes(q) && !(p.environment || "").toLowerCase().includes(q)) {
                    return;
                }

                const row = document.createElement("div");
                row.className = "project-pill-item";
                row.style.padding = "5px 7px";
                row.style.background = isSelected ? "rgba(138, 180, 248, 0.08)" : "var(--bg-surface)";
                row.style.border = isSelected ? "1px solid var(--gcp-blue)" : "1px solid var(--border-subtle)";
                row.innerHTML = `
                    <div class="project-pill-left" style="gap: 7px;">
                        <input type="checkbox" class="project-checkbox" ${isSelected ? "checked" : ""} onchange="toggleProjectSelection('${p.project_id}', this.checked)">
                        <div style="display: flex; flex-direction: column;">
                            <span class="project-id-text" style="font-size: 11.5px; font-weight: ${isSelected ? '600' : '400'}; color: ${isSelected ? 'var(--text-primary)' : 'var(--text-secondary)'};" title="${p.project_id}">${p.project_id}</span>
                            <span style="font-size: 9px; color: var(--text-tertiary);">${p.folder || 'Folder: Workloads'}</span>
                        </div>
                    </div>
                    <span class="env-badge" style="font-size: 8.5px;">${p.environment || "PROD"}</span>
                `;
                list.appendChild(row);
            });

            const badgeText = document.getElementById("orgScopeBadgeText");
            if (badgeText) {
                badgeText.innerText = `${selectedProjectIds.size}/${projectsToDisplay.length} ativos`;
            }
        }

        function filterOrgDropdown(val) {
            renderOrgDropdown(val);
        }

        async function selectAllOrgProjects() {
            const list = allOrgProjects.length > 0 ? allOrgProjects : activeProjects;
            for (const p of list) {
                selectedProjectIds.add(p.project_id);
                try {
                    await fetch("/api/projects/toggle_scope", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ project_id: p.project_id, in_scope: true })
                    });
                } catch(e) {}
            }
            renderScopeBox();
            renderOrgDropdown();
        }

        async function selectProdOnlyOrgProjects() {
            const list = allOrgProjects.length > 0 ? allOrgProjects : activeProjects;
            selectedProjectIds.clear();
            for (const p of list) {
                const isProd = (p.environment || "").toUpperCase() === "PRODUCTION";
                if (isProd) {
                    selectedProjectIds.add(p.project_id);
                }
                try {
                    await fetch("/api/projects/toggle_scope", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ project_id: p.project_id, in_scope: isProd })
                    });
                } catch(e) {}
            }
            if (selectedProjectIds.size === 0 && list.length > 0) {
                selectedProjectIds.add(list[0].project_id);
            }
            renderScopeBox();
            renderOrgDropdown();
        }

        function renderScopeBox() {
            const container = document.getElementById("scopeProjectsList");
            if (container) {
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
            }

            const scopeLabel = document.getElementById("currentScopeLabel");
            if (scopeLabel) {
                const count = selectedProjectIds.size;
                const firstProj = Array.from(selectedProjectIds)[0] || (activeProjects[0] ? activeProjects[0].project_id : "agentic-grc-cd06");
                if (count <= 1) {
                    scopeLabel.innerText = firstProj;
                } else {
                    scopeLabel.innerText = `${firstProj} (+${count - 1} ativos)`;
                }
            }

            const badge = document.getElementById("topProjectCountBadge");
            if (badge) {
                const count = selectedProjectIds.size;
                badge.innerText = `${count} ${count === 1 ? 'projeto ativo' : 'projetos ativos'}`;
            }
        }

        function openProjectScopeModal() {
            openProjectModal();
        }

        async function toggleProjectSelection(pid, checked) {
            if (checked) {
                selectedProjectIds.add(pid);
            } else {
                if (selectedProjectIds.size > 1) {
                    selectedProjectIds.delete(pid);
                } else {
                    alert("Pelo menos um projeto deve permanecer no escopo de auditoria.");
                    renderScopeBox();
                    renderOrgDropdown();
                    return;
                }
            }

            try {
                await fetch("/api/projects/toggle_scope", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ project_id: pid, in_scope: checked })
                });
            } catch(e) {
                console.warn("Failed to persist toggle scope", e);
            }

            renderScopeBox();
            renderOrgDropdown();
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
            if (hero) hero.style.display = "none"; updateBottomInputVisibility();

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
                    <span style="color: var(--text-tertiary)">Agentic GRC Auditor (Google Cloud Security) avaliando telemetria e grafo de evidências...</span>
                </div>
            `;
            chatArea.appendChild(botRow);
            chatArea.scrollTop = chatArea.scrollHeight;

            try {
                const res = await fetch("/api/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        message: text,
                        project_id: Array.from(selectedProjectIds)[0],
                        selected_projects: Array.from(selectedProjectIds),
                        model: currentSelectedModel,
                        locale: window.currentLanguage || 'pt'
                    })
                });
                const data = await res.json();
                const replyElem = document.getElementById("activeBotReply");
                replyElem.removeAttribute("id");
                replyElem.innerHTML = renderExecutiveMarkdown(data.response || "Sem resposta do auditor.");
            } catch (err) {
                const replyElem = document.getElementById("activeBotReply");
                replyElem.removeAttribute("id");
                replyElem.innerHTML = `<span style="color: var(--gcp-red)">Erro na comunicação com o auditor Google Cloud Security: ${err}</span>`;
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
            const nameMap = {
                "annex_a": "Annex A Auditor Agent",
                "horizon_scanner": "Horizon Scanner Agent",
                "iac_scanner": "IaC Scanner (Terraform/Ansible)",
                "org_policies": "Organization Policies Enforcer"
            };
            executeSubagent(subagent, nameMap[subagent] || subagent);
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
                if (hero) hero.style.display = "none"; updateBottomInputVisibility();

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
    
        // -------------------------------------------------------------------
        // FinOps & Token Cost Analytics Engine
        // -------------------------------------------------------------------
        async function loadFinOpsMetrics() {
            try {
                const res = await fetch("/api/finops");
                if (res.ok) {
                    finopsData = await res.json();
                    renderFinOpsDashboard(finopsData);
                }
            } catch(e) {
                console.error("Error loading FinOps data", e);
            }
        }

        function renderFinOpsDashboard(data) {
            if (!data || !data.summary) return;
            const s = data.summary;

            // Summary KPIs
            const costUsdElem = document.getElementById("finopsTotalCostUsd");
            if (costUsdElem) costUsdElem.innerText = `$ ${s.total_cost_usd.toFixed(2)} USD`;

            const costBrlElem = document.getElementById("finopsTotalCostBrl");
            if (costBrlElem) costBrlElem.innerText = `R$ ${s.total_cost_brl.toFixed(2).replace('.', ',')} BRL (Cotação R$ ${s.usd_to_brl_rate.toFixed(2)})`;

            const quotaElem = document.getElementById("finopsQuotaUsed");
            if (quotaElem) quotaElem.innerText = `${s.quota_used_percent}% consumido`;

            const tokensElem = document.getElementById("finopsTotalTokens");
            if (tokensElem) tokensElem.innerText = Number(s.total_tokens).toLocaleString();

            const tokensBreakdownElem = document.getElementById("finopsTokensBreakdown");
            if (tokensBreakdownElem) {
                tokensBreakdownElem.innerText = `Prompt: ${Math.round(s.total_prompt_tokens/1000)}k | Saída: ${Math.round(s.total_completion_tokens/1000)}k`;
            }

            const invocElem = document.getElementById("finopsInvocations");
            if (invocElem) invocElem.innerText = `${s.total_invocations} chamadas`;

            const savingsUsdElem = document.getElementById("finopsSavingsUsd");
            if (savingsUsdElem) savingsUsdElem.innerText = `$ ${s.total_savings_usd.toFixed(2)} USD`;

            const savingsBrlElem = document.getElementById("finopsSavingsBrl");
            if (savingsBrlElem) savingsBrlElem.innerText = `R$ ${s.total_savings_brl.toFixed(2).replace('.', ',')} BRL economizados`;

            const cacheHitElem = document.getElementById("finopsCacheHitRatio");
            if (cacheHitElem) cacheHitElem.innerText = `${s.cache_hit_ratio_percent}%`;

            const costPerCtrlElem = document.getElementById("finopsCostPerControl");
            if (costPerCtrlElem) costPerCtrlElem.innerText = `$ ${s.cost_per_control_usd.toFixed(3)} USD`;

            // Phases Breakdown
            if (data.phases) {
                const p1 = data.phases["Fase 1: Triagem Zero-Copy"];
                if (p1) {
                    const p1Cost = document.getElementById("finopsPhase1Cost");
                    const p1Tok = document.getElementById("finopsPhase1Tokens");
                    if (p1Cost) p1Cost.innerText = `$ ${p1.cost_usd.toFixed(2)} USD`;
                    if (p1Tok) p1Tok.innerText = `${Number(p1.tokens).toLocaleString()} tokens • R$ ${(p1.cost_usd * s.usd_to_brl_rate).toFixed(2).replace('.', ',')}`;
                }
                const p2 = data.phases["Fase 2: Telemetria Técnica GCP"];
                if (p2) {
                    const p2Cost = document.getElementById("finopsPhase2Cost");
                    const p2Tok = document.getElementById("finopsPhase2Tokens");
                    if (p2Cost) p2Cost.innerText = `$ ${p2.cost_usd.toFixed(2)} USD`;
                    if (p2Tok) p2Tok.innerText = `${Number(p2.tokens).toLocaleString()} tokens • R$ ${(p2.cost_usd * s.usd_to_brl_rate).toFixed(2).replace('.', ',')}`;
                }
                const p3 = data.phases["Fase 3: Testes de Eficácia & Drift"];
                if (p3) {
                    const p3Cost = document.getElementById("finopsPhase3Cost");
                    const p3Tok = document.getElementById("finopsPhase3Tokens");
                    if (p3Cost) p3Cost.innerText = `$ ${p3.cost_usd.toFixed(2)} USD`;
                    if (p3Tok) p3Tok.innerText = `${Number(p3.tokens).toLocaleString()} tokens • R$ ${(p3.cost_usd * s.usd_to_brl_rate).toFixed(2).replace('.', ',')}`;
                }
                const p4 = data.phases["Fase 4: Parecer Executivo & Selo"];
                if (p4) {
                    const p4Cost = document.getElementById("finopsPhase4Cost");
                    const p4Tok = document.getElementById("finopsPhase4Tokens");
                    if (p4Cost) p4Cost.innerText = `$ ${p4.cost_usd.toFixed(2)} USD`;
                    if (p4Tok) p4Tok.innerText = `${Number(p4.tokens).toLocaleString()} tokens • R$ ${(p4.cost_usd * s.usd_to_brl_rate).toFixed(2).replace('.', ',')}`;
                }
            }

            // Agents Table
            const tbody = document.getElementById("finopsAgentsTableBody");
            if (tbody && data.agents) {
                tbody.innerHTML = "";
                data.agents.forEach(ag => {
                    const tr = document.createElement("tr");
                    tr.style.borderBottom = "1px solid var(--border-subtle)";
                    tr.style.transition = "background 0.2s ease";
                    tr.innerHTML = `
                        <td style="padding: 10px 12px;">
                            <div style="font-weight: 500; color: var(--text-primary);">${ag.name}</div>
                            <div style="font-size: 11px; color: var(--text-tertiary);">${ag.category}</div>
                        </td>
                        <td style="padding: 10px 12px;">
                            <span class="env-badge" style="background: rgba(138, 180, 248, 0.12); color: var(--gcp-blue);">${ag.model}</span>
                        </td>
                        <td style="padding: 10px 12px; font-weight: 500;">${ag.invocations}</td>
                        <td style="padding: 10px 12px; font-family: monospace;">${Number(ag.prompt_tokens).toLocaleString()}</td>
                        <td style="padding: 10px 12px; font-family: monospace; color: var(--gcp-green); font-weight: 500;">${Number(ag.cached_tokens).toLocaleString()}</td>
                        <td style="padding: 10px 12px; font-family: monospace;">${Number(ag.completion_tokens).toLocaleString()}</td>
                        <td style="padding: 10px 12px; font-family: monospace; font-weight: 600;">${Number(ag.total_tokens).toLocaleString()}</td>
                        <td style="padding: 10px 12px; font-weight: 600; color: var(--text-primary);">$ ${ag.cost_usd.toFixed(3)}</td>
                        <td style="padding: 10px 12px; color: var(--text-secondary);">R$ ${ag.cost_brl.toFixed(2).replace('.', ',')}</td>
                        <td style="padding: 10px 12px;">
                            ${ag.savings_usd > 0 ? `<span style="color: var(--gcp-green); font-size: 11.5px; font-weight: 600;">+$ ${ag.savings_usd.toFixed(3)}</span>` : `<span style="color: var(--text-tertiary); font-size: 11px;">-</span>`}
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        function filterFinopsTable(q) {
            if (!finopsData || !finopsData.agents) return;
            const query = q.toLowerCase().trim();
            const filtered = {
                ...finopsData,
                agents: finopsData.agents.filter(a => 
                    a.name.toLowerCase().includes(query) || 
                    a.category.toLowerCase().includes(query) ||
                    a.model.toLowerCase().includes(query)
                )
            };
            renderFinOpsDashboard(filtered);
        }

        async function simulateFinOpsRun() {
            try {
                const res = await fetch("/api/finops/simulate", { method: "POST" });
                if (res.ok) {
                    finopsData = await res.json();
                    renderFinOpsDashboard(finopsData);
                    alert("Simulação de auditoria contínua executada! Telemetria de tokens e custos atualizada.");
                }
            } catch(e) {
                console.error("Simulation error", e);
            }
        }

        function exportFinOpsJson() {
            if (!finopsData) return;
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(finopsData, null, 2));
            const downloadAnchor = document.createElement("a");
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", `finops_grc_metrics_${new Date().toISOString().slice(0,10)}.json`);
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        }

    </script>

    


    <!-- Overlay e Drawer de Criação de Subagente (Lado Esquerdo) -->
    <div class="left-drawer-overlay" id="leftDrawerOverlay" onclick="closeCreateSubagentModal()"></div>
    <div class="left-drawer" id="subagentLeftDrawer">
        <div class="left-drawer-header">
            <div class="left-drawer-title">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--gcp-blue)" stroke-width="2">
                    <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                <span id="drawerTitle">Criar Novo Subagente</span>
            </div>
            <button class="btn-close-rem" onclick="closeCreateSubagentModal()">&times;</button>
        </div>
        <div class="left-drawer-body">

            <!-- Sugestões Contextuais & IA de Agentes por Indústria -->
            <div class="drawer-suggestions-box">
                <div class="drawer-suggestions-title">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                    Recomendações e Templates de Subagentes
                </div>
                <div class="template-pills-row">
                    <button class="btn-template-pill" type="button" onclick="applyIndustryTemplate('fintech')">Fintech / Bancos</button>
                    <button class="btn-template-pill" type="button" onclick="applyIndustryTemplate('zerotrust')">Zero-Trust / IAM</button>
                    <button class="btn-template-pill" type="button" onclick="applyIndustryTemplate('k8s')">GKE / DevSecOps</button>
                    <button class="btn-template-pill" type="button" onclick="applyIndustryTemplate('privacy')">LGPD / DLP</button>
                    <button class="btn-template-pill" type="button" onclick="applyIndustryTemplate('finops')">FinOps / Storage</button>
                </div>
                <button class="btn-ai-recommend" type="button" onclick="getGeminiAgentRecommendation()">
                    <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
                    </svg>
                    Analisar Ambiente com Vertex AI & Recomendar Agente
                </button>
            </div>

            <input type="hidden" id="drawerAgentEditId" value="">
            
            <div class="form-group">
                <label class="form-label">Nome do Subagente</label>
                <input type="text" id="drawerAgentName" class="form-control" placeholder="Ex: FinOps & Storage Compliance Auditor">
            </div>

            <div class="form-group">
                <label class="form-label">Cargo / Especialidade</label>
                <input type="text" id="drawerAgentRole" class="form-control" placeholder="Ex: Auditor de Ciclo de Vida e Retenção">
            </div>

            <div class="form-group">
                <label class="form-label">Controles ISO Alvo (separados por vírgula)</label>
                <input type="text" id="drawerAgentControls" class="form-control" placeholder="Ex: A.5.9, A.8.10, A.8.11">
            </div>

            <div class="form-group">
                <label class="form-label">Modelo Cognitivo</label>
                <select id="drawerAgentModel" class="form-control">
                    <option value="gemini-2.5-flash" selected>Gemini 2.5 Flash (Recomendado / Resposta Rápida)</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro (Raciocínio Profundo)</option>
                    <option value="gemini-2.5-pro">Gemini 2.5 Pro (Especialista em Auditoria)</option>
                </select>
            </div>

            <div class="form-group">
                <label class="form-label">Descrição do Propósito</label>
                <input type="text" id="drawerAgentDesc" class="form-control" placeholder="Breve resumo do que este subagente avalia no ambiente Google Cloud.">
            </div>

            <div class="form-group">
                <label class="form-label">System Prompt / Instrução Especializada</label>
                <textarea id="drawerAgentPrompt" class="form-control" rows="4" placeholder="Defina a metodologia e critérios do auditor: 'Você é o especialista de Google Cloud Security responsável por...'"></textarea>
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
        <div class="left-drawer-footer">
            <button class="btn-cancel" onclick="closeCreateSubagentModal()">Cancelar</button>
            <button class="btn-confirm" onclick="saveCustomSubagentFromDrawer()" style="background: var(--gcp-blue);">Salvar Subagente</button>
        </div>
    </div>

</body>
</html>
"""
