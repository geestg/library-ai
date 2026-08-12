import { colors, layout, typography } from "../../design";
import { Button, Divider } from "../../components/ui";
import WorkspaceSession from "../../features/workspace/WorkspaceSession";

const sidebarStyle: React.CSSProperties = {
    width: layout.sidebar.width,
    minWidth: layout.sidebar.minWidth,
    display: "flex",
    flexDirection: "column",
    background: colors.surface,
    borderRight: `1px solid ${colors.border}`,
};

const headerStyle: React.CSSProperties = {
    padding: 20,
};

const workspaceListStyle: React.CSSProperties = {
    flex: 1,
    padding: "0 12px 16px",
    overflowY: "auto",
};

const workspaceItemStyle: React.CSSProperties = {
    padding: "10px 12px",
    borderRadius: 10,
    cursor: "pointer",
    color: colors.textSecondary,
    transition: "all .15s ease",
    marginBottom: 4,
};

export default function WorkspaceSidebar() {
    return (
        <aside style={sidebarStyle}>

            <div style={headerStyle}>

                <div
                    style={{
                        ...typography.h3,
                        color: colors.text,
                        marginBottom: 4,
                    }}
                >
                    DELBot
                </div>

                <div
                    style={{
                        ...typography.caption,
                        color: colors.textMuted,
                    }}
                >
                    Academic Research Workspace
                </div>

            </div>

            <Divider />

            <WorkspaceSession />

            <div style={{ padding: 16 }}>
                <Button style={{ width: "100%" }}>
                    + New Workspace
                </Button>
            </div>

            <Divider />

            <WorkspaceSession />

            <div style={workspaceListStyle}>

                <div style={workspaceItemStyle}>
                    Untitled Research
                </div>

            </div>

        </aside>
    );
}
