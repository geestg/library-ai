import { colors, typography, radius, spacing } from "../../design";
import Citation from "../../components/citation/Citation";
import PDFEvidenceViewer from "../../components/pdf/PDFEvidenceViewer";

const panelStyle: React.CSSProperties = {
    width: 340,
    minWidth: 340,
    height: "100%",
    padding: `${spacing.xl}px ${spacing.lg}px`,
    borderLeft: `1px solid ${colors.border}`,
    background: colors.surfaceSecondary,
    overflowY: "auto",
};

const headerStyle: React.CSSProperties = {
    marginBottom: spacing.lg,
};

const titleStyle: React.CSSProperties = {
    ...typography.h3,
    margin: 0,
    color: colors.text,
};

const descriptionStyle: React.CSSProperties = {
    ...typography.caption,
    marginTop: 5,
    color: colors.textSecondary,
    lineHeight: 1.5,
};

const evidenceStyle: React.CSSProperties = {
    background: colors.surface,
    border: `1px solid ${colors.border}`,
    borderRadius: radius.md,
    overflow: "hidden",
};

export default function CitationPanel() {
    return (
        <aside style={panelStyle}>
            <div style={headerStyle}>
                <div style={titleStyle}>
                    Evidence
                </div>

                <div style={descriptionStyle}>
                    Sources and document context used by DELBot.
                </div>
            </div>

            <div style={evidenceStyle}>
                <Citation />
            </div>

            <PDFEvidenceViewer />
        </aside>
    );
}
