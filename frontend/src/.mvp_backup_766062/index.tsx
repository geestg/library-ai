import { useState } from "react";
import { researchAnswer } from "../../api/research";

type Citation = {
    document_id: string;
    source: string;
    section: string;
    page_start?: number;
    page_end?: number;
};

type ResearchResponse = {
    answer: string;
    citations: Citation[];
};

export default function ResearchPage() {
    const [question, setQuestion] = useState("");
    const [result, setResult] =
        useState<ResearchResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleResearch() {
        const value = question.trim();

        if (!value || loading) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const response =
                await researchAnswer(value);

            setResult(response.data);
        } catch {
            setResult(null);
            setError(
                "Unable to generate research answer.",
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <main
            style={{
                minHeight: "100vh",
                padding: 40,
                background: "#f7f8fa",
                color: "#1f2937",
                fontFamily:
                    "Inter, system-ui, sans-serif",
            }}
        >
            <section
                style={{
                    maxWidth: 960,
                    margin: "0 auto",
                }}
            >
                <div style={{ marginBottom: 28 }}>
                    <div
                        style={{
                            fontSize: 13,
                            color: "#64748b",
                            marginBottom: 8,
                        }}
                    >
                        DELBot / Research
                    </div>

                    <h1
                        style={{
                            margin: 0,
                            fontSize: 30,
                        }}
                    >
                        Research Assistant
                    </h1>

                    <p
                        style={{
                            color: "#64748b",
                            lineHeight: 1.6,
                        }}
                    >
                        Ask academic questions and receive
                        answers grounded in indexed documents.
                    </p>
                </div>

                <section
                    style={{
                        background: "#ffffff",
                        border: "1px solid #e5e7eb",
                        borderRadius: 14,
                        padding: 24,
                    }}
                >
                    <textarea
                        value={question}
                        onChange={(event) =>
                            setQuestion(event.target.value)
                        }
                        placeholder="Ask an academic research question..."
                        rows={5}
                        style={{
                            width: "100%",
                            boxSizing: "border-box",
                            padding: 14,
                            border: "1px solid #dbe1e8",
                            borderRadius: 10,
                            resize: "vertical",
                            fontFamily: "inherit",
                            fontSize: 15,
                        }}
                    />

                    <button
                        onClick={handleResearch}
                        disabled={loading}
                        style={{
                            marginTop: 12,
                            padding: "10px 18px",
                            border: 0,
                            borderRadius: 9,
                            background: "#1f2937",
                            color: "#ffffff",
                            cursor: loading
                                ? "default"
                                : "pointer",
                        }}
                    >
                        {loading
                            ? "Researching..."
                            : "Ask Research"}
                    </button>

                    {error && (
                        <p style={{ color: "#b91c1c" }}>
                            {error}
                        </p>
                    )}
                </section>

                {result && (
                    <section
                        style={{
                            marginTop: 20,
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: 14,
                            padding: 24,
                        }}
                    >
                        <h2>Answer</h2>

                        <p
                            style={{
                                whiteSpace: "pre-wrap",
                                lineHeight: 1.7,
                            }}
                        >
                            {result.answer}
                        </p>

                        {result.citations.length > 0 && (
                            <>
                                <h3>Citations</h3>

                                <div>
                                    {result.citations.map(
                                        (citation, index) => (
                                            <div
                                                key={`${citation.document_id}-${index}`}
                                                style={{
                                                    padding:
                                                        "10px 0",
                                                    borderTop:
                                                        "1px solid #eef0f2",
                                                }}
                                            >
                                                <strong>
                                                    {citation.source}
                                                </strong>

                                                <div
                                                    style={{
                                                        color:
                                                            "#64748b",
                                                        fontSize: 14,
                                                    }}
                                                >
                                                    {citation.section}
                                                    {citation.page_start
                                                        ? ` · Page ${citation.page_start}`
                                                        : ""}
                                                </div>
                                            </div>
                                        ),
                                    )}
                                </div>
                            </>
                        )}
                    </section>
                )}
            </section>
        </main>
    );
}
