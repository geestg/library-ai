import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState, } from "react";
import { BookOpen, Database, MessageSquare, MessageSquarePlus, Trash2, } from "lucide-react";
import { NavLink, useLocation, useNavigate, } from "react-router-dom";
import { HISTORY_UPDATED_EVENT, THREAD_SELECTED_EVENT, createConversationThread, loadConversationThreads, removeConversationThread, selectConversationThread, } from "../../features/workspace/conversationHistory";
import "./WorkspaceSidebar.css";
function relativeTime(timestamp) {
    const elapsed = Math.max(0, Date.now() - timestamp);
    const minute = 60_000;
    const hour = 60 * minute;
    const day = 24 * hour;
    if (elapsed < minute) {
        return "Now";
    }
    if (elapsed < hour) {
        return `${Math.floor(elapsed / minute)}m`;
    }
    if (elapsed < day) {
        return `${Math.floor(elapsed / hour)}h`;
    }
    return `${Math.floor(elapsed / day)}d`;
}
export default function WorkspaceSidebar() {
    const navigate = useNavigate();
    const location = useLocation();
    const [threads, setThreads,] = useState(() => loadConversationThreads());
    const [activeThreadId, setActiveThread,] = useState(() => typeof localStorage !== "undefined"
        ? localStorage.getItem("delbot_active_thread_id")
        : null);
    const refreshThreads = () => {
        setThreads(loadConversationThreads());
        setActiveThread(typeof localStorage !== "undefined"
            ? localStorage.getItem("delbot_active_thread_id")
            : null);
    };
    useEffect(() => {
        window.addEventListener(HISTORY_UPDATED_EVENT, refreshThreads);
        window.addEventListener(THREAD_SELECTED_EVENT, refreshThreads);
        return () => {
            window.removeEventListener(HISTORY_UPDATED_EVENT, refreshThreads);
            window.removeEventListener(THREAD_SELECTED_EVENT, refreshThreads);
        };
    }, []);
    const openThread = (threadId) => {
        selectConversationThread(threadId);
        setActiveThread(threadId);
        if (location.pathname !== "/") {
            navigate("/");
        }
    };
    const startConversation = () => {
        const created = createConversationThread();
        setActiveThread(created.id);
        refreshThreads();
        if (location.pathname !== "/") {
            navigate("/");
        }
        window.dispatchEvent(new CustomEvent(THREAD_SELECTED_EVENT, {
            detail: created.id,
        }));
    };
    const visibleThreads = threads.filter((thread) => thread.messages.length > 0);
    return (_jsxs("aside", { className: "delbot-sidebar", children: [_jsxs("div", { className: "delbot-sidebar-brand", children: [_jsx("div", { className: "delbot-brand-mark", children: "D" }), _jsxs("div", { children: [_jsx("strong", { children: "DELBot" }), _jsx("span", { children: "Academic workspace" })] })] }), _jsxs("nav", { className: "delbot-sidebar-navigation", "aria-label": "Primary navigation", children: [_jsxs(NavLink, { to: "/", end: true, className: ({ isActive }) => isActive
                            ? "delbot-nav-link active"
                            : "delbot-nav-link", children: [_jsx(BookOpen, { size: 17 }), _jsx("span", { children: "Research Workspace" })] }), _jsxs(NavLink, { to: "/repository", className: ({ isActive }) => isActive
                            ? "delbot-nav-link active"
                            : "delbot-nav-link", children: [_jsx(Database, { size: 17 }), _jsx("span", { children: "Repository" })] })] }), _jsx("div", { className: "delbot-sidebar-divider" }), _jsxs("button", { type: "button", className: "delbot-new-conversation", onClick: startConversation, children: [_jsx(MessageSquarePlus, { size: 16 }), _jsx("span", { children: "Percakapan baru" })] }), _jsxs("section", { className: "delbot-thread-section", children: [_jsx("div", { className: "delbot-thread-heading", children: "Recent" }), _jsx("div", { className: "delbot-thread-list", children: visibleThreads.length ===
                            0 ? (_jsx("p", { className: "delbot-no-threads", children: "Percakapan akan muncul di sini." })) : (visibleThreads.map((thread) => (_jsxs("div", { className: [
                                "delbot-thread-item",
                                activeThreadId ===
                                    thread.id
                                    ? "active"
                                    : "",
                            ]
                                .filter(Boolean)
                                .join(" "), children: [_jsxs("button", { type: "button", className: "delbot-thread-open", onClick: () => {
                                        openThread(thread.id);
                                    }, children: [_jsx(MessageSquare, { size: 14 }), _jsxs("span", { className: "delbot-thread-copy", children: [_jsx("strong", { children: thread.title }), _jsx("small", { children: relativeTime(thread.updatedAt) })] })] }), _jsx("button", { type: "button", className: "delbot-thread-delete", "aria-label": `Delete ${thread.title}`, onClick: () => {
                                        const next = removeConversationThread(thread.id);
                                        refreshThreads();
                                        if (activeThreadId ===
                                            thread.id) {
                                            window.dispatchEvent(new CustomEvent(THREAD_SELECTED_EVENT, {
                                                detail: next.id,
                                            }));
                                        }
                                    }, children: _jsx(Trash2, { size: 13 }) })] }, thread.id)))) })] })] }));
}
