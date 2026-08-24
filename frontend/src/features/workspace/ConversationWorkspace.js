import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Fragment, useEffect, useMemo, useRef, useState, } from "react";
import { Bot, ExternalLink, UserRound, } from "lucide-react";
import { researchAnswer, } from "../../api/research";
import ResearchInputDock from "./ResearchInputDock";
import { THREAD_SELECTED_EVENT, conversationTitle, ensureActiveThread, loadConversationThreads, saveConversationThread, } from "./conversationHistory";
import "./ConversationWorkspace.css";
function messageId(prefix) {
    if (typeof crypto !== "undefined" &&
        typeof crypto.randomUUID === "function") {
        return `${prefix}-${crypto.randomUUID()}`;
    }
    return (`${prefix}-${Date.now()}-` +
        Math.random().toString(36).slice(2));
}
function inlineContent(value) {
    const parts = value.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    return parts
        .filter(Boolean)
        .map((part, index) => {
        if (part.startsWith("**") &&
            part.endsWith("**")) {
            return (_jsx("strong", { children: part.slice(2, -2) }, index));
        }
        if (part.startsWith("`") &&
            part.endsWith("`")) {
            return (_jsx("code", { children: part.slice(1, -1) }, index));
        }
        return (_jsx(Fragment, { children: part }, index));
    });
}
function RichText({ content, }) {
    const blocks = useMemo(() => content
        .replace(/\r\n/g, "\n")
        .split("\n"), [content]);
    return (_jsx("div", { className: "delbot-rich-text", children: blocks.map((line, index) => {
            const trimmed = line.trim();
            if (!trimmed) {
                return (_jsx("div", { className: "delbot-text-space" }, index));
            }
            if (/^[-*_]{3,}$/.test(trimmed)) {
                return _jsx("hr", {}, index);
            }
            const heading = trimmed.match(/^(#{1,3})\s+(.+)$/);
            if (heading) {
                return (_jsx("div", { className: "delbot-text-heading", children: inlineContent(heading[2]) }, index));
            }
            const bullet = trimmed.match(/^[-•◆▪]\s+(.+)$/);
            if (bullet) {
                return (_jsxs("div", { className: "delbot-text-list-row", children: [_jsx("span", { className: "delbot-text-bullet", "aria-hidden": "true", children: "\u2022" }), _jsx("span", { children: inlineContent(bullet[1]) })] }, index));
            }
            const numbered = trimmed.match(/^(\d+)[.)]\s+(.+)$/);
            if (numbered) {
                return (_jsxs("div", { className: "delbot-text-list-row", children: [_jsxs("span", { className: "delbot-text-number", children: [numbered[1], "."] }), _jsx("span", { children: inlineContent(numbered[2]) })] }, index));
            }
            return (_jsx("p", { children: inlineContent(trimmed) }, index));
        }) }));
}
function citationTitle(citation) {
    return (citation.document?.title ||
        citation.document_title ||
        citation.document?.document_id ||
        citation.document_id ||
        "Repository source");
}
function CitationList({ citations, }) {
    if (citations.length === 0) {
        return null;
    }
    return (_jsxs("details", { className: "delbot-citations", children: [_jsxs("summary", { children: [citations.length, " repository", citations.length === 1
                        ? " source"
                        : " sources"] }), _jsx("div", { className: "delbot-citation-list", children: citations.map((citation, index) => (_jsxs("div", { className: "delbot-citation-card", children: [_jsx("div", { className: "delbot-citation-index", children: index + 1 }), _jsxs("div", { className: "delbot-citation-copy", children: [_jsx("strong", { children: citationTitle(citation) }), _jsx("span", { children: citation.page
                                        ? `Page ${citation.page}`
                                        : "Repository evidence" }), citation.text ? (_jsxs("p", { children: [citation.text
                                            .replace(/\s+/g, " ")
                                            .trim()
                                            .slice(0, 220), citation.text.length >
                                            220
                                            ? "…"
                                            : ""] })) : null] }), citation.document
                            ?.file_path ? (_jsx(ExternalLink, { size: 14, "aria-hidden": "true" })) : null] }, `${citationTitle(citation)}-${index}`))) })] }));
}
function Bubble({ message, }) {
    const isUser = message.role === "user";
    return (_jsxs("article", { className: [
            "delbot-message",
            isUser
                ? "delbot-message-user"
                : "delbot-message-assistant",
        ].join(" "), children: [_jsx("div", { className: [
                    "delbot-message-avatar",
                    isUser
                        ? "delbot-avatar-user"
                        : "delbot-avatar-assistant",
                ].join(" "), "aria-hidden": "true", children: isUser ? (_jsx(UserRound, { size: 15 })) : (_jsx(Bot, { size: 15 })) }), _jsxs("div", { className: "delbot-message-column", children: [_jsx("div", { className: "delbot-message-author", children: isUser ? "You" : "DELBot" }), _jsx("div", { className: "delbot-message-bubble", children: _jsx(RichText, { content: message.content }) }), !isUser ? (_jsx(CitationList, { citations: message.citations ?? [] })) : null] })] }));
}
export default function ConversationWorkspace() {
    const initialThread = useMemo(() => ensureActiveThread(), []);
    const [thread, setThread,] = useState(initialThread);
    const [messages, setMessages,] = useState(initialThread.messages);
    const [loading, setLoading,] = useState(false);
    const bottomRef = useRef(null);
    useEffect(() => {
        const handleThreadSelection = (event) => {
            const selectedId = event.detail;
            const selected = loadConversationThreads().find((candidate) => candidate.id ===
                selectedId);
            if (!selected) {
                return;
            }
            setThread(selected);
            setMessages(selected.messages);
            setLoading(false);
        };
        window.addEventListener(THREAD_SELECTED_EVENT, handleThreadSelection);
        return () => {
            window.removeEventListener(THREAD_SELECTED_EVENT, handleThreadSelection);
        };
    }, []);
    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages, loading]);
    const persistMessages = (nextMessages, nextSessionId = thread.sessionId) => {
        const nextThread = saveConversationThread({
            ...thread,
            sessionId: nextSessionId,
            title: conversationTitle(nextMessages),
            messages: nextMessages,
        });
        setThread(nextThread);
        setMessages(nextThread.messages);
    };
    const handleSubmit = async (question) => {
        if (loading) {
            return;
        }
        const userMessage = {
            id: messageId("user"),
            role: "user",
            content: question,
            createdAt: Date.now(),
        };
        const pendingMessages = [
            ...messages,
            userMessage,
        ];
        persistMessages(pendingMessages);
        setLoading(true);
        try {
            const response = await researchAnswer(question, thread.sessionId);
            const payload = response.data;
            const assistantMessage = {
                id: messageId("assistant"),
                role: "assistant",
                content: String(payload.answer ?? "").trim() ||
                    "DELBot tidak menerima jawaban yang dapat ditampilkan.",
                citations: Array.isArray(payload.citations)
                    ? payload.citations
                    : [],
                createdAt: Date.now(),
            };
            persistMessages([
                ...pendingMessages,
                assistantMessage,
            ], payload.session_id ||
                thread.sessionId);
        }
        catch (error) {
            const message = error instanceof Error
                ? error.message
                : "Unknown request error";
            const errorMessage = {
                id: messageId("assistant"),
                role: "assistant",
                content: "Permintaan belum berhasil diproses. " +
                    `Silakan coba lagi. (${message})`,
                citations: [],
                createdAt: Date.now(),
            };
            persistMessages([
                ...pendingMessages,
                errorMessage,
            ]);
        }
        finally {
            setLoading(false);
        }
    };
    const empty = messages.length === 0;
    return (_jsx("section", { className: "delbot-conversation-workspace", children: _jsxs("div", { className: "delbot-conversation-stage", children: [_jsx("div", { className: [
                        "delbot-message-viewport",
                        empty
                            ? "delbot-message-viewport-empty"
                            : "",
                    ]
                        .filter(Boolean)
                        .join(" "), children: empty ? (_jsxs("div", { className: "delbot-empty-state", children: [_jsx("span", { className: "delbot-empty-eyebrow", children: "Research Workspace" }), _jsx("h1", { children: "Apa yang sedang kamu kerjakan?" }), _jsx("p", { children: "Mulai dari pertanyaan, topik, draft ide, atau percakapan biasa." })] })) : (_jsxs("div", { className: "delbot-message-list", children: [messages.map((message) => (_jsx(Bubble, { message: message }, message.id))), loading ? (_jsxs("div", { className: "delbot-thinking", children: [_jsx(Bot, { size: 15 }), _jsx("span", { children: "DELBot is thinking" }), _jsx("i", {}), _jsx("i", {}), _jsx("i", {})] })) : null, _jsx("div", { ref: bottomRef })] })) }), _jsx(ResearchInputDock, { loading: loading, empty: empty, onSubmit: handleSubmit })] }) }));
}
