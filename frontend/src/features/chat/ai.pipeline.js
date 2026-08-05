import { hybridRetrievalService, } from "../retrieval/hybrid";
export class AIResponsePipeline {
    async execute(request) {
        const retrieval = await hybridRetrievalService.search({
            query: request.message,
            workspaceId: request.workspaceId,
            topK: 8,
        });
        return {
            answer: "",
            retrieval,
        };
    }
}
export const aiPipeline = new AIResponsePipeline();
