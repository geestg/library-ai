import type {
    RetrievalRequest,
    RetrievalResponse,
} from "../../contracts/retrieval";

export interface RetrievalClient {

    retrieve(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse>;

}

export class HttpRetrievalClient
implements RetrievalClient {

    async retrieve(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        const response =
            await fetch(
                "/retrieval",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({
                        question:
                            request.query,
                    }),
                },
            );

        if (!response.ok) {

            throw new Error(
                `Retrieval request failed (${response.status})`,
            );

        }

        const data =
            await response.json();

        return {

            query:
                request.query,

            documents:
                data.documents ?? [],

            total:
                data.documents?.length ?? 0,

            elapsedMs:
                data.elapsedMs,

            source:
                "hybrid",

        };

    }

}

export const retrievalClient =
    new HttpRetrievalClient();
