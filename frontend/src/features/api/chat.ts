import type {
    ChatRequest,
    ChatResponse,
} from "../../contracts";

import { apiClient } from "./client";

export class ChatApi {

    async send(
        request: ChatRequest,
    ): Promise<ChatResponse> {

        return apiClient.post<ChatResponse>(
            "/api/chat",
            request,
        );

    }

}

export const chatApi = new ChatApi();
