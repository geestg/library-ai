import type {
    RetrievalRequest,
    RetrievalResponse,
} from "../../contracts";

import { retrievalApi } from "../api";

export interface RetrievalBackend {
    search(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse>;
}

export class HttpRetrievalBackend
    implements RetrievalBackend {

    async search(
        request: RetrievalRequest,
    ): Promise<RetrievalResponse> {

        return retrievalApi.search(request);

    }

}

export const retrievalBackend =
    new HttpRetrievalBackend();
