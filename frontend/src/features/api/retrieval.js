import { hybridRetrievalService } from "../retrieval/hybrid";
export class RetrievalApi {
    async retrieve(request) {
        return hybridRetrievalService.search(request);
    }
    async search(request) {
        return this.retrieve(request);
    }
}
export const retrievalApi = new RetrievalApi();
