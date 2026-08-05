import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { colors, layout, typography } from "../../design";
import { Button, Divider } from "../../components/ui";
import WorkspaceSession from "../../features/workspace/WorkspaceSession";
const sidebarStyle = {
    width: layout.sidebar.width,
    minWidth: layout.sidebar.minWidth,
    display: "flex",
    flexDirection: "column",
    background: colors.surface,
    borderRight: `1px solid ${colors.border}`,
};
const headerStyle = {
    padding: 20,
};
const workspaceListStyle = {
    flex: 1,
    padding: "0 12px 16px",
    overflowY: "auto",
};
const workspaceItemStyle = {
    padding: "10px 12px",
    borderRadius: 10,
    cursor: "pointer",
    color: colors.textSecondary,
    transition: "all .15s ease",
    marginBottom: 4,
};
export default function WorkspaceSidebar() {
    return (_jsxs("aside", { style: sidebarStyle, children: [_jsxs("div", { style: headerStyle, children: [_jsx("div", { style: {
                            ...typography.h3,
                            color: colors.text,
                            marginBottom: 4,
                        }, children: "DELBot" }), _jsx("div", { style: {
                            ...typography.caption,
                            color: colors.textMuted,
                        }, children: "Academic Research Workspace" })] }), _jsx(Divider, {}), _jsx(WorkspaceSession, {}), _jsx("div", { style: { padding: 16 }, children: _jsx(Button, { style: { width: "100%" }, children: "+ New Workspace" }) }), _jsx(Divider, {}), _jsx(WorkspaceSession, {}), _jsx("div", { style: workspaceListStyle, children: _jsx("div", { style: workspaceItemStyle, children: "Untitled Research" }) })] }));
}
