import { useState } from "react";
import { colors, typography } from "../../design";
import { Button, Input, Card } from "../../components/ui";
import { researchAnswer } from "../../api/research";

const containerStyle: React.CSSProperties = {
    padding: 24,
    borderTop: `1px solid ${colors.border}`,
    background: colors.surface,
};

const wrapperStyle: React.CSSProperties = {
    maxWidth: 920,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 14,
};

const rowStyle: React.CSSProperties = {
    display: "flex",
    gap: 12,
    alignItems: "center",
};

export default function ResearchInputDock() {

    const [question, setQuestion] = useState("");
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

            const response = await researchAnswer(value);

            setAnswer(response.data?.answer ?? "");
            setCitations(response.data?.citations ?? []);

        } catch (error) {

            setAnswer("");
            setCitations([]);
            setError(
                error instanceof Error
                    ? error.message
                    : "Failed to get research answer."
            );

        } finally {

            setLoading(false);

        }

    }

    return (

        <div>

            {answer && (

                <Card
                    style={{
                        marginBottom: 16,
                    }}
                >

                    <div
                        style={{
                            ...typography.h4,
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
                            lineHeight: 1.7,
                        }}
                    >
                        {answer}
                    </div>

                    {citations.length > 0 && (

                        <div
                            style={{
                                marginTop: 16,
                                paddingTop: 12,
                                borderTop: `1px solid ${colors.border}`,
                            }}
                        >

                            <div
                                style={{
                                    ...typography.caption,
                                    color: colors.textSecondary,
                                    marginBottom: 8,
                                }}
                            >
                                Sources: {citations.length}
                            </div>

                            {citations.map((citation, index) => (

                                <div
                                    key={`${citation.document_id ?? "document"}-${index}`}
                                    style={{
                                        ...typography.caption,
                                        color: colors.textSecondary,
                                        marginBottom: 4,
                                    }}
                                >
                                    {index + 1}.{" "}
                                    {citation.section || "Document"}
                                    {citation.page_start
                                        ? ` · Page ${citation.page_start}`
                                        : ""}
                                </div>

                            ))}

                        </div>

                    )}

                </Card>

            )}

            {error && (

                <Card
                    style={{
                        marginBottom: 16,
                    }}
                >

                    <div
                        style={{
                            ...typography.caption,
                            color: colors.textSecondary,
                        }}
                    >
                        Research request failed: {error}
                    </div>

                </Card>

            )}

            <footer style={containerStyle}>

                <div style={wrapperStyle}>

                    <Input
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
                        placeholder="Ask a research question, compare papers, summarize literature..."
                        disabled={loading}
                    />

                    <div
                        style={{
                            ...rowStyle,
                            justifyContent: "space-between",
                        }}
                    >

                        <div
                            style={{
                                ...typography.caption,
                                color: colors.textSecondary,
                            }}
                        >
                            Answers are generated from indexed repository documents with citations.
                        </div>

                        <Button
                            onClick={handleSubmit}
                            disabled={
                                loading ||
                                question.trim().length === 0
                            }
                        >
                            {loading ? "Searching..." : "Ask DELBot"}
                        </Button>

                    </div>

                </div>

            </footer>

        </div>

    );

}
