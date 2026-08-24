import {
    Fragment,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";
import type {
    ReactNode,
} from "react";
import {
    Bot,
    ExternalLink,
    UserRound,
} from "lucide-react";

import {
    researchAnswer,
} from "../../api/research";
import ResearchInputDock from "./ResearchInputDock";
import {
    THREAD_SELECTED_EVENT,
    conversationTitle,
    ensureActiveThread,
    loadConversationThreads,
    saveConversationThread,
} from "./conversationHistory";
import type {
    CitationRecord,
    ConversationMessage,
    ConversationThread,
} from "./conversationHistory";

import "./ConversationWorkspace.css";

function messageId(prefix: string): string {
    if (
        typeof crypto !== "undefined" &&
        typeof crypto.randomUUID === "function"
    ) {
        return `${prefix}-${crypto.randomUUID()}`;
    }

    return (
        `${prefix}-${Date.now()}-` +
        Math.random().toString(36).slice(2)
    );
}

function inlineContent(
    value: string,
): ReactNode[] {
    const parts = value.split(
        /(\*\*[^*]+\*\*|`[^`]+`)/g,
    );

    return parts
        .filter(Boolean)
        .map((part, index) => {
            if (
                part.startsWith("**") &&
                part.endsWith("**")
            ) {
                return (
                    <strong key={index}>
                        {part.slice(2, -2)}
                    </strong>
                );
            }

            if (
                part.startsWith("`") &&
                part.endsWith("`")
            ) {
                return (
                    <code key={index}>
                        {part.slice(1, -1)}
                    </code>
                );
            }

            return (
                <Fragment key={index}>
                    {part}
                </Fragment>
            );
        });
}

function RichText({
    content,
}: {
    content: string;
}) {
    const blocks = useMemo(
        () =>
            content
                .replace(/\r\n/g, "\n")
                .split("\n"),
        [content],
    );

    return (
        <div className="delbot-rich-text">
            {blocks.map((line, index) => {
                const trimmed = line.trim();

                if (!trimmed) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-space"
                        />
                    );
                }

                if (/^[-*_]{3,}$/.test(trimmed)) {
                    return <hr key={index} />;
                }

                const heading =
                    trimmed.match(
                        /^(#{1,3})\s+(.+)$/,
                    );

                if (heading) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-heading"
                        >
                            {inlineContent(
                                heading[2],
                            )}
                        </div>
                    );
                }

                const bullet =
                    trimmed.match(
                        /^[-•◆▪]\s+(.+)$/,
                    );

                if (bullet) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-list-row"
                        >
                            <span
                                className="delbot-text-bullet"
                                aria-hidden="true"
                            >
                                •
                            </span>
                            <span>
                                {inlineContent(
                                    bullet[1],
                                )}
                            </span>
                        </div>
                    );
                }

                const numbered =
                    trimmed.match(
                        /^(\d+)[.)]\s+(.+)$/,
                    );

                if (numbered) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-list-row"
                        >
                            <span className="delbot-text-number">
                                {numbered[1]}.
                            </span>
                            <span>
                                {inlineContent(
                                    numbered[2],
                                )}
                            </span>
                        </div>
                    );
                }

                return (
                    <p key={index}>
                        {inlineContent(trimmed)}
                    </p>
                );
            })}
        </div>
    );
}

function citationTitle(
    citation: CitationRecord,
): string {
    return (
        citation.document?.title ||
        citation.document_title ||
        citation.document?.document_id ||
        citation.document_id ||
        "Repository source"
    );
}

function CitationList({
    citations,
}: {
    citations: CitationRecord[];
}) {
    if (citations.length === 0) {
        return null;
    }

    return (
        <details className="delbot-citations">
            <summary>
                {citations.length} repository
                {citations.length === 1
                    ? " source"
                    : " sources"}
            </summary>

            <div className="delbot-citation-list">
                {citations.map(
                    (citation, index) => (
                        <div
                            key={
                                `${citationTitle(
                                    citation,
                                )}-${index}`
                            }
                            className="delbot-citation-card"
                        >
                            <div className="delbot-citation-index">
                                {index + 1}
                            </div>

                            <div className="delbot-citation-copy">
                                <strong>
                                    {citationTitle(
                                        citation,
                                    )}
                                </strong>

                                <span>
                                    {citation.page
                                        ? `Page ${citation.page}`
                                        : "Repository evidence"}
                                </span>

                                {citation.text ? (
                                    <p>
                                        {citation.text
                                            .replace(
                                                /\s+/g,
                                                " ",
                                            )
                                            .trim()
                                            .slice(
                                                0,
                                                220,
                                            )}
                                        {citation.text.length >
                                        220
                                            ? "…"
                                            : ""}
                                    </p>
                                ) : null}
                            </div>

                            {citation.document
                                ?.file_path ? (
                                <ExternalLink
                                    size={14}
                                    aria-hidden="true"
                                />
                            ) : null}
                        </div>
                    ),
                )}
            </div>
        </details>
    );
}

