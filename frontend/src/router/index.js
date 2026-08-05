import { jsx as _jsx } from "react/jsx-runtime";
import { BrowserRouter, Routes, Route, } from "react-router-dom";
import DashboardPage from "../pages/dashboard";
export default function AppRouter() {
    return (_jsx(BrowserRouter, { children: _jsx(Routes, { children: _jsx(Route, { path: "/", element: _jsx(DashboardPage, {}) }) }) }));
}
