import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, typography, radius, spacing } from "../../design";
import Citation from "../../components/citation/Citation";
import PDFEvidenceViewer from "../../components/pdf/PDFEvidenceViewer";
const panelStyle = {
    width: 340,
    minWidth: 340,
    height: "100%",
    padding: `${spacing.xl}px ${spacing.lg}px`,
    borderLeft: `1px solid ${colors.border}`,
    background: colors.surfaceSecondary,
    overflowY: "auto",
};
const headerStyle = {
    marginBottom: spacing.lg,
};
const titleStyle = {
    ...typography.h3,
    margin: 0,
    color: colors.text,
};
const descriptionStyle = {
    ...typography.caption,
    marginTop: 5,
    color: colors.textSecondary,
    lineHeight: 1.5,
};
const evidenceStyle = {
    background: colors.surface,
    border: `1px solid ${colors.border}`,
    borderRadius: radius.md,
    overflow: "hidden",
};
export default function CitationPanel() {
    return (_jsxs("aside", { style: panelStyle, children: [_jsxs("div", { style: headerStyle, children: [_jsx("div", { style: titleStyle, children: "Evidence" }), _jsx("div", { style: descriptionStyle, children: "Sources and document context used by DELBot." })] }), _jsx("div", { style: evidenceStyle, children: _jsx(Citation, {}) }), _jsx(PDFEvidenceViewer, {})] }));
}
