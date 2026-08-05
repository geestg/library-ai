import { apiClient } from "../api";

export interface BackendHealth {

    status: string;

    ready: boolean;

}

export class BackendHealthService {

    async check(): Promise<BackendHealth> {

        try {

            return await apiClient.get("/health");

        } catch {

            return {
                status: "offline",
                ready: false,
            };

        }

    }

}

export const backendHealth =
    new BackendHealthService();
