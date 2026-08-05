import { Link, Outlet, useLocation } from "react-router-dom";
import {
    LayoutDashboard,
    FolderOpen,
    Files,
    Search,
    FlaskConical,
    Settings,
} from "lucide-react";

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

    return (

        <div
            style={{
                display: "flex",
                minHeight: "100vh",
                background: "#f3f6fb",
                color: "#1f2937",
                fontFamily:
                    "Inter, Arial, Helvetica, sans-serif",
            }}
        >

            <aside
                style={{
                    width: 260,
                    background: "#111827",
                    color: "#fff",
                    display: "flex",
                    flexDirection: "column",
                    borderRight: "1px solid #1f2937",
                }}
            >

                <div
                    style={{
                        padding: "26px 24px",
                        borderBottom:
                            "1px solid rgba(255,255,255,.08)",
                    }}
                >

                    <div
                        style={{
                            fontSize: 24,
                            fontWeight: 700,
                        }}
                    >
                        DELBot
                    </div>

                    <div
                        style={{
                            marginTop: 6,
                            fontSize: 13,
                            color: "#9ca3af",
                        }}
                    >
                        Academic Research Platform
                    </div>

                </div>

                <nav
                    style={{
                        padding: 18,
                        flex: 1,
                    }}
                >

                    {menus.map((item) => {

                        const Icon = item.icon;

                        const active =
                            location.pathname === item.to;

                        return (

                            <Link
                                key={item.to}
                                to={item.to}
                                style={{
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
                                }}
                            >

                                <Icon size={18} />

                                <span>
                                    {item.label}
                                </span>

                            </Link>

                        );

                    })}

                </nav>

                <div
                    style={{
                        padding: 20,
                        borderTop:
                            "1px solid rgba(255,255,255,.08)",
                        color: "#9ca3af",
                        fontSize: 12,
                    }}
                >
                    DELBot MVP
                </div>

            </aside>

            <div
                style={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                }}
            >

                <header
                    style={{
                        height: 72,
                        background: "#ffffff",
                        borderBottom:
                            "1px solid #e5e7eb",
                        display: "flex",
                        alignItems: "center",
                        justifyContent:
                            "space-between",
                        padding: "0 28px",
                    }}
                >

                    <div>

                        <div
                            style={{
                                fontSize: 24,
                                fontWeight: 700,
                            }}
                        >
                            DELBot MVP
                        </div>

                        <div
                            style={{
                                fontSize: 13,
                                color: "#6b7280",
                                marginTop: 4,
                            }}
                        >
                            Digital Engineering Library Bot
                        </div>

                    </div>

                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: 10,
                        }}
                    >

                        <span
                            style={{
                                width: 10,
                                height: 10,
                                borderRadius: "50%",
                                background: "#22c55e",
                                display: "inline-block",
                            }}
                        />

                        <span
                            style={{
                                fontSize: 14,
                                color: "#374151",
                                fontWeight: 600,
                            }}
                        >
                            System Ready
                        </span>

                    </div>

                </header>

                <main
                    style={{
                        flex: 1,
                        padding: 28,
                        overflow: "auto",
                    }}
                >
                    <Outlet />
                </main>

            </div>

        </div>

    );

}
