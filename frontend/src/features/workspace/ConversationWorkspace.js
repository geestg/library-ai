import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, typography, spacing, radius } from "../../design";
import ResearchInputDock from "./ResearchInputDock";
const rootStyle = {
    display: "flex",
    width: "100%",
    minHeight: "calc(100vh - 60px)",
    background: colors.background,
    overflow: "hidden",
};
const mainStyle = {
    flex: 1,
    minWidth: 0,
    display: "flex",
    flexDirection: "column",
    padding: `${spacing.xl}px ${spacing.xxl}px`,
    overflow: "hidden",
};
const headerStyle = {
    marginBottom: spacing.lg,
};
const titleStyle = {
    ...typography.h1,
    margin: 0,
    color: colors.text,
};
const descriptionStyle = {
    ...typography.body,
    margin: "6px 0 0",
    maxWidth: 760,
    color: colors.textSecondary,
};
const streamStyle = {
    flex: 1,
    minHeight: 260,
    overflowY: "auto",
    background: colors.surface,
    border: `1px solid ${colors.border}`,
    borderRadius: radius.md,
};
const emptyStyle = {
    minHeight: 260,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: spacing.xxl,
    textAlign: "center",
};
const emptyTitleStyle = {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.sm,
};
const emptyTextStyle = {
    ...typography.body,
    color: colors.textSecondary,
    maxWidth: 560,
    lineHeight: 1.7,
};
export default function ConversationWorkspace() {
    return (_jsx("section", { style: rootStyle, children: _jsxs("div", { style: mainStyle, children: [_jsxs("header", { style: headerStyle, children: [_jsx("h1", { style: titleStyle, children: "Research Workspace" }), _jsx("p", { style: descriptionStyle, children: "Ask questions, compare literature, and investigate research problems using your indexed academic repository." })] }), _jsx("div", { style: streamStyle, children: _jsxs("div", { style: emptyStyle, children: [_jsx("div", { style: emptyTitleStyle, children: "Start your research" }), _jsx("div", { style: emptyTextStyle, children: "Ask a focused academic question below. DELBot will retrieve relevant repository content and provide an evidence-backed answer with citations." })] }) }), _jsx(ResearchInputDock, {})] }) }));
}
