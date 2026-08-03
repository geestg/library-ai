import { api } from "./client";

export function indexRepository(limit = 25) {
    return api.post("/documents/index-all", {
        limit,
    });
}
