import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import { useState } from "react";
import { retrievalSearch } from "../../api/retrieval";
export default function SearchPage() {
    const [query, setQuery] = useState("");
    const [documents, setDocuments] = useState([]);
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
            const response = await retrievalSearch(value, 5);
            setDocuments(response.data.documents ?? []);
        }
        catch {
            setDocuments([]);
            setError("Unable to search repository.");
        }
        finally {
            setLoading(false);
        }
    }
    return (_jsx(WorkspaceShell, { children: _jsxs("main", { style: {
                padding: 32,
                maxWidth: 1000,
                margin: "0 auto",
                fontFamily: "Inter, system-ui, sans-serif",
            }, children: [_jsx("h1", { style: { marginBottom: 8 }, children: "Semantic Search" }), _jsx("p", { style: { color: "#64748b", marginBottom: 24 }, children: "Search indexed academic documents using natural language." }), _jsxs("div", { style: {
                        display: "flex",
                        gap: 8,
                        marginBottom: 24,
                    }, children: [_jsx("input", { value: query, onChange: (event) => setQuery(event.target.value), onKeyDown: (event) => {
                                if (event.key === "Enter") {
                                    handleSearch();
                                }
                            }, placeholder: "Search the research repository...", style: {
                                flex: 1,
                                padding: "12px 14px",
                                border: "1px solid #cbd5e1",
                                borderRadius: 10,
                                fontSize: 15,
                            } }), _jsx("button", { onClick: handleSearch, disabled: loading, style: {
                                padding: "12px 18px",
                                border: 0,
                                borderRadius: 10,
                                cursor: loading
                                    ? "default"
                                    : "pointer",
                            }, children: loading
                                ? "Searching..."
                                : "Search" })] }), error && (_jsx("p", { style: { color: "#b91c1c" }, children: error })), documents.length > 0 && (_jsx("div", { style: {
                        display: "flex",
                        flexDirection: "column",
                        gap: 12,
                    }, children: documents.map((document, index) => (_jsxs("article", { style: {
                            padding: 18,
                            border: "1px solid #e2e8f0",
                            borderRadius: 12,
                        }, children: [_jsx("div", { style: {
                                    fontWeight: 600,
                                    marginBottom: 8,
                                }, children: document.source ||
                                    document.id }), _jsxs("div", { style: {
                                    fontSize: 13,
                                    color: "#64748b",
                                    marginBottom: 10,
                                }, children: [document.section ||
                                        "Research document", " · ", document.page_start
                                        ? `Page ${document.page_start}`
                                        : "Page unavailable", document.score !== undefined
                                        ? ` · Score ${document.score.toFixed(3)}`
                                        : ""] }), _jsx("p", { style: {
                                    margin: 0,
                                    lineHeight: 1.6,
                                }, children: document.content ||
                                    "No content available." })] }, `${document.id}-${index}`))) })), !loading &&
                    !error &&
                    query &&
                    documents.length === 0 && (_jsx("p", { style: { color: "#64748b" }, children: "No matching documents found." }))] }) }));
}
