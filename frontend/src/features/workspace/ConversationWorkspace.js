import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, typography } from "../../design";
import { Card } from "../../components/ui";
import ResearchInputDock from "./ResearchInputDock";
import CitationPanel from "./CitationPanel";
const workspaceStyle = {
    flex: 1,
    display: "flex",
    background: colors.background,
    overflow: "hidden",
};
const conversationStyle = {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: 32,
    gap: 24,
    overflowY: "auto",
};
export default function ConversationWorkspace() {
    return (_jsxs("section", { style: workspaceStyle, children: [_jsxs("div", { style: conversationStyle, children: [_jsxs(Card, { children: [_jsx("div", { style: {
                                    ...typography.h2,
                                    marginBottom: 8,
                                }, children: "Research Workspace" }), _jsx("div", { style: {
                                    ...typography.body,
                                    color: colors.textSecondary,
                                    lineHeight: 1.7,
                                }, children: "Ask academic questions, compare papers, discover research gaps, generate thesis ideas, and explore your knowledge base with evidence-backed answers." })] }), _jsx("div", { style: {
                            flex: 1,
                            border: `1px dashed ${colors.border}`,
                            borderRadius: 12,
                            background: colors.surface,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            color: colors.textSecondary,
                        }, children: "Conversation Stream" }), _jsx(ResearchInputDock, {})] }), _jsx(CitationPanel, {})] }));
}
