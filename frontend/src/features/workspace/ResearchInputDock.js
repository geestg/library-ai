import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { colors, typography } from "../../design";
import { Button, Input, Card } from "../../components/ui";
import { researchAnswer } from "../../api/research";
const containerStyle = {
    padding: 24,
    borderTop: `1px solid ${colors.border}`,
    background: colors.surface,
};
const wrapperStyle = {
    maxWidth: 920,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 14,
};
const rowStyle = {
    display: "flex",
    gap: 12,
    alignItems: "center",
};
export default function ResearchInputDock() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [citations, setCitations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    async function handleSubmit() {
        const value = question.trim();
        if (!value || loading) {
            return;
        }
        setLoading(true);
        setError("");
        try {
            const response = await researchAnswer(value);
            setAnswer(response.data?.answer ?? "");
            setCitations(response.data?.citations ?? []);
        }
        catch (error) {
            setAnswer("");
            setCitations([]);
            setError(error instanceof Error
                ? error.message
                : "Failed to get research answer.");
        }
        finally {
            setLoading(false);
        }
    }
    return (_jsxs("div", { children: [answer && (_jsxs(Card, { style: {
                    marginBottom: 16,
                }, children: [_jsx("div", { style: {
                            ...typography.h4,
                            marginBottom: 10,
                        }, children: "DELBot Answer" }), _jsx("div", { style: {
                            ...typography.body,
                            color: colors.text,
                            whiteSpace: "pre-wrap",
                            lineHeight: 1.7,
                        }, children: answer }), citations.length > 0 && (_jsxs("div", { style: {
                            marginTop: 16,
                            paddingTop: 12,
                            borderTop: `1px solid ${colors.border}`,
                        }, children: [_jsxs("div", { style: {
                                    ...typography.caption,
                                    color: colors.textSecondary,
                                    marginBottom: 8,
                                }, children: ["Sources: ", citations.length] }), citations.map((citation, index) => (_jsxs("div", { style: {
                                    ...typography.caption,
                                    color: colors.textSecondary,
                                    marginBottom: 4,
                                }, children: [index + 1, ".", " ", citation.section || "Document", citation.page_start
                                        ? ` · Page ${citation.page_start}`
                                        : ""] }, `${citation.document_id ?? "document"}-${index}`)))] }))] })), error && (_jsx(Card, { style: {
                    marginBottom: 16,
                }, children: _jsxs("div", { style: {
                        ...typography.caption,
                        color: colors.textSecondary,
                    }, children: ["Research request failed: ", error] }) })), _jsx("footer", { style: containerStyle, children: _jsxs("div", { style: wrapperStyle, children: [_jsx(Input, { value: question, onChange: (event) => setQuestion(event.target.value), onKeyDown: (event) => {
                                if (event.key === "Enter" &&
                                    !event.shiftKey) {
                                    event.preventDefault();
                                    handleSubmit();
                                }
                            }, placeholder: "Ask a research question, compare papers, summarize literature...", disabled: loading }), _jsxs("div", { style: {
                                ...rowStyle,
                                justifyContent: "space-between",
                            }, children: [_jsx("div", { style: {
                                        ...typography.caption,
                                        color: colors.textSecondary,
                                    }, children: "Answers are generated from indexed repository documents with citations." }), _jsx(Button, { onClick: handleSubmit, disabled: loading ||
                                        question.trim().length === 0, children: loading ? "Searching..." : "Ask DELBot" })] })] }) })] }));
}
