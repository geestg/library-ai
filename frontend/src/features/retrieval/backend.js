import { retrievalApi } from "../api";
export class HttpRetrievalBackend {
    async search(request) {
        return retrievalApi.search(request);
    }
}
export const retrievalBackend = new HttpRetrievalBackend();
