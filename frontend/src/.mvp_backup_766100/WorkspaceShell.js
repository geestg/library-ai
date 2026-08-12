import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import WorkspaceSidebar from "./WorkspaceSidebar";
export default function WorkspaceShell({ children }) {
    return (_jsxs("div", { className: "delbot-app-shell", children: [_jsx(WorkspaceSidebar, {}), _jsx("div", { className: "delbot-main-shell", children: _jsx("main", { className: "delbot-main-content", children: children }) })] }));
}
