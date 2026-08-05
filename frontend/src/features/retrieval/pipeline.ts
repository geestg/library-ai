import type {
    RetrievalRequest,
    RetrievalResponse,
} from "../../contracts";

import { retrievalBackend } from "./backend";

export class RetrievalPipeline {

    async retrieve(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        return retrievalBackend.search(request);

    }

}

export const retrievalPipeline =
    new RetrievalPipeline();

