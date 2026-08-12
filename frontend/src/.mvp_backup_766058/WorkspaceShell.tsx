import { ReactNode } from "react";

import WorkspaceSidebar from "./WorkspaceSidebar";
import WorkspaceTopbar from "./WorkspaceTopbar";

interface Props {
    children: ReactNode;
}

const rootStyle = {
    display: "flex",
    height: "100vh",
    background: "#f8fafc",
};

const bodyStyle = {
    display: "flex",
    flexDirection: "column" as const,
    flex: 1,
    overflow: "hidden",
};

const contentStyle = {
    flex: 1,
    overflow: "auto",
    padding: "24px 32px",
};

export default function WorkspaceShell({
    children,
}: Props) {
    return (
        <div style={rootStyle}>
            <WorkspaceSidebar />

            <div style={bodyStyle}>
                <WorkspaceTopbar />

                <main style={contentStyle}>
                    {children}
                </main>
            </div>
        </div>
    );
}
