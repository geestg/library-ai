import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Link } from "react-router-dom";
import { BrainCircuit, ArrowLeft, Sparkles, } from "lucide-react";
export default function ResearchPage() {
    const card = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 2px 8px rgba(15,23,42,.05)",
    };
    return (_jsx("div", { style: {
            maxWidth: 900,
            margin: "0 auto",
        }, children: _jsxs("div", { style: card, children: [_jsxs("div", { style: {
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        marginBottom: 24,
                    }, children: [_jsx(BrainCircuit, { size: 32, color: "#2563eb" }), _jsx("h1", { style: {
                                margin: 0,
                            }, children: "AI Research Workspace" })] }), _jsx("p", { style: {
                        lineHeight: 1.9,
                        color: "#64748b",
                        marginBottom: 32,
                    }, children: "DELBot now starts every research session directly from the AI Workspace on the Dashboard. Conversation, evidence retrieval, citations, and repository reasoning are unified into a single workspace experience." }), _jsxs("div", { style: {
                        padding: 24,
                        borderRadius: 12,
                        background: "#f8fafc",
                        border: "1px solid #e5e7eb",
                        marginBottom: 32,
                    }, children: [_jsxs("div", { style: {
                                display: "flex",
                                alignItems: "center",
                                gap: 10,
                                marginBottom: 12,
                            }, children: [_jsx(Sparkles, { size: 20, color: "#2563eb" }), _jsx("strong", { children: "Research now begins from Dashboard" })] }), _jsxs("div", { style: {
                                lineHeight: 1.8,
                                color: "#64748b",
                            }, children: ["\u2022 AI Conversation", _jsx("br", {}), "\u2022 Repository Evidence", _jsx("br", {}), "\u2022 Citation Panel", _jsx("br", {}), "\u2022 Workspace Memory", _jsx("br", {}), "\u2022 Research Timeline"] })] }), _jsxs(Link, { to: "/", style: {
                        display: "inline-flex",
                        alignItems: "center",
                        gap: 10,
                        padding: "14px 22px",
                        borderRadius: 12,
                        background: "#2563eb",
                        color: "#ffffff",
                        textDecoration: "none",
                        fontWeight: 700,
                    }, children: [_jsx(ArrowLeft, { size: 18 }), "Return to AI Workspace"] })] }) }));
}
