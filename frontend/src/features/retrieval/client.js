export class HttpRetrievalClient {
    async retrieve(request) {
        const response = await fetch("/retrieval", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question: request.query,
            }),
        });
        if (!response.ok) {
            throw new Error(`Retrieval request failed (${response.status})`);
        }
        const data = await response.json();
        return {
            query: request.query,
            documents: data.documents ?? [],
            total: data.documents?.length ?? 0,
            elapsedMs: data.elapsedMs,
            source: "hybrid",
        };
    }
}
export const retrievalClient = new HttpRetrievalClient();
