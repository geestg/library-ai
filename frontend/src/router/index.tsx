import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import DashboardPage from "../pages/dashboard";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={<DashboardPage />}
                />
            </Routes>
        </BrowserRouter>
    );
}
