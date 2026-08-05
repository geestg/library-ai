import { retrievalBackend, } from "./backend";
export class RetrievalIntegration {
    async search(request) {
        return retrievalBackend.search(request);
    }
}
export const retrievalIntegration = new RetrievalIntegration();
