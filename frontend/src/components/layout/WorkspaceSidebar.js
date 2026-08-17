import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { FileSearch, FileText, Lightbulb, LayoutDashboard, Search, Target, } from "lucide-react";
import { NavLink } from "react-router-dom";
import { colors, typography } from "../../design";
const sidebarStyle = {
    width: 240,
    minWidth: 240,
    minHeight: "100vh",
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
const labelStyle = {
    padding: "4px 12px 8px",
    color: colors.textMuted,
    fontSize: 10,
    fontWeight: 700,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
};
const linkStyle = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    minHeight: 38,
    padding: "9px 12px",
    borderRadius: 8,
    color: colors.textSecondary,
    fontSize: 13,
    fontWeight: 500,
};
const footerStyle = {
    marginTop: "auto",
    padding: "14px 20px 18px",
    borderTop: `1px solid ${colors.border}`,
};
export default function WorkspaceSidebar() {
    return (_jsxs("aside", { style: sidebarStyle, children: [_jsxs("div", { style: headerStyle, children: [_jsx("div", { style: {
                            ...typography.h3,
                            color: colors.text,
                        }, children: "DELBot" }), _jsx("div", { style: {
                            ...typography.caption,
                            color: colors.textMuted,
                            marginTop: 4,
                        }, children: "Academic Research Intelligence" })] }), _jsx("div", { style: {
                    height: 1,
                    background: colors.border,
                } }), _jsxs("nav", { style: navStyle, children: [_jsx("div", { style: labelStyle, children: "Research" }), _jsxs(NavLink, { to: "/", end: true, style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(LayoutDashboard, { size: 17 }), _jsx("span", { children: "Workspace" })] }), _jsxs(NavLink, { to: "/search", style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(Search, { size: 17 }), _jsx("span", { children: "Semantic Search" })] }), _jsxs(NavLink, { to: "/research", style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(FileSearch, { size: 17 }), _jsx("span", { children: "Research" })] }), _jsx("div", { style: {
                            ...labelStyle,
                            marginTop: 12,
                        }, children: "Research Output" }), _jsxs(NavLink, { to: "/gap", style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(Target, { size: 17 }), _jsx("span", { children: "Research Gap" })] }), _jsxs(NavLink, { to: "/thesis-ideas", style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(Lightbulb, { size: 17 }), _jsx("span", { children: "Thesis Ideas" })] }), _jsx("div", { style: {
                            ...labelStyle,
                            marginTop: 12,
                        }, children: "Knowledge" }), _jsxs(NavLink, { to: "/repository", style: ({ isActive }) => ({
                            ...linkStyle,
                            background: isActive
                                ? colors.primarySoft
                                : "transparent",
                            color: isActive
                                ? colors.primary
                                : colors.textSecondary,
                        }), children: [_jsx(FileText, { size: 17 }), _jsx("span", { children: "Repository" })] })] }), _jsx("div", { style: footerStyle, children: _jsx("div", { style: {
                        ...typography.caption,
                        color: colors.textMuted,
                    }, children: "MVP Thesis Edition" }) })] }));
}
