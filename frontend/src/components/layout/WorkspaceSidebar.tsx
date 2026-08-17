import {
    FileSearch,
    FileText,
    Lightbulb,
    LayoutDashboard,
    Search,
    Target,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import { colors, typography } from "../../design";

const sidebarStyle: React.CSSProperties = {
    width: 240,
    minWidth: 240,
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    background: colors.surface,
    borderRight: `1px solid ${colors.border}`,
};

const headerStyle: React.CSSProperties = {
    padding: "22px 20px 20px",
};

const navStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: 4,
    padding: 12,
};

const labelStyle: React.CSSProperties = {
    padding: "4px 12px 8px",
    color: colors.textMuted,
    fontSize: 10,
    fontWeight: 700,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
};

const linkStyle: React.CSSProperties = {
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

const footerStyle: React.CSSProperties = {
    marginTop: "auto",
    padding: "14px 20px 18px",
    borderTop: `1px solid ${colors.border}`,
};

export default function WorkspaceSidebar() {
    return (
        <aside style={sidebarStyle}>
            <div style={headerStyle}>
                <div
                    style={{
                        ...typography.h3,
                        color: colors.text,
                    }}
                >
                    DELBot
                </div>

                <div
                    style={{
                        ...typography.caption,
                        color: colors.textMuted,
                        marginTop: 4,
                    }}
                >
                    Academic Research Intelligence
                </div>
            </div>

            <div
                style={{
                    height: 1,
                    background: colors.border,
                }}
            />

            <nav style={navStyle}>
                <div style={labelStyle}>
                    Research
                </div>

                <NavLink
                    to="/"
                    end
                    style={({ isActive }) => ({
                        ...linkStyle,
                        background: isActive
                            ? colors.primarySoft
                            : "transparent",
                        color: isActive
                            ? colors.primary
                            : colors.textSecondary,
                    })}
                >
                    <LayoutDashboard size={17} />
                    <span>Workspace</span>
                </NavLink>

                <NavLink
                    to="/search"
                    style={({ isActive }) => ({
                        ...linkStyle,
                        background: isActive
                            ? colors.primarySoft
                            : "transparent",
                        color: isActive
                            ? colors.primary
                            : colors.textSecondary,
                    })}
                >
                    <Search size={17} />
                    <span>Semantic Search</span>
                </NavLink>

                <NavLink
                    to="/research"
                    style={({ isActive }) => ({
                        ...linkStyle,
                        background: isActive
                            ? colors.primarySoft
                            : "transparent",
                        color: isActive
                            ? colors.primary
                            : colors.textSecondary,
                    })}
                >
                    <FileSearch size={17} />
                    <span>Research</span>
                </NavLink>

                <div
                    style={{
                        ...labelStyle,
                        marginTop: 12,
                    }}
                >
                    Research Output
                </div>

                <NavLink
                    to="/gap"
                    style={({ isActive }) => ({
                        ...linkStyle,
                        background: isActive
                            ? colors.primarySoft
                            : "transparent",
                        color: isActive
                            ? colors.primary
                            : colors.textSecondary,
                    })}
                >
                    <Target size={17} />
                    <span>Research Gap</span>
                </NavLink>

                <NavLink
                    to="/thesis-ideas"
                    style={({ isActive }) => ({
                        ...linkStyle,
                        background: isActive
                            ? colors.primarySoft
                            : "transparent",
                        color: isActive
                            ? colors.primary
                            : colors.textSecondary,
                    })}
                >
                    <Lightbulb size={17} />
                    <span>Thesis Ideas</span>
                </NavLink>

                <div
                    style={{
                        ...labelStyle,
                        marginTop: 12,
                    }}
                >
                    Knowledge
                </div>

                <NavLink
                    to="/repository"
                    style={({ isActive }) => ({
                        ...linkStyle,
                        background: isActive
                            ? colors.primarySoft
                            : "transparent",
                        color: isActive
                            ? colors.primary
                            : colors.textSecondary,
                    })}
                >
                    <FileText size={17} />
                    <span>Repository</span>
                </NavLink>
            </nav>

            <div style={footerStyle}>
                <div
                    style={{
                        ...typography.caption,
                        color: colors.textMuted,
                    }}
                >
                    MVP Thesis Edition
                </div>
            </div>
        </aside>
    );
}
