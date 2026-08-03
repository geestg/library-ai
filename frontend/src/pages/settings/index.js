import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Settings, Server, Database, BrainCircuit, ShieldCheck, Construction, } from "lucide-react";
export default function SettingsPage() {
    const card = {
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };
    const row = {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "14px 0",
        borderTop: "1px solid #f1f5f9",
    };
    return (_jsxs("div", { children: [_jsxs("div", { style: {
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    marginBottom: 24,
                }, children: [_jsx(Settings, { size: 34 }), _jsxs("div", { children: [_jsx("h1", { style: { margin: 0 }, children: "Settings" }), _jsx("div", { style: {
                                    color: "#64748b",
                                    marginTop: 4,
                                }, children: "DELBot MVP Configuration" })] })] }), _jsxs("div", { style: {
                    ...card,
                    marginBottom: 24,
                    display: "flex",
                    gap: 12,
                    alignItems: "center",
                    background: "#fff7ed",
                    border: "1px solid #fed7aa",
                }, children: [_jsx(Construction, { size: 22, color: "#ea580c" }), _jsxs("div", { children: [_jsx("strong", { children: "Configuration UI is not available yet." }), _jsx("div", { style: {
                                    marginTop: 6,
                                    color: "#9a3412",
                                }, children: "Backend configuration endpoints have not been implemented in the MVP." })] })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))",
                    gap: 20,
                }, children: [_jsxs("div", { style: card, children: [_jsxs("h2", { style: {
                                    marginTop: 0,
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 10,
                                }, children: [_jsx(Server, { size: 20 }), "Backend"] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Gateway" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Repository API" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Research API" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Settings API" }), _jsx("strong", { children: "NOT AVAILABLE" })] })] }), _jsxs("div", { style: card, children: [_jsxs("h2", { style: {
                                    marginTop: 0,
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 10,
                                }, children: [_jsx(Database, { size: 20 }), "Repository"] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Repository Explorer" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Document Index" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Semantic Search" }), _jsx("strong", { children: "PLACEHOLDER" })] })] }), _jsxs("div", { style: card, children: [_jsxs("h2", { style: {
                                    marginTop: 0,
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 10,
                                }, children: [_jsx(BrainCircuit, { size: 20 }), "AI Services"] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Research Pipeline" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Citation Builder" }), _jsx("strong", { children: "READY" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Semantic Search API" }), _jsx("strong", { children: "NOT AVAILABLE" })] })] }), _jsxs("div", { style: card, children: [_jsxs("h2", { style: {
                                    marginTop: 0,
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 10,
                                }, children: [_jsx(ShieldCheck, { size: 20 }), "MVP Status"] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Dashboard" }), _jsx("strong", { children: "PASS" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Repository" }), _jsx("strong", { children: "PASS" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Documents" }), _jsx("strong", { children: "PASS" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Research" }), _jsx("strong", { children: "PASS" })] }), _jsxs("div", { style: row, children: [_jsx("span", { children: "Frontend Build" }), _jsx("strong", { children: "PASS" })] })] })] })] }));
}
