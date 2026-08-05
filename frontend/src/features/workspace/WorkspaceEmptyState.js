import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "../../components/ui";
import { typography, colors } from "../../design";
export default function WorkspaceEmptyState() {
    return (_jsxs(Card, { style: {
            maxWidth: 760,
            margin: "72px auto",
            padding: 48,
            textAlign: "center",
            background: colors.surface,
        }, children: [_jsx("div", { style: {
                    ...typography.h2,
                    color: colors.text,
                    marginBottom: 12,
                }, children: "Start Your Research" }), _jsx("div", { style: {
                    ...typography.body,
                    color: colors.textSecondary,
                    lineHeight: 1.8,
                    maxWidth: 560,
                    margin: "0 auto",
                }, children: "Ask a research question, compare multiple papers, discover research gaps, generate literature reviews, or explore your repository with evidence-based answers." })] }));
}
