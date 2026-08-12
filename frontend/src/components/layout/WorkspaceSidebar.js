import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { FileText, LayoutDashboard, } from "lucide-react";
import { NavLink } from "react-router-dom";
import { colors, typography } from "../../design";
const sidebarStyle = {
    width: 240,
    minWidth: 240,
    display: "flex",
    flexDirection: "column",
    background: colors.surface,
    borderRight: `1px solid ${colors.border}`,
};
const headerStyle = {
    padding: "22px 20px 20px",
};
const navStyle = {
    display: "flex",
    flexDirection: "column",
    gap: 4,
    padding: 12,
};
const linkStyle = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "10px 12px",
    borderRadius: 8,
    color: colors.textSecondary,
    fontSize: 14,
    fontWeight: 500,
};
export default function WorkspaceSidebar() {
    return (_jsxs("aside", { style: sidebarStyle, children: [_jsxs("div", { style: headerStyle, children: [_jsx("div", { style: {
                            ...typography.h3,
                            color: colors.text,
                        }, children: "DELBOT" }), _jsx("div", { style: {
                            ...typography.caption,
                            color: colors.textMuted,
                            marginTop: 4,
                        } })] }), _jsx("div", { style: {
                    height: 1,
                    background: colors.border,
                } }), _jsxs("nav", { style: navStyle, children: [_jsx("div", { style: {
                            fontSize: "18px",
                            fontWeight: 800,
                            letterSpacing: "0.08em",
                            marginBottom: "18px",
                            padding: "0 12px",
                        } }), _jsxs(NavLink, { to: "/", end: true, style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(LayoutDashboard, { size: 17 }), _jsx("span", { children: "Research Workspace" })] }), _jsxs(NavLink, { to: "/repository", style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(FileText, { size: 17 }), _jsx("span", { children: "Repository" })] })] }), _jsx("div", { style: {
                    marginTop: "auto",
                    padding: "16px 20px",
                    borderTop: `1px solid ${colors.border}`,
                }, children: _jsx("div", { style: {
                        ...typography.caption,
                        color: colors.textMuted,
                    } }) })] }));
}
