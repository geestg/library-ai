import { useState } from "react";
import { researchAnswer } from "../../api/research";

export default function ThesisIdeasPage() {
    const [topic, setTopic] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function generateIdeas() {
        const value = topic.trim();

        if (!value || loading) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const response = await researchAnswer(
                `Based on the indexed academic literature about ${value}, recommend practical thesis ideas. For each idea provide a clear title, research problem, motivation, and brief justification based on the literature.`,
            );

            setAnswer(response.data.answer);
        } catch {
            setAnswer("");
            setError(
                "Unable to generate thesis ideas.",
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
                        DELBot / Thesis Ideas
                    </div>

                    <h1
                        style={{
                            margin: 0,
                            fontSize: 30,
                        }}
                    >
                        Thesis Ideas
                    </h1>

                    <p
                        style={{
                            color: "#64748b",
                            lineHeight: 1.6,
                        }}
                    >
                        Generate thesis directions grounded in
                        the indexed literature.
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
                    <input
                        value={topic}
                        onChange={(event) =>
                            setTopic(event.target.value)
                        }
                        placeholder="Research topic..."
                        style={{
                            width: "100%",
                            boxSizing: "border-box",
                            padding: 13,
                            border:
                                "1px solid #dbe1e8",
                            borderRadius: 9,
                            fontSize: 15,
                        }}
                    />

                    <button
                        onClick={generateIdeas}
                        disabled={loading}
                        style={{
                            marginTop: 12,
                            padding: "10px 18px",
                            border: 0,
                            borderRadius: 9,
                            background: "#1f2937",
                            color: "#ffffff",
                        }}
                    >
                        {loading
                            ? "Generating..."
                            : "Generate Ideas"}
                    </button>

                    {error && (
                        <p style={{ color: "#b91c1c" }}>
                            {error}
                        </p>
                    )}
                </section>

                {answer && (
                    <section
                        style={{
                            marginTop: 20,
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: 14,
                            padding: 24,
                        }}
                    >
                        <h2>Recommended Thesis Directions</h2>

                        <p
                            style={{
                                whiteSpace: "pre-wrap",
                                lineHeight: 1.7,
                            }}
                        >
                            {answer}
                        </p>
                    </section>
                )}
            </section>
        </main>
    );
}
