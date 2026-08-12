import { Link, useLocation } from "react-router-dom";
import { Upload } from "lucide-react";
import { Button } from "../../components/ui";

const pageTitles: Record<string, string> = {
    "/": "Dashboard",
    "/repository": "Repository",
    "/documents": "Documents",
    "/search": "Search",
    "/research": "Research",
    "/gap": "Research Gap",
    "/thesis-ideas": "Thesis Ideas",
};

export default function WorkspaceTopbar() {
    const location = useLocation();

    const title =
        pageTitles[location.pathname] ?? "Research Workspace";

    return (
        <header className="delbot-topbar">
            <div className="delbot-topbar-title">
                <div className="delbot-page-title">
                    {title}
                </div>

                <div className="delbot-page-context">
                    Academic Research Workspace
                </div>
            </div>

            <div className="delbot-topbar-actions">
                <Link to="/repository">
                    <Button>
                        <Upload size={16} />
                        Import Repository
                    </Button>
                </Link>
            </div>
        </header>
    );
}
