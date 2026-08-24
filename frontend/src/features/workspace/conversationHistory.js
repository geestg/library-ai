export const THREAD_STORAGE_KEY = "delbot_conversation_threads_v1";
export const ACTIVE_THREAD_KEY = "delbot_active_thread_id";
export const LEGACY_SESSION_KEY = "delbot_research_session_id";
export const HISTORY_UPDATED_EVENT = "delbot:history-updated";
export const THREAD_SELECTED_EVENT = "delbot:thread-selected";
export const MAX_THREADS = 20;
export const MAX_VISIBLE_MESSAGES = 12;
function createId(prefix) {
    if (typeof crypto !== "undefined" &&
        typeof crypto.randomUUID === "function") {
        return `${prefix}-${crypto.randomUUID()}`;
    }
    return (`${prefix}-${Date.now()}-` +
        Math.random().toString(36).slice(2));
}
function storageAvailable() {
    return (typeof window !== "undefined" &&
        typeof window.localStorage !== "undefined");
}
function normalizeMessage(value) {
    if (typeof value !== "object" ||
        value === null) {
        return null;
    }
    const message = value;
    if (message.role !== "user" &&
        message.role !== "assistant") {
        return null;
    }
    if (typeof message.content !== "string") {
        return null;
    }
    return {
        id: typeof message.id === "string"
            ? message.id
            : createId("message"),
        role: message.role,
        content: message.content,
        citations: Array.isArray(message.citations)
            ? message.citations
            : [],
        createdAt: typeof message.createdAt === "number"
            ? message.createdAt
            : Date.now(),
    };
}
function normalizeThread(value) {
    if (typeof value !== "object" ||
        value === null) {
        return null;
    }
    const thread = value;
    if (typeof thread.id !== "string" ||
        typeof thread.sessionId !== "string") {
        return null;
    }
    const messages = Array.isArray(thread.messages)
        ? thread.messages
            .map(normalizeMessage)
            .filter((message) => message !== null)
            .slice(-MAX_VISIBLE_MESSAGES)
        : [];
    return {
        id: thread.id,
        title: typeof thread.title === "string" &&
            thread.title.trim()
            ? thread.title
            : "Untitled conversation",
        sessionId: thread.sessionId,
        messages,
        createdAt: typeof thread.createdAt === "number"
            ? thread.createdAt
            : Date.now(),
        updatedAt: typeof thread.updatedAt === "number"
            ? thread.updatedAt
            : Date.now(),
    };
}
export function loadConversationThreads() {
    if (!storageAvailable()) {
        return [];
    }
    try {
        const raw = localStorage.getItem(THREAD_STORAGE_KEY);
        if (!raw) {
            return [];
        }
        const parsed = JSON.parse(raw);
        if (!Array.isArray(parsed)) {
            return [];
        }
        return parsed
            .map(normalizeThread)
            .filter((thread) => thread !== null)
            .sort((left, right) => right.updatedAt -
            left.updatedAt)
            .slice(0, MAX_THREADS);
    }
    catch {
        return [];
    }
}
export function storeConversationThreads(threads) {
    if (!storageAvailable()) {
        return;
    }
    localStorage.setItem(THREAD_STORAGE_KEY, JSON.stringify(threads
        .sort((left, right) => right.updatedAt -
        left.updatedAt)
        .slice(0, MAX_THREADS)));
    window.dispatchEvent(new CustomEvent(HISTORY_UPDATED_EVENT));
}
export function getActiveThreadId() {
    if (!storageAvailable()) {
        return null;
    }
    return localStorage.getItem(ACTIVE_THREAD_KEY);
}
export function setActiveThreadId(threadId) {
    if (!storageAvailable()) {
        return;
    }
    localStorage.setItem(ACTIVE_THREAD_KEY, threadId);
}
export function createConversationThread() {
    const now = Date.now();
    const thread = {
        id: createId("thread"),
        title: "Untitled conversation",
        sessionId: createId("session"),
        messages: [],
        createdAt: now,
        updatedAt: now,
    };
    const threads = loadConversationThreads();
    storeConversationThreads([
        thread,
        ...threads,
    ]);
    setActiveThreadId(thread.id);
    if (storageAvailable()) {
        localStorage.setItem(LEGACY_SESSION_KEY, thread.sessionId);
    }
    return thread;
}
export function ensureActiveThread() {
    const threads = loadConversationThreads();
    const activeId = getActiveThreadId();
    const active = threads.find((thread) => thread.id === activeId);
    if (active) {
        return active;
    }
    if (threads.length > 0) {
        setActiveThreadId(threads[0].id);
        return threads[0];
    }
    return createConversationThread();
}
export function saveConversationThread(thread) {
    const normalized = {
        ...thread,
        messages: thread.messages.slice(-MAX_VISIBLE_MESSAGES),
        updatedAt: Date.now(),
    };
    const threads = loadConversationThreads()
        .filter((candidate) => candidate.id !== normalized.id);
    storeConversationThreads([
        normalized,
        ...threads,
    ]);
    setActiveThreadId(normalized.id);
    if (storageAvailable()) {
        localStorage.setItem(LEGACY_SESSION_KEY, normalized.sessionId);
    }
    return normalized;
}
export function removeConversationThread(threadId) {
    const remaining = loadConversationThreads().filter((thread) => thread.id !== threadId);
    if (remaining.length > 0) {
        storeConversationThreads(remaining);
        setActiveThreadId(remaining[0].id);
        return remaining[0];
    }
    if (storageAvailable()) {
        localStorage.removeItem(THREAD_STORAGE_KEY);
        localStorage.removeItem(ACTIVE_THREAD_KEY);
    }
    return createConversationThread();
}
export function selectConversationThread(threadId) {
    const thread = loadConversationThreads().find((candidate) => candidate.id === threadId) ?? null;
    if (!thread) {
        return null;
    }
    setActiveThreadId(thread.id);
    if (storageAvailable()) {
        localStorage.setItem(LEGACY_SESSION_KEY, thread.sessionId);
        window.dispatchEvent(new CustomEvent(THREAD_SELECTED_EVENT, {
            detail: thread.id,
        }));
    }
    return thread;
}
export function conversationTitle(messages) {
    const firstUserMessage = messages.find((message) => message.role === "user" &&
        message.content.trim());
    if (!firstUserMessage) {
        return "Untitled conversation";
    }
    const compact = firstUserMessage.content
        .replace(/\s+/g, " ")
        .trim();
    if (compact.length <= 44) {
        return compact;
    }
    return `${compact.slice(0, 41).trim()}…`;
}
