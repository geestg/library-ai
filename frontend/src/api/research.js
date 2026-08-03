import { api } from "./client";
export function researchAnswer(question) {
    return api.post("/research/answer", {
        question,
    });
}
