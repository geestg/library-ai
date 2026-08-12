import { api } from "./client";
export function chat(question, sessionId) {
    return api.post("/chat", {
        question,
        session_id: sessionId,
    });
}
