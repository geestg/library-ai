import { api } from "./client";
export function chat(question) {
    return api.post("/chat", {
        question,
    });
}
