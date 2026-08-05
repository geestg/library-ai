import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { Search, FolderOpen, FileText, CheckCircle2, AlertCircle, } from "lucide-react";
import { repositoryExplorer } from "../../api/repository";
export default function RepositoryPage() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [keyword, setKeyword] = useState("");
    const [repo, setRepo] = useState({
        total: 0,
        pdf_available: 0,
        pdf_missing: 0,
        items: [],
    });
    useEffect(() => {
        repositoryExplorer()
            .then((res) => {
            setRepo({
                total: res.data.total ?? 0,
                pdf_available: res.data.pdf_available ?? 0,
                pdf_missing: res.data.pdf_missing ?? 0,
                items: res.data.items ?? [],
            });
        })
            .catch((err) => {
            setError(err?.message ?? "Failed to load repository.");
        })
            .finally(() => {
            setLoading(false);
        });
    }, []);
    const filtered = useMemo(() => {
        const q = keyword.trim().toLowerCase();
        if (!q) {
            return repo.items;
        }
        return repo.items.filter((item) => {
            const title = item.title ??
                item.filename ??
                item.document_name ??
                item.document_id ??
                "";
            return title.toLowerCase().includes(q);
        });
    }, [repo.items, keyword]);
    const statCard = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 20,
        flex: 1,
        minWidth: 180,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };
    const tableHeader = {
        padding: 14,
        textAlign: "left",
        background: "#f8fafc",
        borderBottom: "1px solid #e5e7eb",
        fontWeight: 600,
    };
    const tableCell = {
        padding: 14,
        borderBottom: "1px solid #f1f5f9",
    };
    if (loading) {
        return _jsx("h3", { children: "Loading repository..." });
    }
    if (error) {
        return _jsx("h3", { children: error });
    }
    return (_jsxs("div", { children: [_jsxs("div", { style: {
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 28,
                    flexWrap: "wrap",
                    gap: 16,
                }, children: [_jsxs("div", { children: [_jsx("h1", { style: { margin: 0 }, children: "Repository Explorer" }), _jsx("p", { style: {
                                    marginTop: 8,
                                    color: "#6b7280",
                                }, children: "Browse repository documents." })] }), _jsxs("div", { style: {
                            display: "flex",
                            alignItems: "center",
                            gap: 8,
                            background: "#eff6ff",
                            color: "#1d4ed8",
                            padding: "10px 16px",
                            borderRadius: 999,
                            fontWeight: 600,
                        }, children: [_jsx(FolderOpen, { size: 18 }), repo.total, " Documents"] })] }), _jsxs("div", { style: {
                    display: "flex",
                    gap: 18,
                    flexWrap: "wrap",
                    marginBottom: 28,
                }, children: [_jsxs("div", { style: statCard, children: [_jsx("div", { children: "Total Repository" }), _jsx("h2", { children: repo.total })] }), _jsxs("div", { style: statCard, children: [_jsx("div", { children: "PDF Available" }), _jsx("h2", { children: repo.pdf_available })] }), _jsxs("div", { style: statCard, children: [_jsx("div", { children: "PDF Missing" }), _jsx("h2", { children: repo.pdf_missing })] }), _jsxs("div", { style: statCard, children: [_jsx("div", { children: "Showing" }), _jsx("h2", { children: filtered.length })] })] }), _jsxs("div", { style: {
                    position: "relative",
                    marginBottom: 24,
                }, children: [_jsx(Search, { size: 18, style: {
                            position: "absolute",
                            left: 14,
                            top: 14,
                            color: "#9ca3af",
                        } }), _jsx("input", { type: "text", placeholder: "Search document...", value: keyword, onChange: (e) => setKeyword(e.target.value), style: {
                            width: "100%",
                            padding: "12px 16px 12px 42px",
                            border: "1px solid #d1d5db",
                            borderRadius: 10,
                            boxSizing: "border-box",
                            fontSize: 15,
                        } })] }), _jsx("div", { style: {
                    background: "#ffffff",
                    border: "1px solid #e5e7eb",
                    borderRadius: 12,
                    overflow: "hidden",
                    boxShadow: "0 1px 4px rgba(0,0,0,.05)",
                }, children: _jsxs("table", { style: {
                        width: "100%",
                        borderCollapse: "collapse",
                    }, children: [_jsx("thead", { children: _jsxs("tr", { children: [_jsx("th", { style: tableHeader, children: "#" }), _jsx("th", { style: tableHeader, children: "Document" }), _jsx("th", { style: tableHeader, children: "Status" })] }) }), _jsxs("tbody", { children: [filtered.length === 0 && (_jsx("tr", { children: _jsx("td", { colSpan: 3, style: {
                                            padding: 40,
                                            textAlign: "center",
                                            color: "#6b7280",
                                        }, children: "No document found." }) })), filtered.map((item, index) => {
                                    const title = item.title ??
                                        item.filename ??
                                        item.document_name ??
                                        item.document_id ??
                                        "Untitled";
                                    const ok = item.status === "pdf_available";
                                    return (_jsxs("tr", { children: [_jsx("td", { style: tableCell, children: index + 1 }), _jsx("td", { style: tableCell, children: _jsxs("div", { style: {
                                                        display: "flex",
                                                        alignItems: "center",
                                                        gap: 10,
                                                    }, children: [_jsx(FileText, { size: 18, color: "#2563eb" }), title] }) }), _jsx("td", { style: tableCell, children: _jsxs("div", { style: {
                                                        display: "inline-flex",
                                                        alignItems: "center",
                                                        gap: 6,
                                                        padding: "5px 10px",
                                                        borderRadius: 999,
                                                        background: ok
                                                            ? "#dcfce7"
                                                            : "#fef3c7",
                                                        color: ok
                                                            ? "#166534"
                                                            : "#92400e",
                                                        fontSize: 13,
                                                        fontWeight: 600,
                                                    }, children: [ok ? (_jsx(CheckCircle2, { size: 15 })) : (_jsx(AlertCircle, { size: 15 })), item.status ?? "-"] }) })] }, item.id ??
                                        item.document_id ??
                                        index));
                                })] })] }) })] }));
}
