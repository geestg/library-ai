import type {
    RetrievalRequest,
    RetrievalResponse,
} from "../../contracts";

import { hybridRetrievalService } from "../retrieval/hybrid";

export class RetrievalApi {

    async retrieve(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        return hybridRetrievalService.search(request);

    }

    async search(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        return this.retrieve(request);

    }

}

export const retrievalApi = new RetrievalApi();
