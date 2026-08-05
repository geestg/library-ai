import type {
    RepositoryDocument,
    RepositorySource,
} from "../../types/repository";

export interface BackendRepositoryDocument {

    id?: string;

    title?: string;

    author?: string;

    year?: string;

    abstract?: string;

    keywords?: string[];

    program_study?: string;

    repository_url?: string;

    pdf_url?: string;

    thumbnail_url?: string;

    page?: number;

    heading?: string;

    chunk_id?: string;

    snippet?: string;

    citation?: string;

    score?: number;

    source?: RepositorySource;
}

export function adaptRepositoryDocument(
    doc: BackendRepositoryDocument,
): RepositoryDocument {

    const source: RepositorySource =
        doc.source ?? "metadata";

    const pdfUrl =
        doc.pdf_url ?? "";

    return {

        id:
            doc.id ?? "",

        title:
            doc.title ?? "",

        author:
            doc.author ?? "",

        year:
            doc.year ?? "",

        abstract:
            doc.abstract ?? "",

        keywords:
            doc.keywords ?? [],

        programStudy:
            doc.program_study ?? "",

        repositoryUrl:
            doc.repository_url ?? "",

        pdfUrl,

        thumbnailUrl:
            doc.thumbnail_url ?? "",

        hasFulltext:
            pdfUrl.length > 0,

        hasMetadata:
            true,

        source,

        page:
            doc.page,

        chunkId:
            doc.chunk_id,

        heading:
            doc.heading,

        snippet:
            doc.snippet,

        citation:
            doc.citation,

        score:
            doc.score,
    };
}

export function adaptRepositoryDocuments(
    docs: BackendRepositoryDocument[],
): RepositoryDocument[] {

    return docs.map(adaptRepositoryDocument);

}
