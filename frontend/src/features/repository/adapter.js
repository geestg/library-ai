export function adaptRepositoryDocument(doc) {
    const source = doc.source ?? "metadata";
    const pdfUrl = doc.pdf_url ?? "";
    return {
        id: doc.id ?? "",
        title: doc.title ?? "",
        author: doc.author ?? "",
        year: doc.year ?? "",
        abstract: doc.abstract ?? "",
        keywords: doc.keywords ?? [],
        programStudy: doc.program_study ?? "",
        repositoryUrl: doc.repository_url ?? "",
        pdfUrl,
        thumbnailUrl: doc.thumbnail_url ?? "",
        hasFulltext: pdfUrl.length > 0,
        hasMetadata: true,
        source,
        page: doc.page,
        chunkId: doc.chunk_id,
        heading: doc.heading,
        snippet: doc.snippet,
        citation: doc.citation,
        score: doc.score,
    };
}
export function adaptRepositoryDocuments(docs) {
    return docs.map(adaptRepositoryDocument);
}
