import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { colors } from "../../design";
import Citation from "../../components/citation/Citation";
import PDFEvidenceViewer from "../../components/pdf/PDFEvidenceViewer";
const panelStyle = {
    width: 340,
    display: "flex",
    flexDirection: "column",
    background: colors.surface,
    borderLeft: `1px solid ${colors.border}`,
};
const bodyStyle = {
    padding: 20,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 16,
};
export default function CitationPanel() {
    return (_jsx("aside", { style: panelStyle, children: _jsxs(_Fragment, { children: [_jsx(Citation, {}), _jsx(PDFEvidenceViewer, {})] }) }));
}