function Bubble({
    message,
}: {
    message: ConversationMessage;
}) {
    const isUser =
        message.role === "user";

    return (
        <article
            className={[
                "delbot-message",
                isUser
                    ? "delbot-message-user"
                    : "delbot-message-assistant",
            ].join(" ")}
        >
            <div
                className={[
                    "delbot-message-avatar",
                    isUser
                        ? "delbot-avatar-user"
                        : "delbot-avatar-assistant",
                ].join(" ")}
                aria-hidden="true"
            >
                {isUser ? (
                    <UserRound size={15} />
                ) : (
                    <Bot size={15} />
                )}
            </div>

            <div className="delbot-message-column">
                <div className="delbot-message-author">
                    {isUser ? "You" : "DELBot"}
                </div>

                <div className="delbot-message-bubble">
                    <RichText
                        content={message.content}
                    />
                </div>

                {!isUser ? (
                    <CitationList
                        citations={
                            message.citations ?? []
                        }
                    />
                ) : null}
            </div>
        </article>
    );
}

export default function ConversationWorkspace() {
    const initialThread = useMemo(
        () => ensureActiveThread(),
        [],
    );

    const [
        thread,
        setThread,
    ] = useState<ConversationThread>(
        initialThread,
    );

    const [
        messages,
        setMessages,
    ] = useState<ConversationMessage[]>(
        initialThread.messages,
    );

    const [
        loading,
        setLoading,
    ] = useState(false);

    const bottomRef =
        useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const handleThreadSelection = (
            event: Event,
        ) => {
            const selectedId =
                (
                    event as CustomEvent<string>
                ).detail;

            const selected =
                loadConversationThreads().find(
                    (candidate) =>
                        candidate.id ===
                        selectedId,
                );

            if (!selected) {
                return;
            }

            setThread(selected);
            setMessages(selected.messages);
            setLoading(false);
        };

        window.addEventListener(
            THREAD_SELECTED_EVENT,
            handleThreadSelection,
        );

        return () => {
            window.removeEventListener(
                THREAD_SELECTED_EVENT,
                handleThreadSelection,
            );
        };
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages, loading]);

    const persistMessages = (
        nextMessages: ConversationMessage[],
        nextSessionId = thread.sessionId,
    ) => {
        const nextThread =
            saveConversationThread({
                ...thread,
                sessionId: nextSessionId,
                title: conversationTitle(
                    nextMessages,
                ),
                messages: nextMessages,
            });

        setThread(nextThread);
        setMessages(nextThread.messages);
    };

    const handleSubmit = async (
        question: string,
    ) => {
        if (loading) {
            return;
        }

        const userMessage:
            ConversationMessage = {
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
            const response =
                await researchAnswer(
                    question,
                    thread.sessionId,
                );

            const payload = response.data;

            const assistantMessage:
                ConversationMessage = {
                    id: messageId("assistant"),
                    role: "assistant",
                    content:
                        String(
                            payload.answer ?? "",
                        ).trim() ||
                        "DELBot tidak menerima jawaban yang dapat ditampilkan.",
                    citations: Array.isArray(
                        payload.citations,
                    )
                        ? (
                              payload.citations as unknown as CitationRecord[]
                          )
                        : [],
                    createdAt: Date.now(),
                };

            persistMessages(
                [
                    ...pendingMessages,
                    assistantMessage,
                ],
                payload.session_id ||
                    thread.sessionId,
            );
        } catch (error) {
            const message =
                error instanceof Error
                    ? error.message
                    : "Unknown request error";

            const errorMessage:
                ConversationMessage = {
                    id: messageId("assistant"),
                    role: "assistant",
                    content:
                        "Permintaan belum berhasil diproses. " +
                        `Silakan coba lagi. (${message})`,
                    citations: [],
                    createdAt: Date.now(),
                };

            persistMessages([
                ...pendingMessages,
                errorMessage,
            ]);
        } finally {
            setLoading(false);
        }
    };

    const empty = messages.length === 0;

    return (
        <section className="delbot-conversation-workspace">
            <div className="delbot-conversation-stage">
                <div
                    className={[
                        "delbot-message-viewport",
                        empty
                            ? "delbot-message-viewport-empty"
                            : "",
                    ]
                        .filter(Boolean)
                        .join(" ")}
                >
                    {empty ? (
                        <div className="delbot-empty-state">
                            <span className="delbot-empty-eyebrow">
                                Research Workspace
                            </span>

                            <h1>
                                Apa yang sedang kamu
                                kerjakan?
                            </h1>

                            <p>
                                Mulai dari pertanyaan,
                                topik, draft ide, atau
                                percakapan biasa.
                            </p>
                        </div>
                    ) : (
                        <div className="delbot-message-list">
                            {messages.map(
                                (message) => (
                                    <Bubble
                                        key={
                                            message.id
                                        }
                                        message={
                                            message
                                        }
                                    />
                                ),
                            )}

                            {loading ? (
                                <div className="delbot-thinking">
                                    <Bot size={15} />
                                    <span>
                                        DELBot is
                                        thinking
                                    </span>
                                    <i />
                                    <i />
                                    <i />
                                </div>
                            ) : null}

                            <div ref={bottomRef} />
                        </div>
                    )}
                </div>

                <ResearchInputDock
                    loading={loading}
                    empty={empty}
                    onSubmit={handleSubmit}
                />
            </div>
        </section>
    );
}
