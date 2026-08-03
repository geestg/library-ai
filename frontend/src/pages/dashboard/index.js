import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useRef, useState } from "react";
const WORKSPACE_STORAGE = "workspace_sessions";
const ACTIVE_WORKSPACE = "active_workspace";
const STORAGE_KEY = "delbot_workspace";
const STREAM_DELAY = 8;
export default function DashboardPage() {
    const conversationRef = useRef(null);
    const [loadingRepository, setLoadingRepository] = useState(true);
    const [loadingResearch, setLoadingResearch] = useState(false);
    const [prompt, setPrompt] = useState("");
    const [messages, setMessages] = useState([]);
    const [workspaceSessions, setWorkspaceSessions] = useState([]);
    const [activeWorkspaceId, setActiveWorkspaceId] = useState("");
    const [result, setResult] = useState(null);
    const [summary, setSummary] = useState({
        total: 0,
        pdf_available: 0,
        pdf_missing: 0,
    });
    const id = Date.now().toString();
    const session = {
        id: crypto.randomUUID(),
        title: "New Conversation",
        preview: "",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        messages: [],
        result: null,
    };
    setWorkspaceSessions((prev) => [
        session,
        ...prev,
    ]);
    setActiveWorkspaceId(id);
    setMessages([]);
    setResult(null);
    setPrompt("");
}
function switchWorkspace(id) {
    setActiveWorkspaceId(id);
}
function renameWorkspace(id) {
    const name = window.prompt("Conversation title");
    if (!name) {
        return;
    }
    setWorkspaceSessions(prev => prev.map(item => item.id === id
        ? {
            ...item,
            title: name,
        }
        : item));
}
function deleteWorkspace(id) {
    if (!window.confirm("Delete conversation?")) {
        return;
    }
    const next = workspaceSessions.filter(item => item.id !== id);
    setWorkspaceSessions(next);
    if (activeWorkspaceId === id) {
        if (next.length > 0) {
            setActiveWorkspaceId(next[0].id);
        }
    }
}
return (_jsx("div", { style: {
        padding: 32,
    }, children: _jsxs("div", { style: {
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: 16,
            padding: 24,
        }, children: [_jsx("h1", { style: {
                    margin: 0,
                    fontSize: 32,
                }, children: "AI Research Workspace" }), _jsx("p", { style: {
                    color: "#64748b",
                    marginTop: 12,
                    lineHeight: 1.8,
                }, children: "Dashboard recovery completed. Workspace will be restored gradually." })] }) }));
