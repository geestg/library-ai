import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import DashboardPage from "../pages/dashboard";
import DocumentsPage from "../pages/documents";
import RepositoryPage from "../pages/repository";
import SearchPage from "../pages/search";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={<DashboardPage />}
                />

                <Route
                    path="/documents"
                    element={<DocumentsPage />}
                />

                <Route
                    path="/repository"
                    element={<RepositoryPage />}
                />

                <Route
                    path="/search"
                    element={<SearchPage />}
                />
            </Routes>
        </BrowserRouter>
    );
}
