import { NavLink } from "react-router-dom";
import {
    BookOpen,
    FileText,
    LayoutDashboard,
    Search,
    FlaskConical,
    Lightbulb,
    FolderSearch,
} from "lucide-react";

const navigation = [
    {
        label: "Dashboard",
        path: "/",
        icon: LayoutDashboard,
    },
    {
        label: "Repository",
        path: "/repository",
        icon: FolderSearch,
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
        icon: BookOpen,
    },
    {
        label: "Thesis Ideas",
        path: "/thesis-ideas",
        icon: Lightbulb,
    },
];

export default function WorkspaceSidebar() {
    return (
        <aside className="delbot-sidebar">
            <div className="delbot-brand">
                <div className="delbot-brand-mark">
                    D
                </div>

                <div>
                    <div className="delbot-brand-name">
                        DELBot
                    </div>

                    <div className="delbot-brand-subtitle">
                        Academic Research
                    </div>
                </div>
            </div>

            <nav
                className="delbot-navigation"
                aria-label="Main navigation"
            >
                <div className="delbot-navigation-label">
                    WORKSPACE
                </div>

                {navigation.map((item) => {
                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            end={item.path === "/"}
                            className={({ isActive }) =>
                                `delbot-nav-item ${
                                    isActive
                                        ? "is-active"
                                        : ""
                                }`
                            }
                        >
                            <Icon
                                size={17}
                                strokeWidth={1.8}
                            />

                            <span>{item.label}</span>
                        </NavLink>
                    );
                })}
            </nav>

            <div className="delbot-sidebar-footer">
                <div className="delbot-sidebar-footer-title">
                    Research Workspace
                </div>

                <div className="delbot-sidebar-footer-text">
                    Evidence-backed academic research.
                </div>
            </div>
        </aside>
    );
}
