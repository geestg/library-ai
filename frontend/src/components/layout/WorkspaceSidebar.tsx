import {
    useEffect,
    useState,
} from "react";
import {
    BookOpen,
    Database,
    MessageSquare,
    MessageSquarePlus,
    Trash2,
} from "lucide-react";
import {
    NavLink,
    useLocation,
    useNavigate,
} from "react-router-dom";

import {
    HISTORY_UPDATED_EVENT,
    THREAD_SELECTED_EVENT,
    createConversationThread,
    loadConversationThreads,
    removeConversationThread,
    selectConversationThread,
} from "../../features/workspace/conversationHistory";
import type {
    ConversationThread,
} from "../../features/workspace/conversationHistory";

import "./WorkspaceSidebar.css";

function relativeTime(timestamp: number): string {
    const elapsed = Math.max(
        0,
        Date.now() - timestamp,
    );

    const minute = 60_000;
    const hour = 60 * minute;
    const day = 24 * hour;

    if (elapsed < minute) {
        return "Now";
    }

    if (elapsed < hour) {
        return `${Math.floor(
            elapsed / minute,
        )}m`;
    }

    if (elapsed < day) {
        return `${Math.floor(
            elapsed / hour,
        )}h`;
    }

    return `${Math.floor(
        elapsed / day,
    )}d`;
}

export default function WorkspaceSidebar() {
    const navigate = useNavigate();
    const location = useLocation();

    const [
        threads,
        setThreads,
    ] = useState<ConversationThread[]>(
        () => loadConversationThreads(),
    );

    const [
        activeThreadId,
        setActiveThread,
    ] = useState<string | null>(() =>
        typeof localStorage !== "undefined"
            ? localStorage.getItem(
                  "delbot_active_thread_id",
              )
            : null,
    );

    const refreshThreads = () => {
        setThreads(
            loadConversationThreads(),
        );

        setActiveThread(
            typeof localStorage !== "undefined"
                ? localStorage.getItem(
                      "delbot_active_thread_id",
                  )
                : null,
        );
    };

    useEffect(() => {
        window.addEventListener(
            HISTORY_UPDATED_EVENT,
            refreshThreads,
        );

        window.addEventListener(
            THREAD_SELECTED_EVENT,
            refreshThreads,
        );

        return () => {
            window.removeEventListener(
                HISTORY_UPDATED_EVENT,
                refreshThreads,
            );

            window.removeEventListener(
                THREAD_SELECTED_EVENT,
                refreshThreads,
            );
        };
    }, []);

    const openThread = (
        threadId: string,
    ) => {
        selectConversationThread(
            threadId,
        );

        setActiveThread(threadId);

        if (location.pathname !== "/") {
            navigate("/");
        }
    };

    const startConversation = () => {
        const created =
            createConversationThread();

        setActiveThread(created.id);
        refreshThreads();

        if (location.pathname !== "/") {
            navigate("/");
        }

        window.dispatchEvent(
            new CustomEvent(
                THREAD_SELECTED_EVENT,
                {
                    detail: created.id,
                },
            ),
        );
    };

    const visibleThreads = threads.filter(
        (thread) =>
            thread.messages.length > 0,
    );

    return (
        <aside className="delbot-sidebar">
            <div className="delbot-sidebar-brand">
                <div className="delbot-brand-mark">
                    D
                </div>

                <div>
                    <strong>DELBot</strong>
                    <span>
                        Academic workspace
                    </span>
                </div>
            </div>

            <nav
                className="delbot-sidebar-navigation"
                aria-label="Primary navigation"
            >
                <NavLink
                    to="/"
                    end
                    className={({ isActive }) =>
                        isActive
                            ? "delbot-nav-link active"
                            : "delbot-nav-link"
                    }
                >
                    <BookOpen size={17} />
                    <span>
                        Research Workspace
                    </span>
                </NavLink>

                <NavLink
                    to="/repository"
                    className={({ isActive }) =>
                        isActive
                            ? "delbot-nav-link active"
                            : "delbot-nav-link"
                    }
                >
                    <Database size={17} />
                    <span>Repository</span>
                </NavLink>
            </nav>

            <div className="delbot-sidebar-divider" />

            <button
                type="button"
                className="delbot-new-conversation"
                onClick={startConversation}
            >
                <MessageSquarePlus size={16} />
                <span>
                    Percakapan baru
                </span>
            </button>

            <section className="delbot-thread-section">
                <div className="delbot-thread-heading">
                    Recent
                </div>

                <div className="delbot-thread-list">
                    {visibleThreads.length ===
                    0 ? (
                        <p className="delbot-no-threads">
                            Percakapan akan muncul
                            di sini.
                        </p>
                    ) : (
                        visibleThreads.map(
                            (thread) => (
                                <div
                                    key={
                                        thread.id
                                    }
                                    className={[
                                        "delbot-thread-item",
                                        activeThreadId ===
                                        thread.id
                                            ? "active"
                                            : "",
                                    ]
                                        .filter(
                                            Boolean,
                                        )
                                        .join(
                                            " ",
                                        )}
                                >
                                    <button
                                        type="button"
                                        className="delbot-thread-open"
                                        onClick={() => {
                                            openThread(
                                                thread.id,
                                            );
                                        }}
                                    >
                                        <MessageSquare
                                            size={
                                                14
                                            }
                                        />

                                        <span className="delbot-thread-copy">
                                            <strong>
                                                {
                                                    thread.title
                                                }
                                            </strong>
                                            <small>
                                                {relativeTime(
                                                    thread.updatedAt,
                                                )}
                                            </small>
                                        </span>
                                    </button>

                                    <button
                                        type="button"
                                        className="delbot-thread-delete"
                                        aria-label={
                                            `Delete ${thread.title}`
                                        }
                                        onClick={() => {
                                            const next =
                                                removeConversationThread(
                                                    thread.id,
                                                );

                                            refreshThreads();

                                            if (
                                                activeThreadId ===
                                                thread.id
                                            ) {
                                                window.dispatchEvent(
                                                    new CustomEvent(
                                                        THREAD_SELECTED_EVENT,
                                                        {
                                                            detail:
                                                                next.id,
                                                        },
                                                    ),
                                                );
                                            }
                                        }}
                                    >
                                        <Trash2
                                            size={13}
                                        />
                                    </button>
                                </div>
                            ),
                        )
                    )}
                </div>
            </section>
        </aside>
    );
}
