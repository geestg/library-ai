import { chatApi } from "../api";
export class HttpChatBackend {
    async send(request) {
        return chatApi.send(request);
    }
}
export const chatBackend = new HttpChatBackend();
