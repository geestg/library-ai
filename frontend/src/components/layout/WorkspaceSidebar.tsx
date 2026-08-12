import {
    FileText,
    LayoutDashboard,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import { colors, typography } from "../../design";

const sidebarStyle: React.CSSProperties = {
    width: 240,
    minWidth: 240,
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

const linkStyle: React.CSSProperties = {
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
    return (
        <aside style={sidebarStyle}>

            <div style={headerStyle}>
                <div
                    style={{
                        ...typography.h3,
                        color: colors.text,
                    }}
                >
                    DELBOT

                </div>

                <div
                    style={{
                        ...typography.caption,
                        color: colors.textMuted,
                        marginTop: 4,
                    }}
                >

                </div>
            </div>


            <div
                style={{
                    height: 1,
                    background: colors.border,
                }}
            />

            <nav style={navStyle}>

                <div
                    style={{
                        fontSize: "18px",
                        fontWeight: 800,
                        letterSpacing: "0.08em",
                        marginBottom: "18px",
                        padding: "0 12px",
                    }}
                >
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
    <span>Research Workspace</span>
                </NavLink>

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

            <div
                style={{
                    marginTop: "auto",
                    padding: "16px 20px",
                    borderTop: `1px solid ${colors.border}`,
                }}
            >
                <div
                    style={{
                        ...typography.caption,
                        color: colors.textMuted,
                    }}
                >

                </div>
            </div>

        </aside>
    );
}
