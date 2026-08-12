import { ReactNode } from "react";
import WorkspaceSidebar from "./WorkspaceSidebar";
import WorkspaceTopbar from "./WorkspaceTopbar";

interface Props {
    children: ReactNode;
}

export default function WorkspaceShell({ children }: Props) {
    return (
        <div className="delbot-app-shell">
            <WorkspaceSidebar />

            <div className="delbot-main-shell">
                <WorkspaceTopbar />

                <main className="delbot-main-content">
                    {children}
                </main>
            </div>
        </div>
    );
}
