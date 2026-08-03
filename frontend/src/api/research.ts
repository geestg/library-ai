import { api } from "./client";

export function researchAnswer(question: string) {
    return api.post("/research/answer", {
        question,
    });
}
