import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Search, Loader2, FileText, } from "lucide-react";
import { researchAnswer } from "../../api/research";
export default function SearchPage() {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState(null);
    async function search() {
        if (!query.trim()) {
            setError("Query is required.");
            return;
        }
        setLoading(true);
        setError("");
        setResult(null);
        try {
            const response = await researchAnswer(query);
            setResult(response.data);
        }
        catch {
            setError("Search failed.");
        }
        finally {
            setLoading(false);
        }
    }
    const card = {
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };
    return (_jsxs("div", { children: [_jsxs("div", { style: {
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    marginBottom: 24,
                }, children: [_jsx(Search, { size: 30 }), _jsxs("div", { children: [_jsx("h1", { style: { margin: 0 }, children: "Semantic Search" }), _jsx("p", { style: {
                                    marginTop: 6,
                                    color: "#6b7280",
                                }, children: "Search repository using existing research pipeline." })] })] }), _jsxs("div", { style: card, children: [_jsx("textarea", { rows: 4, value: query, onChange: (e) => setQuery(e.target.value), placeholder: "Search repository...", style: {
                            width: "100%",
                            padding: 12,
                            boxSizing: "border-box",
                            resize: "vertical",
                        } }), _jsxs("button", { onClick: search, disabled: loading, style: {
                            marginTop: 16,
                            padding: "10px 18px",
                            cursor: "pointer",
                            display: "flex",
                            alignItems: "center",
                            gap: 8,
                        }, children: [loading && _jsx(Loader2, { size: 16 }), loading ? "Searching..." : "Search"] }), error && (_jsx("div", { style: {
                            marginTop: 16,
                            color: "#dc2626",
                        }, children: error }))] }), result && (_jsxs("div", { style: {
                    ...card,
                    marginTop: 24,
                }, children: [_jsx("h2", { style: { marginTop: 0 }, children: "Answer" }), _jsx("div", { style: {
                            whiteSpace: "pre-wrap",
                        }, children: result.answer }), _jsx("h2", { style: {
                            marginTop: 28,
                        }, children: "Citations" }), result.citations.map((c, index) => (_jsxs("div", { style: {
                            borderTop: index === 0
                                ? "none"
                                : "1px solid #eee",
                            padding: "12px 0",
                            display: "flex",
                            gap: 10,
                        }, children: [_jsx(FileText, { size: 18, style: { marginTop: 2 } }), _jsxs("div", { children: [_jsx("strong", { children: c.document_id }), _jsx("div", { children: c.section }), _jsxs("div", { style: {
                                            color: "#6b7280",
                                            fontSize: 13,
                                        }, children: ["Page ", c.page_start ?? "-", c.page_end
                                                ? ` - ${c.page_end}`
                                                : ""] })] })] }, index)))] }))] }));
}
