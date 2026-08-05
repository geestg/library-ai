import { colors, typography } from "../../design";
import { Button } from "../../components/ui";

const topbarStyle: React.CSSProperties = {
    height: 60,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    borderBottom: `1px solid ${colors.border}`,
    background: colors.surface,
};

const leftStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: 2,
};

const rightStyle: React.CSSProperties = {
    display: "flex",
    alignItems: "center",
    gap: 10,
};

export default function WorkspaceTopbar() {
    return (
        <header style={topbarStyle}>
            <div style={leftStyle}>
                <span
                    style={{
                        ...typography.h3,
                        color: colors.text,
                    }}
                >
                    DELBot
                </span>

                <span
                    style={{
                        ...typography.caption,
                        color: colors.textSecondary,
                    }}
                >
                    Academic Research Workspace
                </span>
            </div>

            <div style={rightStyle}>
                <Button>
                    Import Repository
                </Button>
            </div>
        </header>
    );
}
