import { api } from "./client";

export function repositoryExplorer() {
    return api.get("/api/repository/explorer");
}

export function repositoryScan(path: string) {
    return api.post("/api/repository/scan", {
        path,
    });
}
