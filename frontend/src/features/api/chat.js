import { apiClient } from "./client";
export class ChatApi {
    async send(request) {
        return apiClient.post("/api/chat", request);
    }
}
export const chatApi = new ChatApi();
