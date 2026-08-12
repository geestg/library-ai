import { useState } from "react";
import { colors, typography, radius, spacing } from "../../design";
import { Button } from "../../components/ui";
import { researchAnswer } from "../../api/research";

const dockStyle: React.CSSProperties = {
    borderTop: `1px solid ${colors.border}`,
    background: colors.surface,
    padding: "18px 32px 22px",
};

const innerStyle: React.CSSProperties = {
    maxWidth: 980,
    margin: "0 auto",
};

const inputStyle: React.CSSProperties = {
    width: "100%",
    minHeight: 52,
    padding: "14px 16px",
    border: `1px solid ${colors.border}`,
    borderRadius: radius.md,
    background: colors.surface,
    color: colors.text,
    outline: "none",
    resize: "vertical",
    fontFamily: "inherit",
    fontSize: 14,
    lineHeight: 1.5,
};

const footerStyle: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.lg,
    marginTop: 10,
};

const helperStyle: React.CSSProperties = {
    ...typography.caption,
    color: colors.textMuted,
};

const answerStyle: React.CSSProperties = {
    marginBottom: 16,
    padding: "20px 22px",
    border: `1px solid ${colors.border}`,
    borderRadius: radius.lg,
    background: colors.surface,
};

export default function ResearchInputDock() {
    const [question, setQuestion] = useState("");

    const [sessionId] = useState(() => {
        const existing = localStorage.getItem(
            "delbot_research_session_id",
        );

        if (existing) {
            return existing;
        }

        const created =
            typeof crypto !== "undefined" &&
            typeof crypto.randomUUID === "function"
                ? crypto.randomUUID()
                : `session-${Date.now()}`;

        localStorage.setItem(
            "delbot_research_session_id",
            created,
        );

        return created;
    });
    const [answer, setAnswer] = useState("");
    const [citations, setCitations] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit() {
        const value = question.trim();

        if (!value || loading) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const response = await researchAnswer(value, sessionId);

            setAnswer(response.data?.answer ?? "");
            setCitations(response.data?.citations ?? []);

            if (response.data?.session_id) {
                localStorage.setItem(
                    "delbot_research_session_id",
                    response.data.session_id,
                );
            }

            if (response.data?.session_id) {
                localStorage.setItem(
                    "delbot_research_session_id",
                    response.data.session_id,
                );
            }
        } catch (error) {
            setAnswer("");
            setCitations([]);

            setError(
                error instanceof Error
                    ? error.message
                    : "Unable to generate research answer."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div style={dockStyle}>
            <div style={innerStyle}>
                {answer && (
                    <section style={answerStyle}>
                        <div
                            style={{
                                ...typography.h4,
                                color: colors.text,
                                marginBottom: 10,
                            }}
                        >
                            DELBot Answer
                        </div>

                        <div
                            style={{
                                ...typography.body,
                                color: colors.text,
                                whiteSpace: "pre-wrap",
                                lineHeight: 1.75,
                            }}
                        >
                            {answer}
                        </div>

                        {citations.length > 0 && (
                            <div
                                style={{
                                    marginTop: 18,
                                    paddingTop: 14,
                                    borderTop:
                                        `1px solid ${colors.border}`,
                                }}
                            >
                                <div
                                    style={{
                                        ...typography.label,
                                        color: colors.text,
                                        marginBottom: 8,
                                    }}
                                >
                                    Sources
                                </div>

                                {citations.map(
                                    (citation, index) => (
                                        <div
                                            key={
                                                `${citation.document_id ?? "document"}-${index}`
                                            }
                                            style={{
                                                ...typography.caption,
                                                color:
                                                    colors.textSecondary,
                                                marginBottom: 5,
                                            }}
                                        >
                                            {index + 1}.{" "}
                                            {citation.section ||
                                                "Document"}
                                            {citation.page_start
                                                ? ` · Page ${citation.page_start}`
                                                : ""}
                                        </div>
                                    )
                                )}
                            </div>
                        )}
                    </section>
                )}

                {error && (
                    <div
                        style={{
                            ...typography.caption,
                            color: colors.danger,
                            marginBottom: 12,
                        }}
                    >
                        Research request failed: {error}
                    </div>
                )}

                <div
                    style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: 8,
                        marginBottom: 10,
                    }}
                >
                    {[
                        "Literature Review",
                        "Compare Papers",
                        "Research Gap",
                        "Thesis Ideas",
                    ].map((action) => (
                        <button
                            key={action}
                            type="button"
                            onClick={() => {
                                const prompts: Record<string, string> = {
                                    "Literature Review":
                                        "Summarize the key findings, themes, and methods across the indexed literature.",
                                    "Compare Papers":
                                        "Compare the most relevant indexed papers by methods, findings, limitations, and conclusions.",
                                    "Research Gap":
                                        "Identify research gaps supported by the indexed literature and explain the evidence.",
                                    "Thesis Ideas":
                                        "Suggest thesis ideas based on the indexed literature and explain the research motivation.",
                                };

                                setQuestion(prompts[action]);
                            }}
                            style={{
                                height: 32,
                                padding: "0 10px",
                                borderRadius: 8,
                                border: "1px solid #e5e7eb",
                                background: "#ffffff",
                                color: "#475569",
                                cursor: "pointer",
                                fontSize: 12,
                                fontWeight: 600,
                            }}
                        >
                            {action}
                        </button>
                    ))}
                </div>

                <textarea
                    value={question}
                    onChange={(event) =>
                        setQuestion(event.target.value)
                    }
                    onKeyDown={(event) => {
                        if (
                            event.key === "Enter" &&
                            !event.shiftKey
                        ) {
                            event.preventDefault();
                            handleSubmit();
                        }
                    }}
                    placeholder="Ask a research question..."
                    disabled={loading}
                    style={inputStyle}
                    aria-label="Research question"
                />

                <div style={footerStyle}>
                    <div style={helperStyle}>
                        Enter to ask · Shift+Enter for a new line
                    </div>

                    <Button
                        onClick={handleSubmit}
                        disabled={
                            loading ||
                            question.trim().length === 0
                        }
                    >
                        {loading
                            ? "Researching..."
                            : "Ask DELBot"}
                    </Button>
                </div>
            </div>
        </div>
    );
}
