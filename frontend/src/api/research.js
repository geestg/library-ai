import { api } from "./client";
export function researchAnswer(question, sessionId) {
    return api.post("/api/research/answer", {
        question,
        session_id: sessionId,
    });
}
