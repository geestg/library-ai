import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter, Routes, Route, } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import DashboardPage from "../pages/dashboard";
import RepositoryPage from "../pages/repository";
import DocumentsPage from "../pages/documents";
import SearchPage from "../pages/search";
import ResearchPage from "../pages/research";
import SettingsPage from "../pages/settings";
export default function AppRouter() {
    return (_jsx(BrowserRouter, { children: _jsx(Routes, { children: _jsxs(Route, { element: _jsx(MainLayout, {}), children: [_jsx(Route, { path: "/", element: _jsx(DashboardPage, {}) }), _jsx(Route, { path: "/repository", element: _jsx(RepositoryPage, {}) }), _jsx(Route, { path: "/documents", element: _jsx(DocumentsPage, {}) }), _jsx(Route, { path: "/search", element: _jsx(SearchPage, {}) }), _jsx(Route, { path: "/research", element: _jsx(ResearchPage, {}) }), _jsx(Route, { path: "/settings", element: _jsx(SettingsPage, {}) })] }) }) }));
}
