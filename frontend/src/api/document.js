import { api } from "./client";
export function indexRepository(limit = 25) {
    return api.post("/api/documents/index-all", {
        limit,
    });
}
