import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import DashboardPage from "../pages/dashboard";
import RepositoryPage from "../pages/repository";

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
                    element={<Navigate to="/repository" replace />}
                />

                <Route
                    path="/search"
                    element={<Navigate to="/" replace />}
                />

                <Route
                    path="/research"
                    element={<Navigate to="/" replace />}
                />

                <Route
                    path="/gap"
                    element={<Navigate to="/" replace />}
                />

                <Route
                    path="/thesis-ideas"
                    element={<Navigate to="/" replace />}
                />

                <Route
                    path="*"
                    element={<Navigate to="/" replace />}
                />

            </Routes>
        </BrowserRouter>
    );
}
