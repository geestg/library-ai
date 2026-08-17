import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter, Navigate, Route, Routes, } from "react-router-dom";
import DashboardPage from "../pages/dashboard";
import RepositoryPage from "../pages/repository";
import SearchPage from "../pages/search";
import ResearchPage from "../pages/research";
import GapPage from "../pages/gap";
import ThesisIdeasPage from "../pages/thesis-ideas";
export default function AppRouter() {
    return (_jsx(BrowserRouter, { children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(DashboardPage, {}) }), _jsx(Route, { path: "/repository", element: _jsx(RepositoryPage, {}) }), _jsx(Route, { path: "/search", element: _jsx(SearchPage, {}) }), _jsx(Route, { path: "/research", element: _jsx(ResearchPage, {}) }), _jsx(Route, { path: "/gap", element: _jsx(GapPage, {}) }), _jsx(Route, { path: "/thesis-ideas", element: _jsx(ThesisIdeasPage, {}) }), _jsx(Route, { path: "*", element: _jsx(Navigate, { to: "/", replace: true }) })] }) }));
}
