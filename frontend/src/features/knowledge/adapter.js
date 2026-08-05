import { retrievalPipeline, } from "../retrieval";
export class RetrievalKnowledgeAdapter {
    async search(request) {
        return retrievalPipeline.retrieve(request);
    }
}
export const knowledgeAdapter = new RetrievalKnowledgeAdapter();
