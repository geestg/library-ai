import type {
    ChatRequest,
    ChatResponse,
} from "../../contracts";

import { chatApi } from "../api";

export interface ChatBackend {

    send(
        request: ChatRequest,
    ): Promise<ChatResponse>;

}

export class HttpChatBackend
implements ChatBackend {

    async send(
        request: ChatRequest,
    ): Promise<ChatResponse> {

        return chatApi.send(request);

    }

}

export const chatBackend =
    new HttpChatBackend();
