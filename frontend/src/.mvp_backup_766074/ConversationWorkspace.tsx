import { colors, typography, spacing, radius } from "../../design";
import ResearchInputDock from "./ResearchInputDock";
import CitationPanel from "./CitationPanel";

const rootStyle: React.CSSProperties = {
    display: "flex",
    width: "100%",
    minHeight: "calc(100vh - 60px)",
    background: colors.background,
};

const mainStyle: React.CSSProperties = {
    flex: 1,
    minWidth: 0,
    display: "flex",
    flexDirection: "column",
};

const headerStyle: React.CSSProperties = {
    padding: "28px 32px 20px",
    borderBottom: `1px solid ${colors.border}`,
    background: colors.surface,
};

const titleStyle: React.CSSProperties = {
    ...typography.h1,
    color: colors.text,
    margin: 0,
};

const descriptionStyle: React.CSSProperties = {
    ...typography.body,
    color: colors.textSecondary,
    margin: "8px 0 0",
    maxWidth: 760,
};

const streamStyle: React.CSSProperties = {
    flex: 1,
    minHeight: 280,
    padding: "28px 32px",
    overflowY: "auto",
};

const emptyStyle: React.CSSProperties = {
    maxWidth: 760,
    margin: "48px auto",
    padding: "36px 40px",
    border: `1px solid ${colors.border}`,
    borderRadius: radius.lg,
    background: colors.surface,
};

const emptyTitleStyle: React.CSSProperties = {
    ...typography.h3,
    color: colors.text,
    margin: 0,
};

const emptyTextStyle: React.CSSProperties = {
    ...typography.body,
    color: colors.textSecondary,
    lineHeight: 1.7,
    margin: `${spacing.sm}px 0 0`,
};

export default function ConversationWorkspace() {
    return (
        <section style={rootStyle}>
            <div style={mainStyle}>
                <header style={headerStyle}>
                    <h1 style={titleStyle}>
                        Research Workspace
                    </h1>

                    <p style={descriptionStyle}>
                        Ask academic questions, compare literature,
                        discover research gaps, and develop thesis ideas
                        using evidence from your indexed repository.
                    </p>
                </header>

                <div style={streamStyle}>
                    <div style={emptyStyle}>
                        <h2 style={emptyTitleStyle}>
                            Start your research
                        </h2>

                        <p style={emptyTextStyle}>
                            Enter a research question below. DELBot will
                            search the indexed repository and return an
                            evidence-backed answer with source citations.
                        </p>
                    </div>
                </div>

                <ResearchInputDock />
            </div>

            <CitationPanel />
        </section>
    );
}
