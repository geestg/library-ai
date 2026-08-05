import { retrievalClient } from "./client";
export class HybridRetrievalService {
    async search(request) {
        const response = await retrievalClient.retrieve(request);
        return {
            ...response,
            source: response.source ?? "hybrid",
        };
    }
}
export const hybridRetrievalService = new HybridRetrievalService();
