import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "../../components/ui";
import { colors, typography } from "../../design";
export default function PDFEvidenceViewer({ title = "No document selected", page, }) {
    return (_jsxs(Card, { style: {
            marginTop: 24,
            display: "flex",
            flexDirection: "column",
            gap: 16,
            minHeight: 320,
        }, children: [_jsx("div", { style: typography.h4, children: "PDF Preview" }), _jsx("div", { style: {
                    ...typography.caption,
                    color: colors.textSecondary,
                }, children: title }), _jsxs("div", { style: {
                    flex: 1,
                    minHeight: 220,
                    border: `1px dashed ${colors.border}`,
                    borderRadius: 10,
                    background: colors.surfaceSecondary,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: colors.textMuted,
                    textAlign: "center",
                    padding: 32,
                }, children: ["PDF Preview Area", page
                        ? ` (Page ${page})`
                        : ""] })] }));
}
