import type { RepositoryDocument } from "../types/repository";

export interface ChatRequest {

    workspaceId: string;

    message: string;

}

export interface CitationReference {

    id: string;

    page?: number;

    chunkId?: string;

    score?: number;

    source:

        | "fulltext"
        | "metadata";

}

export interface ChatResponse {

    answer: string;

    citations: CitationReference[];

    documents: RepositoryDocument[];

}
