import { api } from "./client";

export type ChatResponse = {
    answer: string;
    session_id: string;
};

export function chat(
    question: string,
    sessionId: string,
) {
    return api.post<ChatResponse>(
        "/chat",
        {
            question,
            session_id: sessionId,
        },
    );
}
