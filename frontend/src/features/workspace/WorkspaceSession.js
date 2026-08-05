import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "../../components/ui";
import { typography, colors } from "../../design";
export default function WorkspaceSession() {
    return (_jsxs(Card, { style: {
            marginTop: 16,
            background: colors.surfaceSecondary,
        }, children: [_jsx("div", { style: typography.label, children: "Current Workspace" }), _jsx("div", { style: {
                    ...typography.bodyMedium,
                    marginTop: 8,
                    color: colors.text,
                }, children: "Untitled Research" }), _jsx("div", { style: {
                    ...typography.caption,
                    marginTop: 6,
                    color: colors.textSecondary,
                }, children: "No conversation history yet." })] }));
}
