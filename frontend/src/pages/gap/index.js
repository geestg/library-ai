import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import { useState } from "react";
import { researchAnswer } from "../../api/research";
export default function GapPage() {
    const [topic, setTopic] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const sessionId = localStorage.getItem("delbot_research_session_id") ||
        "default";
    async function analyzeGap() {
        const value = topic.trim();
        if (!value || loading) {
            return;
        }
        setLoading(true);
        setError("");
        try {
            const response = await researchAnswer(`Analyze the research gaps in the academic literature related to: ${value}. Identify important missing areas, limitations, contradictions, or opportunities supported by the indexed documents.`, sessionId);
            setAnswer(response.data.answer);
            if (response.data.session_id) {
                localStorage.setItem("delbot_research_session_id", response.data.session_id);
            }
        }
        catch {
            setAnswer("");
            setError("Unable to analyze research gap.");
        }
        finally {
            setLoading(false);
        }
    }
    return (_jsx(WorkspaceShell, { children: _jsx("main", { style: {
                minHeight: "100vh",
                padding: 40,
                background: "#f7f8fa",
                fontFamily: "Inter, system-ui, sans-serif",
            }, children: _jsxs("section", { style: {
                    maxWidth: 960,
                    margin: "0 auto",
                }, children: [_jsxs("div", { style: { marginBottom: 28 }, children: [_jsx("div", { style: {
                                    fontSize: 13,
                                    color: "#64748b",
                                    marginBottom: 8,
                                }, children: "DELBot / Research Gap" }), _jsx("h1", { style: {
                                    margin: 0,
                                    fontSize: 30,
                                }, children: "Research Gap" }), _jsx("p", { style: {
                                    color: "#64748b",
                                    lineHeight: 1.6,
                                }, children: "Identify potential research gaps from the indexed academic literature." })] }), _jsxs("section", { style: {
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: 14,
                            padding: 24,
                        }, children: [_jsx("input", { value: topic, onChange: (event) => setTopic(event.target.value), placeholder: "Research topic...", style: {
                                    width: "100%",
                                    boxSizing: "border-box",
                                    padding: 13,
                                    border: "1px solid #dbe1e8",
                                    borderRadius: 9,
                                    fontSize: 15,
                                } }), _jsx("button", { onClick: analyzeGap, disabled: loading, style: {
                                    marginTop: 12,
                                    padding: "10px 18px",
                                    border: 0,
                                    borderRadius: 9,
                                    background: "#1f2937",
                                    color: "#ffffff",
                                }, children: loading
                                    ? "Analyzing..."
                                    : "Analyze Gap" }), error && (_jsx("p", { style: { color: "#b91c1c" }, children: error }))] }), answer && (_jsxs("section", { style: {
                            marginTop: 20,
                            background: "#ffffff",
                            border: "1px solid #e5e7eb",
                            borderRadius: 14,
                            padding: 24,
                        }, children: [_jsx("h2", { children: "Potential Research Gaps" }), _jsx("p", { style: {
                                    whiteSpace: "pre-wrap",
                                    lineHeight: 1.7,
                                }, children: answer })] }))] }) }) }));
}
