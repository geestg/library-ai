export type RepositorySource =
    | "fulltext"
    | "metadata";

export interface RepositoryDocument {

    id: string;

    source: RepositorySource;

    title: string;

    author: string;

    year: string;

    programStudy: string;

    abstract: string;

    keywords: string[];

    repositoryUrl: string;

    pdfUrl: string;

    thumbnailUrl: string;

    hasFulltext: boolean;

    hasMetadata: boolean;

    // ------------------------------------------------
    // Retrieval
    // ------------------------------------------------

    score?: number;

    page?: number;

    chunkId?: string;

    chunkIndex?: number;

    section?: string;

    heading?: string;

    snippet?: string;

    citation?: string;

    // ------------------------------------------------
    // Metadata
    // ------------------------------------------------

    createdAt?: string;

    updatedAt?: string;
}
