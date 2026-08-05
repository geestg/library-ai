import { apiClient } from "../api";
export class BackendHealthService {
    async check() {
        try {
            return await apiClient.get("/health");
        }
        catch {
            return {
                status: "offline",
                ready: false,
            };
        }
    }
}
export const backendHealth = new BackendHealthService();
