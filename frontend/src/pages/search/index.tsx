import WorkspaceShell from "../../components/layout/WorkspaceShell";
import { useState } from "react";
import { retrievalSearch } from "../../api/retrieval";

type SearchDocument = {
    id: string;
    score?: number;
    content?: string;
    source?: string;
    section?: string;
    page_start?: number;
    page_end?: number;
};

type SearchResponse = {
    documents?: SearchDocument[];
};

export default function SearchPage() {
    const [query, setQuery] = useState("");
    const [documents, setDocuments] = useState<SearchDocument[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSearch() {
        const value = query.trim();

        if (!value || loading) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const response = await retrievalSearch(
                value,
                5,
            );

            setDocuments(
                response.data.documents ?? [],
            );
        } catch {
            setDocuments([]);
            setError(
                "Unable to search repository.",
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <WorkspaceShell>
        <main
            style={{
                padding: 32,
                maxWidth: 1000,
                margin: "0 auto",
                fontFamily: "Inter, system-ui, sans-serif",
            }}
        >
            <h1 style={{ marginBottom: 8 }}>
                Semantic Search
            </h1>

            <p style={{ color: "#64748b", marginBottom: 24 }}>
                Search indexed academic documents using natural language.
            </p>

            <div
                style={{
                    display: "flex",
                    gap: 8,
                    marginBottom: 24,
                }}
            >
                <input
                    value={query}
                    onChange={(event) =>
                        setQuery(event.target.value)
                    }
                    onKeyDown={(event) => {
                        if (event.key === "Enter") {
                            handleSearch();
                        }
                    }}
                    placeholder="Search the research repository..."
                    style={{
                        flex: 1,
                        padding: "12px 14px",
                        border:
                            "1px solid #cbd5e1",
                        borderRadius: 10,
                        fontSize: 15,
                    }}
                />

                <button
                    onClick={handleSearch}
                    disabled={loading}
                    style={{
                        padding: "12px 18px",
                        border: 0,
                        borderRadius: 10,
                        cursor: loading
                            ? "default"
                            : "pointer",
                    }}
                >
                    {loading
                        ? "Searching..."
                        : "Search"}
                </button>
            </div>

            {error && (
                <p style={{ color: "#b91c1c" }}>
                    {error}
                </p>
            )}

            {documents.length > 0 && (
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 12,
                    }}
                >
                    {documents.map((document, index) => (
                        <article
                            key={`${document.id}-${index}`}
                            style={{
                                padding: 18,
                                border:
                                    "1px solid #e2e8f0",
                                borderRadius: 12,
                            }}
                        >
                            <div
                                style={{
                                    fontWeight: 600,
                                    marginBottom: 8,
                                }}
                            >
                                {document.source ||
                                    document.id}
                            </div>

                            <div
                                style={{
                                    fontSize: 13,
                                    color: "#64748b",
                                    marginBottom: 10,
                                }}
                            >
                                {document.section ||
                                    "Research document"}
                                {" · "}
                                {document.page_start
                                    ? `Page ${document.page_start}`
                                    : "Page unavailable"}
                                {document.score !== undefined
                                    ? ` · Score ${document.score.toFixed(3)}`
                                    : ""}
                            </div>

                            <p
                                style={{
                                    margin: 0,
                                    lineHeight: 1.6,
                                }}
                            >
                                {document.content ||
                                    "No content available."}
                            </p>
                        </article>
                    ))}
                </div>
            )}

            {!loading &&
                !error &&
                query &&
                documents.length === 0 && (
                    <p style={{ color: "#64748b" }}>
                        No matching documents found.
                    </p>
                )}
        </main>
        </WorkspaceShell>
    );
}
