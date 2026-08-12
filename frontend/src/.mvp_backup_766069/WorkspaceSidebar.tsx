import { NavLink } from "react-router-dom";
import {
    LayoutDashboard,
    FolderOpen,
    FileText,
    Search,
    FlaskConical,
    ScanSearch,
    Lightbulb,
} from "lucide-react";
import type { CSSProperties } from "react";

const navigation = [
    {
        label: "Dashboard",
        path: "/",
        icon: LayoutDashboard,
    },
    {
        label: "Repository",
        path: "/repository",
        icon: FolderOpen,
    },
    {
        label: "Documents",
        path: "/documents",
        icon: FileText,
    },
    {
        label: "Search",
        path: "/search",
        icon: Search,
    },
    {
        label: "Research",
        path: "/research",
        icon: FlaskConical,
    },
    {
        label: "Research Gap",
        path: "/gap",
        icon: ScanSearch,
    },
    {
        label: "Thesis Ideas",
        path: "/thesis-ideas",
        icon: Lightbulb,
    },
];

const sidebar: CSSProperties = {
    width: 240,
    minWidth: 240,
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    background: "#ffffff",
    borderRight: "1px solid #e5e7eb",
};

const brand: CSSProperties = {
    padding: "22px 20px 18px",
};

const nav: CSSProperties = {
    flex: 1,
    padding: "12px",
    overflowY: "auto",
};

const footer: CSSProperties = {
    padding: "14px 16px",
    borderTop: "1px solid #e5e7eb",
    color: "#94a3b8",
    fontSize: 11,
    lineHeight: 1.5,
};

const itemStyle = (active: boolean): CSSProperties => ({
    display: "flex",
    alignItems: "center",
    gap: 11,
    width: "100%",
    padding: "9px 11px",
    marginBottom: 3,
    borderRadius: 7,
    color: active ? "#1d4ed8" : "#475569",
    background: active ? "#eff6ff" : "transparent",
    fontSize: 13,
    fontWeight: active ? 600 : 500,
    transition: "background .15s ease, color .15s ease",
});

const iconStyle: CSSProperties = {
    width: 17,
    height: 17,
    flexShrink: 0,
};

export default function WorkspaceSidebar() {
    return (
        <aside style={sidebar}>
            <div style={brand}>
                <div
                    style={{
                        fontSize: 18,
                        fontWeight: 700,
                        color: "#0f172a",
                        letterSpacing: "-0.02em",
                    }}
                >
                    DELBot
                </div>

                <div
                    style={{
                        marginTop: 4,
                        fontSize: 11,
                        color: "#94a3b8",
                    }}
                >
                    Academic Research Intelligence
                </div>
            </div>

            <div
                style={{
                    height: 1,
                    background: "#e5e7eb",
                }}
            />

            <nav style={nav} aria-label="Main navigation">
                <div
                    style={{
                        padding: "6px 10px 8px",
                        fontSize: 10,
                        fontWeight: 700,
                        color: "#94a3b8",
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                    }}
                >
                    Research
                </div>

                {navigation.map((item) => {
                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            end={item.path === "/"}
                            style={({ isActive }) =>
                                itemStyle(isActive)
                            }
                        >
                            {({ isActive }) => (
                                <>
                                    <Icon
                                        style={iconStyle}
                                        strokeWidth={isActive ? 2.2 : 1.8}
                                    />
                                    <span>{item.label}</span>
                                </>
                            )}
                        </NavLink>
                    );
                })}
            </nav>

            <div style={footer}>
                DELBot MVP
                <br />
                Academic Research Workspace
            </div>
        </aside>
    );
}
