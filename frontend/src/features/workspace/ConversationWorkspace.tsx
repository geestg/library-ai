import { colors, typography, spacing, radius } from "../../design";
import ResearchInputDock from "./ResearchInputDock";

const rootStyle: React.CSSProperties = {
    display: "flex",
    width: "100%",
    minHeight: "calc(100vh - 60px)",
    background: colors.background,
    overflow: "hidden",
};

const mainStyle: React.CSSProperties = {
    flex: 1,
    minWidth: 0,
    display: "flex",
    flexDirection: "column",
    padding: `${spacing.xl}px ${spacing.xxl}px`,
    overflow: "hidden",
};

const headerStyle: React.CSSProperties = {
    marginBottom: spacing.lg,
};

const titleStyle: React.CSSProperties = {
    ...typography.h1,
    margin: 0,
    color: colors.text,
};

const descriptionStyle: React.CSSProperties = {
    ...typography.body,
    margin: "6px 0 0",
    maxWidth: 760,
    color: colors.textSecondary,
};

const streamStyle: React.CSSProperties = {
    flex: 1,
    minHeight: 260,
    overflowY: "auto",
    background: colors.surface,
    border: `1px solid ${colors.border}`,
    borderRadius: radius.md,
};

const emptyStyle: React.CSSProperties = {
    minHeight: 260,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: spacing.xxl,
    textAlign: "center",
};

const emptyTitleStyle: React.CSSProperties = {
    ...typography.h3,
    color: colors.text,
    marginBottom: spacing.sm,
};

const emptyTextStyle: React.CSSProperties = {
    ...typography.body,
    color: colors.textSecondary,
    maxWidth: 560,
    lineHeight: 1.7,
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
                        Ask questions, compare literature, and
                        investigate research problems using your
                        indexed academic repository.
                    </p>
                </header>

                <div style={streamStyle}>
                    <div style={emptyStyle}>
                        <div style={emptyTitleStyle}>
                            Start your research
                        </div>

                        <div style={emptyTextStyle}>
                            Ask a focused academic question below.
                            DELBot will retrieve relevant repository
                            content and provide an evidence-backed
                            answer with citations.
                        </div>
                    </div>
                </div>

                <ResearchInputDock />
            </div>

        </section>
    );
}
