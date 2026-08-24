import { api } from "./client";
export function researchAnswer(question, sessionId) {
    return api.post("/chat", {
        question,
        session_id: sessionId,
    });
}
