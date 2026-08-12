import { api } from "./client";

export type RetrievalDocument = {
    id: string;
    score?: number;
    content?: string;
    source?: string;
    section?: string;
    page_start?: number;
    page_end?: number;
};

export type RetrievalResponse = {
    context?: string;
    documents?: RetrievalDocument[];
};

export function retrievalSearch(
    question: string,
    top_k = 5,
) {
    return api.post<RetrievalResponse>(
        "/api/retrieval",
        {
            question,
            top_k,
        },
    );
}
