import { ReactNode } from "react";
import WorkspaceSidebar from "./WorkspaceSidebar";
interface Props {
    children: ReactNode;
}

export default function WorkspaceShell({ children }: Props) {
    return (
        <div className="delbot-app-shell">
            <WorkspaceSidebar />

            <div className="delbot-main-shell">
<main className="delbot-main-content">
                    {children}
                </main>
            </div>
        </div>
    );
}
