import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter, Routes, Route, } from "react-router-dom";
import DashboardPage from "../pages/dashboard";
import DocumentsPage from "../pages/documents";
import RepositoryPage from "../pages/repository";
import SearchPage from "../pages/search";
export default function AppRouter() {
    return (_jsx(BrowserRouter, { children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(DashboardPage, {}) }), _jsx(Route, { path: "/documents", element: _jsx(DocumentsPage, {}) }), _jsx(Route, { path: "/repository", element: _jsx(RepositoryPage, {}) }), _jsx(Route, { path: "/search", element: _jsx(SearchPage, {}) })] }) }));
}
