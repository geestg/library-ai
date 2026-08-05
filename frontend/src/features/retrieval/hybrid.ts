import type {
    RetrievalRequest,
    RetrievalResponse,
} from "../../contracts";

import { retrievalClient } from "./client";

export class HybridRetrievalService {

    async search(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        const response =
            await retrievalClient.retrieve(request);

        return {

            ...response,

            source:
                response.source ?? "hybrid",

        };

    }

}

export const hybridRetrievalService =
    new HybridRetrievalService();
