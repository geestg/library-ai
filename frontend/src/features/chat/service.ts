import type {
    ChatRequest,
    ChatResponse,
} from "../../contracts";

import { chatApi } from "../api";
import { retrievalIntegration } from "../retrieval";
import { streamController } from "../stream";

export class ChatService {

    async execute(
        request: ChatRequest,
    ): Promise<ChatResponse> {

        await retrievalIntegration.search({
            query: request.message,
            workspaceId: request.workspaceId,
        });

        await streamController.start();

        return chatApi.send(request);
    }

}

export const chatService =
    new ChatService();
