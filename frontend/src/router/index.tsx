import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import DashboardPage from "../pages/dashboard";
import RepositoryPage from "../pages/repository";
import DocumentsPage from "../pages/documents";
import SearchPage from "../pages/search";
import ResearchPage from "../pages/research";
import SettingsPage from "../pages/settings";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<MainLayout />}>
                    <Route path="/" element={<DashboardPage />} />
                    <Route path="/repository" element={<RepositoryPage />} />
                    <Route path="/documents" element={<DocumentsPage />} />
                    <Route path="/search" element={<SearchPage />} />
                    <Route path="/research" element={<ResearchPage />} />
                    <Route path="/settings" element={<SettingsPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
