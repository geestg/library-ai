import { jsx as _jsx } from "react/jsx-runtime";
import { useEffect, useRef, useState } from "react";
import { FolderOpen, Search, Files, } from "lucide-react";
import { repositoryExplorer } from "../../api/repository";
import { researchAnswer } from "../../api/research";
const WORKSPACE_STORAGE = "workspace_sessions";
const ACTIVE_WORKSPACE = "active_workspace";
const STORAGE_KEY = "delbot_workspace";
const STREAM_DELAY = 8;
const sidebarStyle = {
    width: 260,
    background: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 16,
    height: "fit-content",
};
const workspaceToolbarStyle = {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
    marginBottom: 16,
};
// WORKSPACE_TOOLBAR_STYLE
const workspaceButtonStyle = {
    width: "100%",
    textAlign: "left",
    padding: "10px 12px",
    marginBottom: 8,
    border: "1px solid #e5e7eb",
    borderRadius: 8,
    background: "#f8fafc",
    cursor: "pointer",
};
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import ConversationWorkspace from "../../features/workspace/ConversationWorkspace";
export default function DashboardPage() {
    const conversationRef = useRef(null);
    const [loadingRepository, setLoadingRepository] = useState(true);
    const [loadingResearch, setLoadingResearch] = useState(false);
    const [prompt, setPrompt] = useState("");
    const [messages, setMessages] = useState([]);
    const [result, setResult] = useState(null);
    const [workspaceSessions, setWorkspaceSessions] = useState([]);
    const [activeWorkspaceId, setActiveWorkspaceId] = useState("");
    const [summary, setSummary] = useState({
        total: 0,
        pdf_available: 0,
        pdf_missing: 0,
    });
    const [workspaces, setWorkspaces] = useState([]);
    // WORKSPACE_LIST_POLISH
    useEffect(() => {
        repositoryExplorer()
            .then((res) => {
            setSummary({
                total: res.data.total ?? 0,
                pdf_available: res.data.pdf_available ?? 0,
                pdf_missing: res.data.pdf_missing ?? 0,
            });
        })
            .catch(console.error)
            .finally(() => setLoadingRepository(false));
    }, []);
    useEffect(() => {
        try {
            const saved = localStorage.getItem(WORKSPACE_STORAGE);
            const active = localStorage.getItem(ACTIVE_WORKSPACE);
            if (saved) {
                setWorkspaceSessions(JSON.parse(saved));
            }
            if (active) {
                setActiveWorkspaceId(active);
            }
        }
        catch (error) {
            console.error(error);
        }
    }, []);
    useEffect(() => {
        const saved = sessionStorage.getItem(STORAGE_KEY);
        if (!saved) {
            return;
        }
        try {
            const data = JSON.parse(saved);
            setMessages(data.messages ?? []);
            setResult(data.result ?? null);
        }
        catch {
            console.error("Invalid workspace session.");
        }
    }, []);
    useEffect(() => {
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
            messages,
            result,
        }));
        conversationRef.current?.scrollTo({
            top: conversationRef.current.scrollHeight,
            behavior: "smooth",
        });
    }, [messages, result]);
    // AUTO_WORKSPACE_SAVE
    useEffect(() => {
        if (!activeWorkspaceId) {
            return;
        }
        setWorkspaces(prev => prev.map(item => item.id === activeWorkspaceId
            ? {
                ...item,
                updated_at: new Date().toISOString(),
                messages,
                result,
            }
            : item));
    }, [messages, result, activeWorkspaceId]);
    // RESTORE_WORKSPACE_SESSION
    useEffect(() => {
        if (!activeWorkspaceId) {
            return;
        }
        const current = workspaceSessions.find(item => item.id === activeWorkspaceId);
        if (!current) {
            return;
        }
        setMessages(current.messages ?? []);
        setResult(current.result ?? null);
    }, [activeWorkspaceId]);
    async function streamAnswer(answer) {
        let text = "";
        setMessages(prev => [
            ...prev,
            {
                role: "assistant",
                content: "",
            },
        ]);
        for (const ch of answer) {
            text += ch;
            setMessages(prev => {
                const copy = [...prev];
                copy[copy.length - 1] = {
                    role: "assistant",
                    content: text,
                };
                const activeWorkspaceButtonStyle = {
                    ...workspaceButtonStyle,
                    background: "#eef2ff",
                    border: "1px solid #6366f1",
                    fontWeight: 600,
                };
                return copy;
            });
            await new Promise(resolve => setTimeout(resolve, STREAM_DELAY));
        }
    }
    async function askAI(question) {
        const current = (question ?? prompt).trim();
        if (!current) {
            return;
        }
        setMessages(prev => [
            ...prev,
            {
                role: "user",
                content: current,
            },
        ]);
        setPrompt("");
        setLoadingResearch(true);
        try {
            const response = await researchAnswer(current);
            const data = response.data;
            setResult(data);
            await streamAnswer(data.answer);
        }
        catch {
            setMessages(prev => [
                ...prev,
                {
                    role: "assistant",
                    content: "Unable to answer this question.",
                },
            ]);
        }
        finally {
            setLoadingResearch(false);
        }
    }
    function clearWorkspace() {
        sessionStorage.removeItem(STORAGE_KEY);
        setMessages([]);
        setResult(null);
        setPrompt("");
    }
    const quickPrompts = [
        "Summarize repository.",
        "Identify the main research gaps in the retrieved academic literature. Focus on limitations, unresolved problems, findings, recommendations, future work, and aspects not yet addressed. Ignore table of contents, lists of figures, lists of tables, appendices, bibliography, page numbers, and navigation text. Do not summarize the documents. Return 3 concise numbered gaps with Gap, Evidence, Limitation, Missing Aspect, and Research Direction. Only use evidence supported by the retrieved documents.",
        "Generate feasible thesis ideas from the retrieved academic literature. Focus on research problems, limitations, findings, recommendations, future work, and unresolved aspects. Ignore table of contents, lists of figures, lists of tables, appendices, bibliography, page numbers, and navigation text. Do not summarize the documents. Return 3 concise numbered thesis ideas with Research Problem, Proposed Focus, Gap or Novelty, and Supporting Evidence. Only use evidence supported by the retrieved documents.",
        "Compare CNN and ViT.",
        "Explain recommendation systems.",
    ];
    const actions = [
        {
            title: "Repository",
            description: "Browse indexed research documents.",
            icon: FolderOpen,
            to: "/repository",
        },
        {
            title: "Semantic Search",
            description: "Search repository semantically.",
            icon: Search,
            to: "/search",
        },
        {
            title: "Document Index",
            description: "Index new PDF documents.",
            icon: Files,
            to: "/documents",
        },
    ];
    useEffect(() => {
        localStorage.setItem(WORKSPACE_STORAGE, JSON.stringify(workspaceSessions));
    }, [workspaceSessions]);
    useEffect(() => {
        localStorage.setItem("mvp_workspaces", JSON.stringify(workspaces));
    }, [workspaces]);
    useEffect(() => {
        if (!activeWorkspaceId) {
            return;
        }
        localStorage.setItem("mvp_active_workspace", activeWorkspaceId);
    }, [activeWorkspaceId]);
    useEffect(() => {
        if (activeWorkspaceId) {
            localStorage.setItem(ACTIVE_WORKSPACE, activeWorkspaceId);
        }
    }, [activeWorkspaceId]);
    function createWorkspace() {
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
    useEffect(() => {
        localStorage.setItem("mvp_workspaces", JSON.stringify(workspaces));
    }, [workspaces]);
    return (_jsx(WorkspaceShell, { children: _jsx(ConversationWorkspace, {}) }));
}
