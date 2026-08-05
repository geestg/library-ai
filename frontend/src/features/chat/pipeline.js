import { chatBackend } from "./backend";
import { hybridRetrievalService } from "../retrieval";
import { streamController } from "../stream";
export class ChatPipeline {
    async execute(request) {
        await hybridRetrievalService.search({
            query: request.message,
            workspaceId: request.workspaceId,
            topK: 5,
        });
        await streamController.start();
        return chatBackend.send(request);
    }
}
export const chatPipeline = new ChatPipeline();
