import { api } from "./client";
export function retrievalSearch(question, top_k = 5) {
    return api.post("/api/retrieval", {
        question,
        top_k,
    });
}
