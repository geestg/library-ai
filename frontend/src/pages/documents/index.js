import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Database, Play, Loader2, CheckCircle2, FileText, SkipForward, } from "lucide-react";
import { indexRepository } from "../../api/document";
export default function DocumentsPage() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState(null);
    async function runIndex() {
        setLoading(true);
        setError("");
        setResult(null);
        try {
            const response = await indexRepository();
            setResult(response.data);
        }
        catch (err) {
            setError(err?.message ?? "Index failed.");
        }
        finally {
            setLoading(false);
        }
    }
    const card = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };
    const stat = {
        ...card,
        flex: 1,
        minWidth: 180,
    };
    return (_jsxs("div", { children: [_jsxs("div", { style: {
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    marginBottom: 24,
                }, children: [_jsx(Database, { size: 30 }), _jsxs("div", { children: [_jsx("h1", { style: {
                                    margin: 0,
                                    fontSize: 30,
                                }, children: "Document Index" }), _jsx("p", { style: {
                                    marginTop: 6,
                                    color: "#6b7280",
                                }, children: "Build Knowledge Base from repository PDFs." })] })] }), _jsxs("div", { style: card, children: [_jsxs("button", { onClick: runIndex, disabled: loading, style: {
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                            padding: "12px 20px",
                            border: "none",
                            borderRadius: 10,
                            background: "#2563eb",
                            color: "#fff",
                            fontWeight: 600,
                            cursor: loading ? "default" : "pointer",
                        }, children: [loading
                                ? _jsx(Loader2, { size: 18 })
                                : _jsx(Play, { size: 18 }), loading
                                ? "Indexing..."
                                : "Start Index"] }), error && (_jsx("div", { style: {
                            marginTop: 18,
                            color: "#dc2626",
                        }, children: error }))] }), result && (_jsxs("div", { style: {
                    display: "flex",
                    gap: 18,
                    flexWrap: "wrap",
                    marginTop: 24,
                }, children: [_jsxs("div", { style: stat, children: [_jsx(CheckCircle2, { size: 22 }), _jsx("h2", { children: String(result.success) }), _jsx("div", { children: "Status" })] }), _jsxs("div", { style: stat, children: [_jsx(FileText, { size: 22 }), _jsx("h2", { children: result.indexed }), _jsx("div", { children: "Indexed" })] }), _jsxs("div", { style: stat, children: [_jsx(SkipForward, { size: 22 }), _jsx("h2", { children: result.skipped }), _jsx("div", { children: "Skipped" })] }), _jsxs("div", { style: stat, children: [_jsx(Database, { size: 22 }), _jsx("h2", { children: result.total_pdf }), _jsx("div", { children: "Total PDF" })] })] }))] }));
}
