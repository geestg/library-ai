import { api } from "./client";

export type ResearchCitation = {
    document_id: string;
    source: string;
    section: string;
    page_start?: number | null;
    page_end?: number | null;
};

export type ResearchAnswerResponse = {
    answer: string;
    citations: ResearchCitation[];
    session_id: string;
    research_state?: Record<string, unknown>;
    context_length?: number;
    documents?: number;
    retrieved?: number;
};

export function researchAnswer(
    question: string,
    sessionId: string,
) {
    return api.post<ResearchAnswerResponse>(
        "/chat",
        {
            question,
            session_id: sessionId,
        },
    );
}
