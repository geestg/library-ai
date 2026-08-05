import type {
    RetrievalRequest,
    RetrievalResponse,
} from "../../contracts";

import {
    retrievalBackend,
} from "./backend";

export class RetrievalIntegration {

    async search(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        return retrievalBackend.search(request);

    }

}

export const retrievalIntegration =
    new RetrievalIntegration();
