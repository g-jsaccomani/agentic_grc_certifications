"""Official Gemini / Sidekick style Web Portal View for GEAP Compliance."""

PORTAL_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Enterprise Agent Platform - GRC Audit & Compliance Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
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
            --gemini-blue: #8ab4f8;
            --gemini-purple: #c58af9;
            --google-green: #81c995;
            --google-yellow: #fdd663;
            --google-red: #f28b82;
            --accent-glow: rgba(138, 180, 248, 0.15);
            --sidebar-width: 280px;
            --sidebar-collapsed-width: 68px;
            --font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --transition-smooth: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
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

        /* ------------------------------------------------------------------ */
        /* SVG Icons Helper Classes */
        /* ------------------------------------------------------------------ */
        .icon-svg {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            stroke-width: 1.8;
        }

        /* ------------------------------------------------------------------ */
        /* Left Sidebar (Gemini Sidekick Style) */
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

        .sidebar.collapsed {
            width: var(--sidebar-collapsed-width);
        }

        .sidebar-top {
            padding: 16px 14px 8px 14px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
        }

        .sidebar-top::-webkit-scrollbar {
            width: 4px;
        }
        .sidebar-top::-webkit-scrollbar-thumb {
            background: var(--border-subtle);
            border-radius: 4px;
        }

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

        .gemini-sparkle-icon {
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .brand-title {
            font-size: 19px;
            font-weight: 500;
            letter-spacing: -0.2px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .brand-sidekick {
            background: linear-gradient(135deg, #4285F4 0%, #9B72CB 50%, #D96570 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        .brand-badge {
            font-size: 10px;
            color: var(--text-secondary);
            background: var(--bg-surface);
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
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
        .btn-collapse:hover {
            background: var(--bg-surface);
            color: var(--text-primary);
        }

        /* Primary Action Items */
        .nav-actions {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .nav-action-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: 12px;
            color: var(--text-secondary);
            font-size: 14px;
            cursor: pointer;
            transition: var(--transition-smooth);
            text-decoration: none;
            border: none;
            background: transparent;
            width: 100%;
            text-align: left;
        }

        .nav-action-item:hover {
            background-color: var(--bg-surface);
            color: var(--text-primary);
        }

        .nav-action-item.active {
            background-color: var(--bg-surface-hover);
            color: var(--gemini-blue);
            font-weight: 500;
        }

        .nav-action-item .label {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .sidebar.collapsed .label,
        .sidebar.collapsed .brand-title,
        .sidebar.collapsed .brand-badge,
        .sidebar.collapsed .section-header,
        .sidebar.collapsed .agent-pin,
        .sidebar.collapsed .recent-list,
        .sidebar.collapsed .scope-box,
        .sidebar.collapsed .user-meta {
            display: none !important;
        }

        .sidebar.collapsed .nav-action-item {
            justify-content: center;
            padding: 12px;
        }

        /* Section Header */
        .section-header {
            font-size: 12px;
            font-weight: 500;
            color: var(--text-tertiary);
            padding: 8px 14px 4px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .agent-list {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

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

        .agent-item:hover {
            background-color: var(--bg-surface);
        }

        .agent-item.active {
            background-color: var(--bg-surface-hover);
            color: var(--gemini-blue);
            font-weight: 500;
        }

        .agent-left-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
        }

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
            background: rgba(138, 180, 248, 0.2);
            color: var(--gemini-blue);
            border-color: var(--gemini-blue);
        }

        .agent-name {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .agent-pin {
            color: var(--text-tertiary);
            opacity: 0.6;
            transition: var(--transition-smooth);
        }
        .agent-item:hover .agent-pin {
            opacity: 1;
            color: var(--text-secondary);
        }

        /* Recents */
        .recent-list {
            display: flex;
            flex-direction: column;
            gap: 2px;
            padding-left: 4px;
        }

        .recent-item {
            padding: 8px 12px;
            font-size: 13px;
            color: var(--text-secondary);
            border-radius: 8px;
            cursor: pointer;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transition: var(--transition-smooth);
        }
        .recent-item:hover {
            background-color: var(--bg-surface);
            color: var(--text-primary);
        }

        /* ------------------------------------------------------------------ */
        /* Bottom Left: Scope Box & User Profile (As Requested) */
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
            color: var(--gemini-blue);
            cursor: pointer;
            font-size: 11px;
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 2px 4px;
            border-radius: 4px;
        }
        .btn-add-scope:hover {
            background: rgba(138, 180, 248, 0.15);
        }

        .scope-projects-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            max-height: 110px;
            overflow-y: auto;
        }
        .scope-projects-list::-webkit-scrollbar {
            width: 3px;
        }
        .scope-projects-list::-webkit-scrollbar-thumb {
            background: var(--border-focus);
            border-radius: 3px;
        }

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
        .project-pill-item:hover {
            border-color: var(--border-focus);
        }

        .project-pill-left {
            display: flex;
            align-items: center;
            gap: 6px;
            overflow: hidden;
        }

        .project-checkbox {
            accent-color: var(--gemini-blue);
            cursor: pointer;
        }

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
            color: var(--google-green);
        }

        /* User Profile Row */
        .user-profile-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 4px 0 4px;
            cursor: pointer;
        }

        .user-left {
            display: flex;
            align-items: center;
            gap: 10px;
            overflow: hidden;
        }

        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1a73e8, #8ab4f8);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .user-meta {
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .user-name {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .user-plan {
            font-size: 11px;
            color: var(--text-secondary);
        }

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
        .btn-settings:hover {
            background: var(--bg-surface);
            color: var(--text-primary);
        }

        /* ------------------------------------------------------------------ */
        /* Main Application Area */
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

        /* Top Bar */
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

        .nav-breadcrumb {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
        }

        .top-active-agent {
            font-weight: 500;
            color: var(--text-primary);
        }

        .top-status-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--google-green);
            background: rgba(129, 201, 149, 0.1);
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid rgba(129, 201, 149, 0.2);
        }

        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--google-green);
            box-shadow: 0 0 8px var(--google-green);
        }

        .top-right-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        /* Export Dropdown */
        .dropdown {
            position: relative;
            display: inline-block;
        }

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
        .btn-action-primary:hover {
            background: var(--bg-surface-hover);
            border-color: var(--border-focus);
        }

        .dropdown-menu {
            display: none;
            position: absolute;
            right: 0;
            top: 110%;
            background: var(--bg-sidebar);
            border: 1px solid var(--border-focus);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            min-width: 220px;
            z-index: 100;
            overflow: hidden;
            padding: 6px 0;
        }
        .dropdown.show .dropdown-menu {
            display: block;
        }

        .dropdown-item {
            padding: 9px 16px;
            font-size: 13px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            transition: var(--transition-smooth);
            text-decoration: none;
        }
        .dropdown-item:hover {
            background: var(--bg-surface);
            color: var(--gemini-blue);
        }

        /* Content Views Area */
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
        .view-pane.active {
            display: flex;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ------------------------------------------------------------------ */
        /* View 1: Chatbot Auditor (Gemini Native Chat Experience) */
        /* ------------------------------------------------------------------ */
        .chat-view-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            max-width: 860px;
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
            gap: 24px;
        }

        .chat-messages-area::-webkit-scrollbar {
            width: 6px;
        }
        .chat-messages-area::-webkit-scrollbar-thumb {
            background: var(--border-subtle);
            border-radius: 6px;
        }

        /* Hero Welcome Screen (Matches Screenshot) */
        .gemini-hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin: auto 0;
            padding: 40px 20px;
            gap: 16px;
        }

        .hero-avatar {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: radial-gradient(circle, #25282c 0%, #1e1f20 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border-focus);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .hero-title {
            font-size: 32px;
            font-weight: 500;
            letter-spacing: -0.5px;
            color: var(--text-primary);
        }

        .hero-subtitle {
            font-size: 14.5px;
            color: var(--text-secondary);
            max-width: 580px;
            line-height: 1.6;
        }

        .hero-suggestions-stack {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 100%;
            max-width: 580px;
            margin-top: 16px;
        }

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
        .hero-suggestion-card:hover {
            background: var(--bg-surface);
            border-color: var(--border-focus);
            transform: translateX(4px);
        }

        /* Message Bubbles */
        .msg-row {
            display: flex;
            gap: 16px;
            width: 100%;
            animation: fadeIn 0.25s ease;
        }

        .msg-row.user {
            justify-content: flex-end;
        }

        .msg-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .msg-avatar.gemini {
            background: radial-gradient(circle, #25282c 0%, #1e1f20 100%);
            border: 1px solid var(--border-subtle);
        }

        .msg-avatar.user-av {
            background: var(--gemini-blue);
            color: #131314;
            font-weight: 700;
            font-size: 12px;
        }

        .msg-content {
            max-width: 80%;
            line-height: 1.65;
            font-size: 14.5px;
            color: var(--text-primary);
        }

        .msg-row.user .msg-content {
            background: var(--bg-surface);
            padding: 12px 18px;
            border-radius: 18px 18px 4px 18px;
            border: 1px solid var(--border-subtle);
        }

        .msg-row.bot .msg-content {
            padding: 4px 0;
        }

        .msg-content p {
            margin-bottom: 12px;
        }

        .msg-content ul, .msg-content ol {
            margin-left: 20px;
            margin-bottom: 12px;
        }

        .msg-content li {
            margin-bottom: 6px;
        }

        .msg-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 13.5px;
        }

        .msg-content th, .msg-content td {
            border: 1px solid var(--border-subtle);
            padding: 8px 12px;
            text-align: left;
        }

        .msg-content th {
            background: var(--bg-surface);
            font-weight: 500;
        }

        .msg-content pre {
            background: #0d0e0f;
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 12px;
            font-family: var(--font-mono);
            font-size: 12.5px;
            overflow-x: auto;
            margin: 12px 0;
        }

        /* Floating Gemini Input Bar */
        .chat-input-wrapper {
            position: absolute;
            bottom: 20px;
            left: 0;
            right: 0;
            max-width: 860px;
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

        .chat-input-box:focus-within {
            border-color: var(--border-focus);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 0 1px var(--border-focus);
        }

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
        .btn-input-icon:hover {
            background: var(--bg-surface);
            color: var(--text-primary);
        }

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

        .chat-textarea::placeholder {
            color: var(--text-tertiary);
        }

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

        .btn-send.active {
            background: var(--gemini-blue);
            color: #131314;
        }

        .chat-disclaimer {
            font-size: 11px;
            color: var(--text-tertiary);
            text-align: center;
        }

        /* ------------------------------------------------------------------ */
        /* View 2: Scan por Fases */
        /* ------------------------------------------------------------------ */
        .section-header-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-subtle);
        }

        .view-title-group h2 {
            font-size: 22px;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .view-title-group p {
            font-size: 13.5px;
            color: var(--text-secondary);
        }

        .phases-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

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

        .phase-card.active {
            border-color: var(--gemini-blue);
            background: rgba(138, 180, 248, 0.05);
        }

        .phase-badge-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .phase-step-num {
            font-size: 11px;
            font-weight: 700;
            color: var(--gemini-blue);
            text-transform: uppercase;
        }

        .phase-status-tag {
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--bg-canvas);
            color: var(--text-secondary);
        }

        .phase-status-tag.completed {
            background: rgba(129, 201, 149, 0.15);
            color: var(--google-green);
        }

        .phase-name {
            font-size: 15px;
            font-weight: 500;
            color: var(--text-primary);
        }

        .phase-desc {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .phase-progress-bar {
            height: 4px;
            background: var(--bg-canvas);
            border-radius: 4px;
            overflow: hidden;
            margin-top: auto;
        }

        .phase-progress-fill {
            height: 100%;
            background: var(--gemini-blue);
            width: 0%;
            transition: width 0.4s ease;
        }

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

        .console-logs {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            line-height: 1.5;
        }

        .log-entry {
            display: flex;
            gap: 12px;
        }

        .log-ts {
            color: var(--text-tertiary);
            flex-shrink: 0;
        }

        .log-msg {
            color: var(--text-primary);
        }
        .log-msg.success { color: var(--google-green); }
        .log-msg.info { color: var(--gemini-blue); }

        /* ------------------------------------------------------------------ */
        /* View 3: Matriz ISO 27001 Escalável */
        /* ------------------------------------------------------------------ */
        .matrix-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }

        .matrix-filter-pills {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

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

        .btn-filter-pill:hover,
        .btn-filter-pill.active {
            background: var(--bg-surface-hover);
            color: var(--text-primary);
            border-color: var(--gemini-blue);
        }

        .search-box-wrap {
            position: relative;
            min-width: 260px;
        }

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
        .search-input:focus {
            border-color: var(--border-focus);
        }

        .search-icon-pos {
            position: absolute;
            left: 11px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-tertiary);
            pointer-events: none;
        }

        .table-container {
            flex: 1;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            overflow: auto;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }

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

        .data-table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-primary);
            vertical-align: top;
        }

        .data-table tr:hover td {
            background: var(--bg-surface-hover);
        }

        .ctrl-id-badge {
            font-family: var(--font-mono);
            font-size: 11.5px;
            color: var(--gemini-blue);
            background: rgba(138, 180, 248, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
        }

        .status-badge {
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 10px;
            display: inline-block;
        }

        .status-badge.compliant {
            background: rgba(129, 201, 149, 0.15);
            color: var(--google-green);
        }

        /* ------------------------------------------------------------------ */
        /* View 4: Subagentes & Zero-Copy */
        /* ------------------------------------------------------------------ */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
        }

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
        .card-panel:hover {
            border-color: var(--border-focus);
        }

        .card-panel-header {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .card-icon-avatar {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: var(--bg-canvas);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--gemini-blue);
            border: 1px solid var(--border-subtle);
        }

        .card-title {
            font-size: 15px;
            font-weight: 500;
            color: var(--text-primary);
        }

        .card-desc {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* ------------------------------------------------------------------ */
        /* View 5: Scorecard & Grafo de Evidências */
        /* ------------------------------------------------------------------ */
        .scorecard-stats-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .stat-val {
            font-size: 36px;
            font-weight: 700;
            color: var(--text-primary);
            font-family: var(--font-mono);
        }

        .stat-label {
            font-size: 13px;
            color: var(--text-secondary);
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
        .modal-overlay.active {
            display: flex;
        }

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

        .modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .modal-title {
            font-size: 18px;
            font-weight: 500;
            color: var(--text-primary);
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .form-label {
            font-size: 12.5px;
            color: var(--text-secondary);
        }

        .form-input {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 10px 12px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
        }
        .form-input:focus {
            border-color: var(--gemini-blue);
        }

        .modal-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 8px;
        }

        .btn-cancel {
            background: transparent;
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
        }

        .btn-confirm {
            background: var(--gemini-blue);
            border: none;
            color: #131314;
            font-weight: 500;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
        }

        /* Print styles for PDF export */
        @media print {
            body { background: #fff !important; color: #000 !important; overflow: visible !important; }
            .sidebar, .top-navbar, .chat-input-wrapper, .modal-overlay { display: none !important; }
            .main-container { height: auto !important; }
            .views-viewport { overflow: visible !important; }
            .view-pane { display: block !important; }
            .data-table th { background: #f0f0f0 !important; color: #000 !important; }
            .data-table td { color: #000 !important; }
        }
    </style>
</head>
<body>

    <!-- Left Sidebar (Gemini Sidekick Style) -->
    <aside class="sidebar" id="appSidebar">
        <div class="sidebar-top">
            <!-- Brand & Sidebar Toggle -->
            <div class="brand-header">
                <a href="#" class="brand-left" onclick="switchView('view-chat')">
                    <div class="gemini-sparkle-icon">
                        <svg viewBox="0 0 24 24" width="24" height="24" fill="none">
                            <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="url(#gemini-star-grad)"/>
                            <defs>
                                <linearGradient id="gemini-star-grad" x1="2" y1="2" x2="22" y2="22">
                                    <stop stop-color="#4285F4"/>
                                    <stop offset="0.33" stop-color="#9B72CB"/>
                                    <stop offset="0.66" stop-color="#D96570"/>
                                    <stop offset="1" stop-color="#F2A600"/>
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                    <span class="brand-title">
                        <span class="brand-sidekick">sidekick</span>
                        <span class="brand-badge">GEAP</span>
                    </span>
                </a>
                <button class="btn-collapse" onclick="toggleSidebar()" title="Recolher menu">
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
                    <span class="label">Pesquisar</span>
                </button>
                <button class="nav-action-item" onclick="switchView('view-matrix')">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <rect x="3" y="3" width="7" height="7"/>
                            <rect x="14" y="3" width="7" height="7"/>
                            <rect x="14" y="14" width="7" height="7"/>
                            <rect x="3" y="14" width="7" height="7"/>
                        </svg>
                    </span>
                    <span class="label">Biblioteca</span>
                </button>
                <button class="nav-action-item" onclick="switchView('view-connectors')">
                    <span class="icon-svg">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
                            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                        </svg>
                    </span>
                    <span class="label">Habilidades</span>
                </button>
            </div>

            <!-- Specialized Sub-Agents Group (Requested by User) -->
            <div class="section-header">
                <span>Agentes</span>
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
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none">
                                <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="#8ab4f8"/>
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
                                <line x1="16" y1="13" x2="8" y2="13"/>
                                <line x1="16" y1="17" x2="8" y2="17"/>
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
                <span>Recentes</span>
            </div>
            <div class="recent-list">
                <div class="recent-item" onclick="promptPreFill('Qual é o status de conformidade do projeto agentic-grc-cd06?')">Auditoria ISO 27001 - agentic-grc-cd06</div>
                <div class="recent-item" onclick="promptPreFill('Executar auditoria das 4 fases em todos os projetos')">Scan Fases 1 a 4 - Staging & Prod</div>
                <div class="recent-item" onclick="promptPreFill('Analisar requisitos de Ação Climática Amd 1:2024')">Resiliência Amd 1:2024</div>
            </div>
        </div>

        <!-- Bottom Left: Escopo de Projetos & Perfil (Requested by User) -->
        <div class="sidebar-bottom">
            <!-- Escopo de Projetos -->
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
                    <!-- Dynamic project items injected via JS -->
                </div>
            </div>

            <!-- User Profile Row -->
            <div class="user-profile-row">
                <div class="user-left">
                    <div class="user-avatar">JS</div>
                    <div class="user-meta">
                        <span class="user-name">Joabson Saccomani</span>
                        <span class="user-plan">Enterprise / GEAP</span>
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
                <span class="top-active-agent" id="topActiveTitle">Chatbot Auditor</span>
                <span style="color: var(--text-tertiary)">/</span>
                <span style="color: var(--text-secondary); font-size: 13px;" id="topProjectCountBadge">1 projeto no escopo</span>
            </div>

            <div class="top-right-actions">
                <div class="top-status-indicator">
                    <span class="status-dot"></span>
                    <span>Vertex AI gemini-2.5-flash</span>
                </div>

                <div class="dropdown" id="exportDropdown">
                    <button class="btn-action-primary" onclick="toggleExportMenu()">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                        Exportar Relatório
                    </button>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="javascript:void(0)" onclick="window.print()">
                            <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor">
                                <polyline points="6 9 6 2 18 2 18 9"/>
                                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                                <rect x="6" y="14" width="12" height="8"/>
                            </svg>
                            Imprimir / Salvar PDF
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

            <!-- View 1: Chatbot Auditor (Gemini Native Chat Experience) -->
            <section class="view-pane active" id="view-chat">
                <div class="chat-view-container">
                    <div class="chat-messages-area" id="chatArea">
                        <!-- Hero Screen (Shown when empty) -->
                        <div class="gemini-hero" id="geminiHero">
                            <div class="hero-avatar">
                                <svg viewBox="0 0 24 24" width="36" height="36" fill="none">
                                    <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="url(#gemini-hero-grad)"/>
                                    <defs>
                                        <linearGradient id="gemini-hero-grad" x1="2" y1="2" x2="22" y2="22">
                                            <stop stop-color="#4285F4"/>
                                            <stop offset="0.33" stop-color="#9B72CB"/>
                                            <stop offset="0.66" stop-color="#D96570"/>
                                            <stop offset="1" stop-color="#F2A600"/>
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <h1 class="hero-title">Gemini Enterprise Auditor</h1>
                            <p class="hero-subtitle">
                                Auditor cognitivo de conformidade contínua integrado à telemetria real do Google Cloud para a ISO/IEC 27001:2022 e Amd 1:2024 de Ação Climática.
                            </p>

                            <div class="hero-suggestions-stack">
                                <div class="hero-suggestion-card" onclick="promptPreFill('Qual é o status de conformidade atual dos projetos no escopo?')">
                                    <span>Qual é o status de conformidade atual dos projetos no escopo?</span>
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                        <polyline points="9 18 15 12 9 6"/>
                                    </svg>
                                </div>
                                <div class="hero-suggestion-card" onclick="promptPreFill('Executar auditoria por fases (Fase 1 a 4) e gerar evidências')">
                                    <span>Executar auditoria por fases (Fase 1 a 4) e gerar evidências</span>
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                        <polyline points="9 18 15 12 9 6"/>
                                    </svg>
                                </div>
                                <div class="hero-suggestion-card" onclick="promptPreFill('Como está a aderência à emenda de Ação Climática (Amd 1:2024)?')">
                                    <span>Como está a aderência à emenda de Ação Climática (Amd 1:2024)?</span>
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                        <polyline points="9 18 15 12 9 6"/>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Floating Gemini Input Box -->
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
                            <textarea id="chatInput" class="chat-textarea" placeholder="Pergunte ao Gemini Auditor..." rows="1" onkeydown="handleChatKey(event)" oninput="handleChatInput(this)"></textarea>
                            <button id="sendBtn" class="btn-send" onclick="sendChatMessage()" title="Enviar mensagem">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5">
                                    <line x1="12" y1="19" x2="12" y2="5"/>
                                    <polyline points="5 12 12 5 19 12"/>
                                </svg>
                            </button>
                        </div>
                        <div class="chat-disclaimer">
                            A IA generativa pode apresentar informações imprecisas. Valide as evidências críticas no Grafo de Evidências SHA-256.
                        </div>
                    </div>
                </div>
            </section>

            <!-- View 2: Scan por Fases -->
            <section class="view-pane" id="view-phases">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Scan de Auditoria por Fases</h2>
                        <p>Pipeline estruturado de 4 fases para auditoria técnica, governança e selamento criptográfico.</p>
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
                    </div>

                    <div class="phase-card" id="cardPhase2">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 2</span>
                            <span class="phase-status-tag" id="statusPhase2">Pronto</span>
                        </div>
                        <div class="phase-name">Auditoria Técnica & IaC</div>
                        <div class="phase-desc">Scan de templates Terraform, portas abertas, VPC Service Controls e Cloud KMS (A.8.9, A.8.24).</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase2"></div></div>
                    </div>

                    <div class="phase-card" id="cardPhase3">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 3</span>
                            <span class="phase-status-tag" id="statusPhase3">Pronto</span>
                        </div>
                        <div class="phase-name">Governança & Clima</div>
                        <div class="phase-desc">Org Policies e avaliação da emenda Amd 1:2024 de Ação Climática (Cláusulas 4.1 e 4.2).</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase3"></div></div>
                    </div>

                    <div class="phase-card" id="cardPhase4">
                        <div class="phase-badge-row">
                            <span class="phase-step-num">Fase 4</span>
                            <span class="phase-status-tag" id="statusPhase4">Pronto</span>
                        </div>
                        <div class="phase-name">Grafo & Assinatura</div>
                        <div class="phase-desc">Consolidação e ancoragem de evidências com hashes SHA-256 no grafo imutável.</div>
                        <div class="phase-progress-bar"><div class="phase-progress-fill" id="fillPhase4"></div></div>
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
                            <span class="log-msg">Motor de auditoria pronto para inicialização das 4 fases nos projetos selecionados.</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- View 3: Matriz ISO 27001 Escalável -->
            <section class="view-pane" id="view-matrix">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Matriz de Controles ISO/IEC 27001:2022</h2>
                        <p>Catálogo escalável cobrindo A.5, A.6, A.7, A.8 e a nova emenda Amd 1:2024 de Ação Climática.</p>
                    </div>
                </div>

                <div class="matrix-toolbar">
                    <div class="matrix-filter-pills" id="matrixFilterPills">
                        <button class="btn-filter-pill active" onclick="filterMatrixByTheme('Todos')">Todos</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.5 Organizacional')">A.5 Organizacional</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.6 Pessoas')">A.6 Pessoas</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.7 Físico')">A.7 Físico</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('A.8 Tecnológico')">A.8 Tecnológico</button>
                        <button class="btn-filter-pill" onclick="filterMatrixByTheme('Amd 1:2024 Clima')">Amd 1:2024 Clima</button>
                    </div>

                    <div class="search-box-wrap">
                        <span class="search-icon-pos">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor">
                                <circle cx="11" cy="11" r="8"/>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                            </svg>
                        </span>
                        <input type="text" id="matrixSearchInput" class="search-input" placeholder="Buscar controle ou serviço GCP..." oninput="searchMatrix(this.value)">
                    </div>
                </div>

                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="width: 90px;">Código</th>
                                <th style="width: 200px;">Nome do Controle</th>
                                <th style="width: 140px;">Domínio</th>
                                <th>Mapeamento GCP & Implementação</th>
                                <th style="width: 110px;">Status</th>
                                <th style="width: 90px;">Severidade</th>
                            </tr>
                        </thead>
                        <tbody id="matrixTableBody">
                            <!-- Injected by JS -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- View 4: Subagentes & Zero-Copy -->
            <section class="view-pane" id="view-connectors">
                <div class="section-header-banner">
                    <div class="view-title-group">
                        <h2>Subagentes & Conectores Zero-Copy</h2>
                        <p>Integração com repositórios externos (Google Drive, SharePoint, Jira) sem replicação de dados.</p>
                    </div>
                    <button class="btn-confirm" onclick="openStorageModal()">
                        Conectar Repositório
                    </button>
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
                                <div style="font-size: 11px; color: var(--google-green)">Online</div>
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
                                <div style="font-size: 11px; color: var(--google-green)">Online</div>
                            </div>
                        </div>
                        <div class="card-desc">Monitora emendas regulatórias globais e propõe aditamentos à política (ex.: Amd 1:2024 de Ação Climática).</div>
                        <button class="btn-action-primary" onclick="triggerSubagent('horizon_scanner', 'climate_action')" style="margin-top: auto;">Executar Horizon Scan</button>
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
                                <div style="font-size: 11px; color: var(--google-green)" id="driveStatusText">Conectado</div>
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
                                <div style="font-size: 11px; color: var(--google-green)">Online</div>
                            </div>
                        </div>
                        <div class="card-desc">Varredura estática de templates de infraestrutura como código para validação prévia de conformidade.</div>
                        <button class="btn-action-primary" onclick="openUploadModal()" style="margin-top: auto;">Analisar Template IaC</button>
                    </div>
                </div>
            </section>

            <!-- View 5: Scorecard & Grafo de Evidências -->
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
                        <div class="stat-val" style="color: var(--google-green);" id="scoreDisplay">100.0%</div>
                        <div style="font-size: 12px; color: var(--text-secondary)">Classificação: EXCELLENT</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Nós no Grafo de Evidências</div>
                        <div class="stat-val" id="evidenceNodesDisplay">24</div>
                        <div style="font-size: 12px; color: var(--google-green)">Assinatura Criptográfica: SHA-256</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Proteção de Borda IA</div>
                        <div class="stat-val" style="color: var(--gemini-blue);">Ativo</div>
                        <div style="font-size: 12px; color: var(--text-secondary)">Model Armor (Anti-Jailbreak / DLP)</div>
                    </div>
                </div>

                <div class="card-panel" style="margin-top: 16px;">
                    <div class="card-title">Aprovações Humanas Pendentes (Human-in-the-Loop)</div>
                    <div class="card-desc">
                        Aditamento de Política para Incorporação da Emenda Amd 1:2024 (Ação Climática) proposto pelo Horizon Scanner.
                    </div>
                    <div style="display: flex; gap: 10px; margin-top: 12px;">
                        <button class="btn-confirm" onclick="approveRemediation('HITL-AMENDMENT-001')">
                            Aprovar Aditamento à Política
                        </button>
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

        // Initialization
        document.addEventListener("DOMContentLoaded", () => {
            loadProjects();
            loadIsoMatrix();
        });

        // Sidebar Toggle
        function toggleSidebar() {
            const sidebar = document.getElementById("appSidebar");
            sidebar.classList.toggle("collapsed");
        }

        // View Switching (Fluid Transitions)
        function switchView(viewId) {
            document.querySelectorAll(".view-pane").forEach(p => p.classList.remove("active"));
            const target = document.getElementById(viewId);
            if (target) target.classList.add("active");

            // Update sidebar agent active states
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

            // Update top bar breadcrumb
            const titleMap = {
                "view-chat": "Chatbot Auditor",
                "view-phases": "Scan por Fases",
                "view-matrix": "Matriz ISO 27001 Escalável",
                "view-connectors": "Subagentes & Zero-Copy",
                "view-scorecard": "Scorecard & Grafo de Evidências"
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
            document.getElementById("topProjectCountBadge").innerText = `${count} ${count === 1 ? 'projeto' : 'projetos'} no escopo`;
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
            document.getElementById("topProjectCountBadge").innerText = `${count} ${count === 1 ? 'projeto' : 'projetos'} no escopo`;
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

            // Append User Message
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

            // Append Typing Indicator
            const botRow = document.createElement("div");
            botRow.className = "msg-row bot";
            botRow.innerHTML = `
                <div class="msg-avatar gemini">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none">
                        <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="url(#gemini-star-grad)"/>
                    </svg>
                </div>
                <div class="msg-content" id="activeBotReply">
                    <span style="color: var(--text-tertiary)">Gemini Auditor consultando Grafo de Evidências e telemetria GCP...</span>
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
                replyElem.innerHTML = formatMarkdown(data.response || "Sem resposta do auditor.");
            } catch (err) {
                const replyElem = document.getElementById("activeBotReply");
                replyElem.removeAttribute("id");
                replyElem.innerHTML = `<span style="color: var(--google-red)">Erro na comunicação com o agente: ${err}</span>`;
            }
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        // Phased Audit Execution
        async function triggerPhasedAudit() {
            const projects = Array.from(selectedProjectIds);
            const consoleBox = document.getElementById("auditLogsContainer");
            consoleBox.innerHTML = "";

            appendLog(`Iniciando Scan de Auditoria estruturado em 4 Fases para [${projects.join(', ')}]...`, "info");

            // Reset progress
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

                // Complete each phase visual
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

        // ISO Matrix Handling
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
                tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-tertiary); padding: 24px;">Nenhum controle encontrado.</td></tr>`;
                return;
            }

            items.forEach(c => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><span class="ctrl-id-badge">${c.id}</span></td>
                    <td style="font-weight: 500;">${escapeHtml(c.name)}</td>
                    <td style="color: var(--text-secondary);">${escapeHtml(c.theme)}</td>
                    <td style="line-height: 1.5;">${escapeHtml(c.gcp_mapping)}</td>
                    <td><span class="status-badge compliant">${c.status}</span></td>
                    <td><span style="font-size: 11px; color: ${c.severity === 'CRITICAL' ? 'var(--google-red)' : 'var(--text-secondary)'}">${c.severity}</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filterMatrixByTheme(theme) {
            currentThemeFilter = theme;
            document.querySelectorAll(".btn-filter-pill").forEach(b => {
                b.classList.toggle("active", b.innerText === theme);
            });
            const searchVal = document.getElementById("matrixSearchInput").value;
            loadIsoMatrix(currentThemeFilter, searchVal);
        }

        function searchMatrix(val) {
            loadIsoMatrix(currentThemeFilter, val);
        }

        // Subagents & Storage triggers
        async function triggerSubagent(subagent, target) {
            switchView("view-chat");
            promptPreFill(`Executar agente ${subagent} no alvo ${target}`);
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
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none">
                            <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="url(#gemini-star-grad)"/>
                        </svg>
                    </div>
                    <div class="msg-content">
                        <strong>Relatório de Varredura IaC (${escapeHtml(data.filename)}):</strong><br>
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

        // Utility: escape HTML
        function escapeHtml(text) {
            const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
            return String(text).replace(/[&<>"']/g, m => map[m]);
        }

        // Utility: simple markdown formatter
        function formatMarkdown(md) {
            let html = md
                .replace(/^### (.*$)/gim, '<h3 style="margin: 16px 0 8px 0; color: var(--text-primary); font-size: 16px;">$1</h3>')
                .replace(/^## (.*$)/gim, '<h2 style="margin: 20px 0 10px 0; color: var(--text-primary); font-size: 18px;">$1</h2>')
                .replace(/^# (.*$)/gim, '<h1 style="margin: 24px 0 12px 0; color: var(--text-primary); font-size: 20px;">$1</h1>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/gim, '<em>$1</em>')
                .replace(/`([^`]+)`/gim, '<code style="background: #282a2c; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 12.5px;">$1</code>')
                .replace(/^\* (.*$)/gim, '<li style="margin-left: 20px;">$1</li>')
                .replace(/\n\n/gim, '<br><br>');
            return html;
        }
    </script>
</body>
</html>
"""
