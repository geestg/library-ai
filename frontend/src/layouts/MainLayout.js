import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Link, Outlet, useLocation } from "react-router-dom";
import { LayoutDashboard, FolderOpen, Files, Search, FlaskConical, Settings, } from "lucide-react";
const menus = [
    {
        to: "/",
        label: "Dashboard",
        icon: LayoutDashboard,
    },
    {
        to: "/repository",
        label: "Repository",
        icon: FolderOpen,
    },
    {
        to: "/documents",
        label: "Documents",
        icon: Files,
    },
    {
        to: "/research",
        label: "Research",
        icon: FlaskConical,
    },
    {
        to: "/search",
        label: "Search",
        icon: Search,
    },
    {
        to: "/settings",
        label: "Settings",
        icon: Settings,
    },
];
export default function MainLayout() {
    const location = useLocation();
    return (_jsxs("div", { style: {
            display: "flex",
            minHeight: "100vh",
            background: "#f3f6fb",
            color: "#1f2937",
            fontFamily: "Inter, Arial, Helvetica, sans-serif",
        }, children: [_jsxs("aside", { style: {
                    width: 260,
                    background: "#111827",
                    color: "#fff",
                    display: "flex",
                    flexDirection: "column",
                    borderRight: "1px solid #1f2937",
                }, children: [_jsxs("div", { style: {
                            padding: "26px 24px",
                            borderBottom: "1px solid rgba(255,255,255,.08)",
                        }, children: [_jsx("div", { style: {
                                    fontSize: 24,
                                    fontWeight: 700,
                                }, children: "DELBot" }), _jsx("div", { style: {
                                    marginTop: 6,
                                    fontSize: 13,
                                    color: "#9ca3af",
                                }, children: "Academic Research Platform" })] }), _jsx("nav", { style: {
                            padding: 18,
                            flex: 1,
                        }, children: menus.map((item) => {
                            const Icon = item.icon;
                            const active = location.pathname === item.to;
                            return (_jsxs(Link, { to: item.to, style: {
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 12,
                                    padding: "12px 14px",
                                    marginBottom: 8,
                                    borderRadius: 10,
                                    textDecoration: "none",
                                    color: "#fff",
                                    background: active
                                        ? "#2563eb"
                                        : "transparent",
                                    transition: "0.2s",
                                    fontWeight: active
                                        ? 600
                                        : 500,
                                }, children: [_jsx(Icon, { size: 18 }), _jsx("span", { children: item.label })] }, item.to));
                        }) }), _jsx("div", { style: {
                            padding: 20,
                            borderTop: "1px solid rgba(255,255,255,.08)",
                            color: "#9ca3af",
                            fontSize: 12,
                        }, children: "DELBot MVP" })] }), _jsxs("div", { style: {
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                }, children: [_jsxs("header", { style: {
                            height: 72,
                            background: "#ffffff",
                            borderBottom: "1px solid #e5e7eb",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            padding: "0 28px",
                        }, children: [_jsxs("div", { children: [_jsx("div", { style: {
                                            fontSize: 24,
                                            fontWeight: 700,
                                        }, children: "DELBot MVP" }), _jsx("div", { style: {
                                            fontSize: 13,
                                            color: "#6b7280",
                                            marginTop: 4,
                                        }, children: "Digital Engineering Library Bot" })] }), _jsxs("div", { style: {
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 10,
                                }, children: [_jsx("span", { style: {
                                            width: 10,
                                            height: 10,
                                            borderRadius: "50%",
                                            background: "#22c55e",
                                            display: "inline-block",
                                        } }), _jsx("span", { style: {
                                            fontSize: 14,
                                            color: "#374151",
                                            fontWeight: 600,
                                        }, children: "System Ready" })] })] }), _jsx("main", { style: {
                            flex: 1,
                            padding: 28,
                            overflow: "auto",
                        }, children: _jsx(Outlet, {}) })] })] }));
}
