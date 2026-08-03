import { api } from "./client";

export function repositoryExplorer() {
    return api.get("/repository/explorer");
}

export function repositoryScan(path: string) {
    return api.post("/repository/scan", {
        path,
    });
}
