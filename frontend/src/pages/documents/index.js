import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import { indexRepository } from "../../api/document";
export default function DocumentsPage() {
    const [limit, setLimit] = useState("25");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
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
        }
        catch (requestError) {
            setResult(null);
            setError(requestError instanceof Error
                ? requestError.message
                : "Document indexing failed.");
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx(WorkspaceShell, { children: _jsx("main", { style: {
                minHeight: "100vh",
                padding: "40px",
                background: "#f7f8fa",
                color: "#1f2937",
                boxSizing: "border-box",
            }, children: _jsxs("section", { style: {
                    maxWidth: "960px",
                    margin: "0 auto",
                }, children: [_jsxs("div", { style: {
                            marginBottom: "28px",
                        }, children: [_jsx("div", { style: {
                                    fontSize: "13px",
                                    color: "#6b7280",
                                    marginBottom: "8px",
                                }, children: "DELBot / Documents" }), _jsx("h1", { style: {
                                    margin: 0,
                                    fontSize: "30px",
                                    fontWeight: 650,
                                }, children: "Document Index" }), _jsx("p", { style: {
                                    marginTop: "10px",
                                    color: "#6b7280",
                                    lineHeight: 1.6,
                                }, children: "Index PDF documents from the repository into the research knowledge base." })] }), _jsxs("section", { style: {
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: "14px",
                            padding: "24px",
                            marginBottom: "20px",
                        }, children: [_jsx("h2", { style: {
                                    margin: "0 0 8px",
                                    fontSize: "18px",
                                }, children: "Batch Indexing" }), _jsx("p", { style: {
                                    margin: "0 0 20px",
                                    color: "#6b7280",
                                    fontSize: "14px",
                                    lineHeight: 1.5,
                                }, children: "Process a limited number of repository PDFs." }), _jsxs("div", { style: {
                                    display: "flex",
                                    gap: "12px",
                                    alignItems: "center",
                                    flexWrap: "wrap",
                                }, children: [_jsx("input", { value: limit, onChange: (event) => setLimit(event.target.value), type: "number", min: "1", style: {
                                            width: "120px",
                                            padding: "10px 12px",
                                            border: "1px solid #d1d5db",
                                            borderRadius: "8px",
                                            fontSize: "14px",
                                            boxSizing: "border-box",
                                        } }), _jsx("button", { type: "button", onClick: handleIndex, disabled: loading, style: {
                                            padding: "10px 16px",
                                            border: "0",
                                            borderRadius: "8px",
                                            background: "#111827",
                                            color: "#ffffff",
                                            cursor: loading
                                                ? "wait"
                                                : "pointer",
                                            fontSize: "14px",
                                        }, children: loading
                                            ? "Indexing..."
                                            : "Index Documents" })] })] }), error && (_jsx("section", { style: {
                            background: "#fff7f7",
                            border: "1px solid #fecaca",
                            borderRadius: "12px",
                            padding: "18px",
                            color: "#991b1b",
                            marginBottom: "20px",
                        }, children: error })), result && (_jsxs("section", { style: {
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: "14px",
                            padding: "24px",
                        }, children: [_jsx("h2", { style: {
                                    margin: "0 0 18px",
                                    fontSize: "18px",
                                }, children: "Index Result" }), _jsxs("div", { style: {
                                    display: "grid",
                                    gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                                    gap: "12px",
                                }, children: [_jsx(Metric, { label: "Total PDF", value: result.total_pdf ?? 0 }), _jsx(Metric, { label: "Indexed", value: result.indexed ?? 0 }), _jsx(Metric, { label: "Skipped", value: result.skipped ?? 0 })] })] }))] }) }) }));
}
function Metric({ label, value, }) {
    return (_jsxs("div", { style: {
            padding: "16px",
            borderRadius: "10px",
            background: "#f9fafb",
            border: "1px solid #eef0f2",
        }, children: [_jsx("div", { style: {
                    fontSize: "12px",
                    color: "#6b7280",
                    marginBottom: "6px",
                }, children: label }), _jsx("div", { style: {
                    fontSize: "24px",
                    fontWeight: 650,
                }, children: value })] }));
}
