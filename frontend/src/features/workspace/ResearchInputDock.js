import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, typography } from "../../design";
import { Button, Input } from "../../components/ui";
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
    return (_jsx("footer", { style: containerStyle, children: _jsxs("div", { style: wrapperStyle, children: [_jsx(Input, { placeholder: "Ask a research question, compare papers, summarize literature..." }), _jsxs("div", { style: {
                        ...rowStyle,
                        justifyContent: "space-between",
                    }, children: [_jsx("div", { style: {
                                ...typography.caption,
                                color: colors.textSecondary,
                            }, children: "Answers are generated from indexed repository documents with citations." }), _jsx(Button, { children: "Ask DELBot" })] })] }) }));
}
