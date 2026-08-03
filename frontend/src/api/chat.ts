import { api } from "./client";

export function chat(question: string) {
    return api.post("/chat", {
        question,
    });
}
