import WorkspaceShell from "../../components/layout/WorkspaceShell";
import ConversationWorkspace from "../../features/workspace/ConversationWorkspace";

export default function DashboardPage() {
    return (
        <WorkspaceShell>
            <ConversationWorkspace />
        </WorkspaceShell>
    );
}
