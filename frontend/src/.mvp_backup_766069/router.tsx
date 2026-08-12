import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import DashboardPage from "../pages/dashboard";
import DocumentsPage from "../pages/documents";
import RepositoryPage from "../pages/repository";
import SearchPage from "../pages/search";
import ResearchPage from "../pages/research";
import GapPage from "../pages/gap";
import ThesisIdeasPage from "../pages/thesis-ideas";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={<DashboardPage />}
                />

                <Route
                    path="/repository"
                    element={<RepositoryPage />}
                />

                <Route
                    path="/documents"
                    element={<DocumentsPage />}
                />

                <Route
                    path="/search"
                    element={<SearchPage />}
                />

                <Route
                    path="/research"
                    element={<ResearchPage />}
                />

                <Route
                    path="/gap"
                    element={<GapPage />}
                />

                <Route
                    path="/thesis-ideas"
                    element={<ThesisIdeasPage />}
                />
            </Routes>
        </BrowserRouter>
    );
}
