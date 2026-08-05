import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import WorkspaceSidebar from "./WorkspaceSidebar";
import WorkspaceTopbar from "./WorkspaceTopbar";
const rootStyle = {
    display: "flex",
    height: "100vh",
    background: "#f8fafc",
};
const bodyStyle = {
    display: "flex",
    flexDirection: "column",
    flex: 1,
    overflow: "hidden",
};
const contentStyle = {
    flex: 1,
    overflow: "auto",
    padding: "24px 32px",
};
export default function WorkspaceShell({ children, }) {
    return (_jsxs("div", { style: rootStyle, children: [_jsx(WorkspaceSidebar, {}), _jsxs("div", { style: bodyStyle, children: [_jsx(WorkspaceTopbar, {}), _jsx("main", { style: contentStyle, children: children })] })] }));
}
