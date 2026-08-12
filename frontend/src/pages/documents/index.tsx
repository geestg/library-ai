import { useState } from "react";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import { indexRepository } from "../../api/document";

type IndexResult = {
    success?: boolean;
    indexed?: number;
    skipped?: number;
    total_pdf?: number;
};

export default function DocumentsPage() {
    const [limit, setLimit] = useState("25");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<IndexResult | null>(null);
    const [error, setError] = useState("");

    const handleIndex = async () => {
        if (loading) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const value = Number(limit) || 25;
            const response = await indexRepository(value);

            setResult(response.data ?? null);
        } catch (requestError) {
            setResult(null);
            setError(
                requestError instanceof Error
                    ? requestError.message
                    : "Document indexing failed."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <WorkspaceShell>
        <main
            style={{
                minHeight: "100vh",
                padding: "40px",
                background: "#f7f8fa",
                color: "#1f2937",
                boxSizing: "border-box",
            }}
        >
            <section
                style={{
                    maxWidth: "960px",
                    margin: "0 auto",
                }}
            >
                <div
                    style={{
                        marginBottom: "28px",
                    }}
                >
                    <div
                        style={{
                            fontSize: "13px",
                            color: "#6b7280",
                            marginBottom: "8px",
                        }}
                    >
                        DELBot / Documents
                    </div>

                    <h1
                        style={{
                            margin: 0,
                            fontSize: "30px",
                            fontWeight: 650,
                        }}
                    >
                        Document Index
                    </h1>

                    <p
                        style={{
                            marginTop: "10px",
                            color: "#6b7280",
                            lineHeight: 1.6,
                        }}
                    >
                        Index PDF documents from the repository into the
                        research knowledge base.
                    </p>
                </div>

                <section
                    style={{
                        background: "#ffffff",
                        border: "1px solid #e5e7eb",
                        borderRadius: "14px",
                        padding: "24px",
                        marginBottom: "20px",
                    }}
                >
                    <h2
                        style={{
                            margin: "0 0 8px",
                            fontSize: "18px",
                        }}
                    >
                        Batch Indexing
                    </h2>

                    <p
                        style={{
                            margin: "0 0 20px",
                            color: "#6b7280",
                            fontSize: "14px",
                            lineHeight: 1.5,
                        }}
                    >
                        Process a limited number of repository PDFs.
                    </p>

                    <div
                        style={{
                            display: "flex",
                            gap: "12px",
                            alignItems: "center",
                            flexWrap: "wrap",
                        }}
                    >
                        <input
                            value={limit}
                            onChange={(event) =>
                                setLimit(event.target.value)
                            }
                            type="number"
                            min="1"
                            style={{
                                width: "120px",
                                padding: "10px 12px",
                                border: "1px solid #d1d5db",
                                borderRadius: "8px",
                                fontSize: "14px",
                                boxSizing: "border-box",
                            }}
                        />

                        <button
                            type="button"
                            onClick={handleIndex}
                            disabled={loading}
                            style={{
                                padding: "10px 16px",
                                border: "0",
                                borderRadius: "8px",
                                background: "#111827",
                                color: "#ffffff",
                                cursor: loading
                                    ? "wait"
                                    : "pointer",
                                fontSize: "14px",
                            }}
                        >
                            {loading
                                ? "Indexing..."
                                : "Index Documents"}
                        </button>
                    </div>
                </section>

                {error && (
                    <section
                        style={{
                            background: "#fff7f7",
                            border: "1px solid #fecaca",
                            borderRadius: "12px",
                            padding: "18px",
                            color: "#991b1b",
                            marginBottom: "20px",
                        }}
                    >
                        {error}
                    </section>
                )}

                {result && (
                    <section
                        style={{
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: "14px",
                            padding: "24px",
                        }}
                    >
                        <h2
                            style={{
                                margin: "0 0 18px",
                                fontSize: "18px",
                            }}
                        >
                            Index Result
                        </h2>

                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns:
                                    "repeat(auto-fit, minmax(160px, 1fr))",
                                gap: "12px",
                            }}
                        >
                            <Metric
                                label="Total PDF"
                                value={result.total_pdf ?? 0}
                            />

                            <Metric
                                label="Indexed"
                                value={result.indexed ?? 0}
                            />

                            <Metric
                                label="Skipped"
                                value={result.skipped ?? 0}
                            />
                        </div>
                    </section>
                )}
            </section>
        </main>
        </WorkspaceShell>
    );
}

function Metric({
    label,
    value,
}: {
    label: string;
    value: number;
}) {
    return (
        <div
            style={{
                padding: "16px",
                borderRadius: "10px",
                background: "#f9fafb",
                border: "1px solid #eef0f2",
            }}
        >
            <div
                style={{
                    fontSize: "12px",
                    color: "#6b7280",
                    marginBottom: "6px",
                }}
            >
                {label}
            </div>

            <div
                style={{
                    fontSize: "24px",
                    fontWeight: 650,
                }}
            >
                {value}
            </div>
        </div>
    );
}
