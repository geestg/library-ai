import type { RepositoryDocument } from "../types/repository";

export interface RetrievalRequest {
    query: string;
    workspaceId?: string;
    topK?: number;
}

export interface RetrievalResponse {

    query: string;

    documents: RepositoryDocument[];

    total: number;

    elapsedMs?: number;

    source: "fulltext" | "metadata" | "hybrid";
}
