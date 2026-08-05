import { retrievalBackend } from "./backend";
export class RetrievalPipeline {
    async retrieve(request) {
        return retrievalBackend.search(request);
    }
}
export const retrievalPipeline = new RetrievalPipeline();
