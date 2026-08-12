import { jsx as _jsx } from "react/jsx-runtime";
import WorkspaceShell from "../../components/layout/WorkspaceShell";
import ConversationWorkspace from "../../features/workspace/ConversationWorkspace";
export default function DashboardPage() {
    return (_jsx(WorkspaceShell, { children: _jsx(ConversationWorkspace, {}) }));
}
